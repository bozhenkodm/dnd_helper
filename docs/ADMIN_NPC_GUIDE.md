# Admin Site and NPC Model Guide

This guide provides comprehensive documentation for using the Django admin interface to create and manage NPCs (Non-Player Characters) in the D&D Helper application.

## Table of Contents

- [Admin Site Overview](#admin-site-overview)
- [NPC Model Structure](#npc-model-structure)
- [Creating NPCs](#creating-npcs)
- [NPC Fields Reference](#npc-fields-reference)
- [Power Management](#power-management)
- [Equipment System](#equipment-system)
- [Admin Features](#admin-features)
- [Troubleshooting](#troubleshooting)

## Admin Site Overview

### Access
- **URL**: `http://127.0.0.1:8000/admin/`
- **Authentication**: Superuser or staff account required
- **User Isolation**: Users can only see their own NPCs (superusers see all)

### Key Sections
- **Base** → **NPCs**: Main character management
- **Base** → **Powers**: Spell/ability management
- **Base** → **Races**: Character races
- **Base** → **Classes**: Character classes
- **Items** → **Armor/Weapons**: Equipment management

## NPC Model Structure

The NPC model represents a complete D&D 4th Edition character with the following architecture:

### Core Components
```
NPC inherits from:
├── NPCClassAbstract (class/subclass management)
├── NPCDefenceMixin (AC, Fort, Ref, Will calculations)
├── NPCExperienceAbstract (experience and leveling)
├── NPCAbilityAbstract (ability scores and modifiers)
├── NPCSkillAbstract (skill bonuses and calculations)
├── PowerMixin (power display and calculation)
├── NPCMagicItemAbstract (magic item slot management)
├── BonusMixin (comprehensive bonus system)
└── NPCFeatAbstract (feat management)
```

### Key Relationships
- **Owner**: Each NPC belongs to a specific user
- **Race**: Defines racial bonuses and abilities
- **Class**: Determines powers, skills, and progression
- **Powers**: Many-to-many relationship with spell/abilities
- **Equipment**: Foreign keys to armor, weapons, and magic items

## Creating NPCs

### Step-by-Step Process

1. **Navigate to Admin**
   - Go to `http://127.0.0.1:8000/admin/`
   - Login with superuser or staff credentials

2. **Create New NPC**
   - Click "Base" → "NPCs" → "Add NPC"
   - Fill in required fields (marked with *)

3. **Basic Information**
   ```
   Name: [Character name, max 50 characters]
   Description: [Optional character background]
   Sex: [Male/Female/Other - radio buttons]
   Level: [1-30, defaults to 1]
   Race: [Select from dropdown with search]
   ```

4. **Ability Scores**
   - Set base ability scores (8-18 typically)
   - Choose variable racial bonus ability if applicable
   - Scores automatically calculate modifiers

5. **Class Selection**
   - Choose primary class
   - Select subclass if available
   - Optional functional template for specialized builds

6. **Equipment Assignment**
   - **Armor**: Select from available armor types
   - **Weapons**: Assign to primary/secondary/no-hand slots
   - **Magic Items**: Fill available slots (neck, head, waist, etc.)

7. **Skills and Powers**
   - Select trained skills (limited by class)
   - Assign powers from class, race, and other sources
   - Powers are automatically filtered by source and level

### Level-Dependent Features

- **Paragon Path**: Available at level 11+
- **Epic Destiny**: Available at level 21+
- **Power Selection**: Expands with level progression
- **Magic Item Enhancement**: Limited by level

## NPC Fields Reference

### Required Fields
| Field          | Type                 | Description                  |
|----------------|----------------------|------------------------------|
| Name           | CharField(50)        | Character's name             |
| Race           | ForeignKey           | Character's race             |
| Level          | PositiveIntegerField | Character level (1-30)       |
| Base Abilities | IntegerField × 6     | STR, CON, DEX, INT, WIS, CHA |

### Optional Fields
| Field                  | Type       | Description                 |
|------------------------|------------|-----------------------------|
| Description            | TextField  | Character background/notes  |
| Sex                    | Choice     | Character gender            |
| Functional Template    | ForeignKey | Special character template  |
| Paragon Path           | ForeignKey | Level 11+ advancement path  |
| Variable Bonus Ability | ForeignKey | Racial +2 ability choice    |

### Equipment Slots
| Slot           | Purpose             | Restrictions               |
|----------------|---------------------|----------------------------|
| Armor          | AC calculation      | One armor piece            |
| Primary Hand   | Main weapon         | Any weapon type            |
| Secondary Hand | Off-hand weapon     | Light weapons, shields     |
| No Hand        | Implement           | Specific implements        |
| Magic Items    | Enhancement bonuses | One per slot, level limits |

### Calculated Fields
- **Ability Modifiers**: Auto-calculated from base scores + bonuses
- **Defense Values**: AC, Fortitude, Reflex, Will
- **Skill Bonuses**: Base modifier + training + bonuses
- **Attack/Damage**: Weapon + ability + enhancement bonuses

## Power Management

### Power Sources
NPCs can acquire powers from multiple sources:

1. **Race Powers**: Granted by character race (level 0)
2. **Class Powers**: Core class abilities by level
3. **Subclass Powers**: Additional specialization powers
4. **Magic Item Powers**: From equipped magical items
5. **Functional Template**: Template-specific abilities
6. **Paragon Path Powers**: Advanced path abilities
7. **Manual Assignment**: Custom power additions

### Power Display
- Powers show **weapon-specific variations** for attacks
- **Dynamic calculations** include current bonuses
- **Expression evaluation** for complex damage formulas
- **Multiple weapon combinations** for two-weapon fighting

### Power Filtering
The admin interface automatically filters available powers by:
- Character level requirements
- Class/race prerequisites
- Power source restrictions
- Already selected powers

## Equipment System

### Weapon Proficiency
- Characters must be proficient with equipped weapons
- Proficiency comes from race, class, or feats
- Non-proficient weapons show penalties

### Magic Item Enhancement
- Enhancement bonuses are **level-limited**:
  - Levels 1-5: +1 items
  - Levels 6-10: +2 items
  - Levels 11-15: +3 items
  - Levels 16-20: +4 items
  - Levels 21-25: +5 items
  - Levels 26-30: +6 items

### Armor Class Calculation
```
AC = 10 + Armor Bonus + Shield Bonus + Ability Modifier + Enhancement Bonus + Other Bonuses
```

## Admin Features

### Dynamic Field Display
- Fields change based on character state
- Level requirements hide/show certain options
- Bonus application toggles additional fields

### Search and Filtering
- **Autocomplete fields** for races, classes, equipment
- **User-based filtering** (privacy protection)
- **Advanced search** by name, level, race, class

### Bulk Operations
- **Cache NPCs**: Refresh calculated bonuses and values
- **Export functionality**: Generate character sheets
- **Batch updates**: Modify multiple NPCs simultaneously

### Validation
- **Level restrictions** for paragon paths and items
- **Proficiency checking** for weapons and armor
- **Slot limitations** for magic items
- **Prerequisite validation** for powers and feats

## Character Calculation System

### Bonus Stacking
The system handles complex bonus stacking rules:
- **Enhancement bonuses**: Don't stack with same type
- **Racial bonuses**: Applied automatically
- **Class features**: Level-based progression
- **Feat bonuses**: Conditional applications
- **Item bonuses**: Slot-based restrictions

### Performance Optimization
- **Calculation caching** for complex formulas
- **Lazy loading** of related objects
- **Efficient queries** for power displays
- **Manual cache refresh** when needed

### Expression Evaluation
Powers use a sophisticated expression system:
```python
# Example power expression
"1d8 + [STR] + [weapon_enhancement]"
# Evaluates to actual damage based on current stats
```

## Troubleshooting

### Common Issues

**Issue**: NPC powers not displaying correctly
**Solution**: Use "Cache NPC" admin action to refresh calculations

**Issue**: Equipment not providing expected bonuses
**Solution**: Check level restrictions and proficiency requirements

**Issue**: Ability scores seem wrong
**Solution**: Verify racial bonuses and variable bonus ability selection

**Issue**: Can't see other users' NPCs
**Solution**: This is intentional - users are isolated for privacy

### Data Integrity

The system includes several safeguards:
- **Automatic level/experience sync** on save
- **Bonus recalculation** when equipment changes
- **Validation rules** prevent invalid configurations
- **Cascade deletion** protection for referenced objects

## Advanced Usage

### Custom Templates
Create functional templates for recurring character types:
1. Design template with specific power/feat combinations
2. Save as functional template
3. Apply to new NPCs for consistent builds

### Power Variants
Many powers have multiple display variants:
- Different weapons show different attack/damage
- Conditional effects based on equipment
- Situational bonuses from feats/items

### Character Progression
Track character advancement:
1. Increase level appropriately
2. Add new powers as they become available
3. Upgrade equipment within level limits
4. Select paragon path at level 11
5. Choose epic destiny at level 21

## File Locations

For developers and advanced users:

```
base/models/models.py          # Main NPC model definition
base/admin/admin_classes.py    # Admin interface configuration  
base/forms/npc.py             # Custom forms for NPC creation
base/views.py                 # Web interface views
base/tests/test_npc.py        # Comprehensive test suite
templates/base/               # HTML templates for display
```

This system provides a complete implementation of D&D 4th Edition character mechanics with a user-friendly admin interface for creating and managing complex NPCs.