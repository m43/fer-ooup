from importlib import import_module
def myfactory(module_name):
    return getattr(import_module("plugins."+module_name), module_name.capitalize())