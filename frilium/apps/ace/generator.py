from .applicators import applicators


def generate_ace(roles):
    ace = {}

    for ext, module in applicators.list():
        try:
            ace = module.generat_ace(ace, roles, ext)
        except AttributeError:
            message = f'{ext} has to define generate_ace function'
            raise AttributeError(message)
    return ace
