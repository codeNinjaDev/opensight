import importlib
import inspect
import os.path
import sys
from typing import Dict, List, Tuple, Type

from .manager_schema import Function, ModuleInfo, ModuleItem, ModulePath, isfunction


def import_module(path: ModulePath):
    # So this sometimes doesn't work if the module name also exists in site-packages
    # But I don't understand exactly when and why this happens

    """
    path_bak = sys.path[:]
    try:
        sys.path.insert(0, os.path.abspath(path.path))
        return importlib.import_module(path.name)
    finally:
        sys.path = path_bak[:]
    """

    # Workaround for now: only allow import .py file, not full package

    full_path = os.path.abspath(os.path.join(path.path, path.name + ".py"))

    # https://docs.python.org/3.7/library/importlib.html#importing-a-source-file-directly

    spec = importlib.util.spec_from_file_location(path.name, full_path)
    module = importlib.util.module_from_spec(spec)

    # This will break if the standard library package is imported, I think?
    # But it's necessary for inspect.getmodule to work
    sys.modules[path.name] = module

    spec.loader.exec_module(module)

    return module


class Manager:
    def __init__(self):
        self.modules: Dict[str, ModuleItem] = {}
        self.funcs: Dict[str, Type[Function]] = {}

    @classmethod
    def is_valid_function(cls, module):
        def closure(func):
            # Todo: are there any other times we don't want to register a Function?
            # This is important because the default is registering every single Function
            return (
                isfunction(func)
                and (not func.disabled)
                # If a module imports a Function from another module, do not register that Function
                and (inspect.getmodule(func) == module)
            )

        return closure

    @classmethod
    def get_module_info(cls, module):
        # Generate ModuleInfo from global variables in a module, with fallbacks

        package = getattr(module, "__package__", module.__name__)
        version = getattr(module, "__version__", "1.0")

        return ModuleInfo(package, version)

    def register_module(self, path: ModulePath):
        module = import_module(path)
        info = Manager.get_module_info(module)

        funcs_tuple: List[Tuple[str, Type[Function]]]
        funcs_tuple = inspect.getmembers(module, Manager.is_valid_function(module))

        if len(funcs_tuple) == 0:
            # Todo: error, return value?
            print(f"No Functions found in module {path}")
            return

        funcs: Dict[str, Type[Function]] = {}

        for name, func in funcs_tuple:
            func.type = info.package + "/" + name

            funcs[name] = func
            self.funcs[func.type] = func

        self.modules[info.package] = ModuleItem(info, funcs)
