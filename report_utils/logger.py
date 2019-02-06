from report_utils import preferences


def debug(messagePattern, args=None, compact=True):
    if not preferences.debug():
        return

    if not compact:
        print('\n')

    if args is None:
        print(messagePattern)
    else:
        print(messagePattern % args)
