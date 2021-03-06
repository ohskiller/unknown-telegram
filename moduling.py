# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import importlib
import logging
import os


class Module():
    def __init__(self):
        self.name = "Unknown"


def get_modules_py(folder):
    res = []
    files = []
    try:
        files = os.listdir(folder)
    except:
        return []
    for f in files:
        if f == "__init__.py":
            continue
        mod_name, ext = os.path.splitext(f)
        if ext == ".py":
            try:
                res.append(importlib.import_module(
                    "{}.{}".format(folder, mod_name)))
            except Exception as e:
                logging.error(
                    "Can't load module '{}': '{}'.".format(mod_name, e))
    return res


def get_modules(mods_py, db):
    modules = []
    for mod in mods_py:
        attr = None
        try:
            attr = mod.__getattribute__("Module")
        except BaseException:
            logging.warning(
                "Module {} does not have a 'Module' class.".format(
                    mod.__name__))
            continue
        kind = attr.__class__.__name__
        if kind == "type":
            if not issubclass(attr, Module):
                continue
            _mod = attr()
            _mod.commands = {}
            _mod.incoming_handler = None
            _mod.db = db.table("module_" + os.path.basename(mod.__file__)[:-3])
            for i in dir(_mod):
                if i.startswith("__") and i.endswith("__"):
                    continue
                if i.endswith("cmd") or i == "incoming":
                    _attr = getattr(_mod, i)
                    if _attr.__class__.__name__ == "method":
                        if i.endswith("cmd"):
                            _mod.commands[i[:-3]] = _attr
                        else:
                            _mod.incoming_handler = _attr
            logging.info("Loaded module '{}'.".format(_mod.name))
            modules.append(_mod)
    return modules
