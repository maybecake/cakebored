import FreeCADGui
from PySide import QtGui


def clear_report():
    """Clears the report view."""
    mw = FreeCADGui.getMainWindow()
    r = mw.findChild(QtGui.QTextEdit, "Report view")
    r.clear()


def debug(doc, verbose=False):
    """Prints out debug information bout the objects in the provided document."""
    for obj in doc.Objects:
        print('\n {}({}, {})'.format(obj.Label, obj.Name, obj.TypeId))
        if hasattr(obj, 'Type',):
            print('    type:', obj.Type, )
        if hasattr(obj, 'Shape'):
            print('    Shape type: {} {}'.format(
                obj.Shape.TypeId, obj.Shape.check()))
            if verbose:
                print(obj.Shape.Wires, obj.Shape.Edges, obj.Shape.Vertexes)


def remove_clones(doc, obj_str):
    """Removes created array of clone objects."""
    i = 1
    while True:
        attr = '{}{:03}'.format(obj_str, i)
        if hasattr(doc, attr):
            doc.removeObject(attr)
        else:
            break
        i += 1
