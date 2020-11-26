from io import BytesIO
from itertools import cycle

import xlsxwriter


class ExcelMixin:
    def write_npc(self, sheet, row, column, npc):
        sheet.write(row, column, npc.name)
        column += 1
        sheet.merge_range(
            row, column, row, column + 3, f'{npc.klass} {npc.level} уровня'
        )
        row += 1
        column = 0
        sheet.write(row, column, str(npc.race))
        row += 1
        for property in npc.race.bonuses.all():
            sheet.write(row, column, property.name)
            row += 1
        for property in npc.klass.bonuses.all():
            sheet.write(row, column, property.name)
            row += 1
        sheet.write(row, 0, f'КД {npc.armor_class}')
        sheet.write(row, 1, f'Стойкость {npc.fortitude}')
        sheet.write(row, 2, f'Реакция {npc.reflex}')
        sheet.write(row, 3, f'Воля {npc.will}')
        return row + 2

    def generate_excel(self):
        output = BytesIO()
        book = xlsxwriter.Workbook(output)
        sheet = book.add_worksheet()
        row = 0
        for npc in self.npcs.all():
            column = 0
            row = self.write_npc(sheet, row, column, npc)
        book.close()
        return output
