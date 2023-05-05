import locale
from locale import format_string


class Stats:
    def __init__(self, description, count, unit_name):
        self.description = description
        self.count = count
        self.unit_name = unit_name

    def __str__(self):
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        return f"{self.description}: {format_string('%d', self.count, grouping=True)} {self.unit_name}"
