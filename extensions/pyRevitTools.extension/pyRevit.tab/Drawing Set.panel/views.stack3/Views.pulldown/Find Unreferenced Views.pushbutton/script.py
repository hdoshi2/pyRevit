"""Lists views that have not been references by any other view."""

from pyrevit import revit, DB
from pyrevit import script


output = script.get_output()


view_ref_prefixes = {DB.ViewType.CeilingPlan: 'Reflected Ceiling Plan: ',
                     DB.ViewType.FloorPlan: 'Floor Plan: ',
                     DB.ViewType.EngineeringPlan: 'Structural Plan: ',
                     DB.ViewType.DraftingView: 'Drafting View: '}


def find_unrefed_views(view_list):
    for v in view_list:
        phasep = v.LookupParameter('Phase')
        sheetnum = v.LookupParameter('Sheet Number')
        detnum = v.LookupParameter('Detail Number')
        refsheet = v.LookupParameter('Referencing Sheet')
        refviewport = v.LookupParameter('Referencing Detail')
        if refsheet \
                and refviewport \
                and refsheet.AsString() != '' \
                and refviewport.AsString() != '' \
                or (view_ref_prefixes[v.ViewType] + v.ViewName) \
                in view_refs_names:
            continue
        else:
            print('-'*20)
            print('NAME: {0}\nTYPE: {1}\nID: {2}\n'
                  'PLACED ON DETAIL/SHEET: {4} / {3}'
                  .format(v.ViewName,
                          str(v.ViewType).ljust(20),
                          output.linkify(v.Id),
                          sheetnum.AsString() if sheetnum else '-',
                          detnum.AsString() if detnum else '-'
                          )
                  )


views = DB.FilteredElementCollector(revit.doc)\
          .OfCategory(DB.BuiltInCategory.OST_Views)\
          .WhereElementIsNotElementType()\
          .ToElements()

view_refs = DB.FilteredElementCollector(revit.doc)\
              .OfCategory(DB.BuiltInCategory.OST_ReferenceViewer)\
              .WhereElementIsNotElementType()\
              .ToElements()

view_refs_names = set()
for view_ref in view_refs:
    ref_param = view_ref.LookupParameter('Target view')
    view_refs_names.add(ref_param.AsValueString())

dviews = []
mviews = []

for v in views:
    if not v.IsTemplate:
        if v.ViewType == DB.ViewType.DraftingView:
            dviews.append(v)
        else:
            mviews.append(v)

print('UNREFERENCED DRAFTING VIEWS'.ljust(100, '-'))
find_unrefed_views(dviews)
print('\n\n\n' + 'UNREFERENCED MODEL VIEWS'.ljust(100, '-'))
find_unrefed_views(mviews)