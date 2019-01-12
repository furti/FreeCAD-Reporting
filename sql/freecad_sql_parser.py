import FreeCAD
from . import sql_parser

def checkActiveDocument():
    if FreeCAD.ActiveDocument is None:
        raise ValueError("Need an active document to execute a SQL Statement")

def documentObjectsSupplier():
    checkActiveDocument()

    return FreeCAD.ActiveDocument.Objects

def singleObjectSupplier(objectName):
    checkActiveDocument()

    return FreeCAD.ActiveDocument.getObjectsByLabel(objectName)

def newParser():
    return sql_parser.newParser(documentObjectsSupplier, singleObjectSupplier)
