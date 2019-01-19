DEBUG = True


def debug(messagePattern, args=None):
    if not DEBUG:
        return

    print('\n')

    if args is None:
        print(messagePattern)
    else:
        print(messagePattern % args)
