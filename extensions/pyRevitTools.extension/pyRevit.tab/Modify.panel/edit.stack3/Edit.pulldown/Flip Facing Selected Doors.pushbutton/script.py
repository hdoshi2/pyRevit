"""Flips the facing for the selected doors."""

from pyrevit import revit


__context__ = 'selection'


selection = revit.get_selection()

with revit.Transaction('Flip Facing Selected Doors'):
    for el in selection:
        if el.Category.Name == 'Doors':
            el.flipFacing()
