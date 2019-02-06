import FreeCAD

params = FreeCAD.ParamGet('User parameter:Plugins/Furti/Reporting')


def debug():
    return params.GetBool('Debug')


def setupMissingParams():
    if params.GetBool('Debug') is False:
        params.SetBool('Debug', False)
