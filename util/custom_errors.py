class TelebotInputError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'TelebotInputError, {0} '.format(self.message)
        else:
            return 'TelebotInputError has been raised'