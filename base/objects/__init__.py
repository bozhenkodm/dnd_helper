from base.objects import implement_types, npc_classes, races, weapon_types

races_tuple = (
    # races.BladelingRace,  # too exotic for now
    races.BugbearRace,
    races.DevaRace,
    races.DoppelgangerRace,
    races.DragonbornRace,
    races.DrowRace,
    races.DuergarRace,
    races.DwarfRace,
    races.EladrinRace,
    races.ElfRace,
    races.GenasiEarthsoulRace,
    races.GenasiFiresoulRace,
    races.GenasiStormsoulRace,
    races.GenasiWatersoulRace,
    races.GenasiWindsoulRace,
    races.GithzeraiRace,
    races.GnollRace,
    races.GnomeRace,
    races.GoblinRace,
    races.GoliathRace,
    races.HalfelfRace,
    races.HalflingRace,
    races.HalforcRace,
    # races.HamadryadRace,  # too exotic for now
    races.HobgoblinRace,
    races.HumanRace,
    races.KalashtarRace,
    # races.KenkuRace,  # too exotic for now
    races.KoboldRace,
    races.MinotaurRace,
    races.MulRace,
    # races.OrcRace,
    # races.PixieRace,  # too exotic for now
    races.SatyrRace,  # too exotic for now
    races.ShadarKaiRace,
    races.ShifterLongteethRace,
    races.ShifterRazorclawRace,
    races.ThriKreenRace,
    races.TieflingRace,
    races.VrylokaRace,
    races.WarforgedRace,
    # races.WildenRace,  # dummy
)

race_classes = {cls.slug.name: cls for cls in races_tuple}


npc_klasses = {
    cls.slug.value: cls
    for cls in (
        npc_classes.ArtificerClass,
        npc_classes.AvengerClass,
        npc_classes.BarbarianClass,
        npc_classes.BardClass,
        npc_classes.DruidClass,
        npc_classes.FighterClass,
        npc_classes.HexbladeClass,
        npc_classes.InvokerClass,
        npc_classes.MonkClass,
        npc_classes.PaladinClass,
        npc_classes.PriestClass,
        npc_classes.RangerMarksmanClass,
        npc_classes.RangerMeleeClass,
        npc_classes.RogueClass,
        npc_classes.RunepriestClass,
        npc_classes.SeekerClass,
        npc_classes.ShamanClass,
        npc_classes.SorcererClass,
        npc_classes.SwordmageClass,
        npc_classes.VampireClass,
        npc_classes.WardenClass,
        npc_classes.WarlockClass,
        npc_classes.WarlordClass,
        npc_classes.WizardClass,
    )
}

_weapon_types_tuple = (
    weapon_types.AnnihilationBlade,  # hexblade weapon
    weapon_types.BastardSword,
    weapon_types.Battleaxe,
    weapon_types.Broadsword,
    weapon_types.ChaosBlade,  # hexblade weapon
    weapon_types.Club,
    weapon_types.Craghammer,
    weapon_types.Crossbow,
    weapon_types.Dagger,
    weapon_types.ExecutionAxe,
    weapon_types.ExquisiteAgonyScourge,  # hexblade weapon
    weapon_types.Falchion,
    weapon_types.Flail,
    weapon_types.Fullblade,
    weapon_types.Glaive,
    weapon_types.Greataxe,
    weapon_types.Greatbow,
    weapon_types.Greatclub,
    weapon_types.Greatspear,
    weapon_types.Greatsword,
    weapon_types.Halberg,
    weapon_types.HandCrossbow,
    weapon_types.Handaxe,
    weapon_types.HeavyFlail,
    weapon_types.HeavyWarPick,
    weapon_types.Javelin,
    weapon_types.Katar,
    weapon_types.Khopesh,
    weapon_types.Kukri,
    weapon_types.LightMace,
    weapon_types.LightWarPick,
    weapon_types.LongSword,
    weapon_types.Longbow,
    weapon_types.Longspear,
    weapon_types.Mace,
    weapon_types.Maul,
    weapon_types.Mordenkrad,
    weapon_types.Morningstar,
    weapon_types.ParryingDagger,
    weapon_types.Quaterstaff,
    weapon_types.Rapier,
    weapon_types.RepeatingCrossbow,
    weapon_types.RitualDagger,  # warlock implement
    weapon_types.RitualSickle,  # warlock implement
    weapon_types.Scimitar,
    weapon_types.Scourge,
    weapon_types.Scythe,
    weapon_types.ShortSpear,
    weapon_types.ShortSword,
    weapon_types.Shortbow,
    weapon_types.Shuriken,
    weapon_types.Sickle,
    weapon_types.Sling,
    weapon_types.Spear,
    weapon_types.SpikedChain,
    weapon_types.SpikedGauntlet,
    weapon_types.SuperiorCrossbow,
    weapon_types.ThrowingHammer,
    weapon_types.Tratnyr,
    weapon_types.Trident,
    weapon_types.TrippleHeadedFlail,
    weapon_types.WarPick,
    weapon_types.Waraxe,
    weapon_types.Warhammer,
    weapon_types.WinterMourningBlade,  # hexblade weapon
)

weapon_types_classes = {cls.slug: cls for cls in _weapon_types_tuple}

implement_types_classes = {
    cls.slug: cls
    for cls in (
        implement_types.Wand,
        implement_types.Rod,
        implement_types.Totem,
        implement_types.HolySymbol,
        implement_types.KiFocus,
        implement_types.Sphere,
    )
}
implement_types_classes.update(
    {cls.slug: cls for cls in _weapon_types_tuple if cls.is_implement}
)
