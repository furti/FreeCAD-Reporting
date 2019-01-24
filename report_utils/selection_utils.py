import FreeCAD
import FreeCADGui


def findSelectedReportConfig():
    selection = FreeCADGui.Selection.getSelection()

    if len(selection) != 1:
        return None

    selectedObject = selection[0]

    if not hasattr(selectedObject, 'Proxy') or selectedObject.Proxy is None:
        return None

    if not hasattr(selectedObject.Proxy, 'statements'):
        return None

    return selection[0].Proxy
