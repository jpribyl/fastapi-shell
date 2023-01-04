import argparse
import asyncio
import importlib
import importlib.util
import logging
import re
from glob import glob
from typing import List, Optional, Set

from genericpath import isfile
from IPython.terminal import embed
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import HasFocus, ViInsertMode
from prompt_toolkit.key_binding.vi_state import InputMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_module(filename: str):
    return isfile(filename) and not filename.endswith("__init__.py")


def import_modules(
    path_glob: str,
    excluded_modules: Optional[Set[str]] = None,
):
    module_files = filter(is_module, glob(path_glob, recursive=True))
    selected_files = filter(
        lambda f: not any(re.search(i, f) for i in excluded_modules or []),
        module_files,
    )

    for module_file in selected_files:
        module_name = module_file.replace(".py", "").replace("/", ".")
        module = importlib.import_module(module_name)
        prefix = module_name.split(".")[-1]
        logger.info(f"import {module_name} as {prefix}")
        globals().update({prefix: module})


def switch_to_navigation_mode(event):
    event.cli.vi_state.input_mode = InputMode.NAVIGATION


async def shell(
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    run_code: Optional[str] = None,
):
    excluded_modules = set(exclude or [])
    for path_glob in include or ["**/*.py"]:
        import_modules(
            path_glob=path_glob,
            excluded_modules=excluded_modules,
        )

    terminal = embed.InteractiveShellEmbed(colors="neutral")
    terminal.extension_manager.load_extension("autoreload")  # type: ignore
    terminal.events.register('post_run_cell', lambda: terminal.user_global_ns.update(terminal.user_ns))

    terminal.editing_mode = "vi"
    terminal.pt_app.key_bindings.add_binding(  # type: ignore
        "j", "k", filter=(HasFocus(DEFAULT_BUFFER) & ViInsertMode())
    )(switch_to_navigation_mode)

    terminal.run_line_magic("autoreload", "2")

    if run_code:
        await terminal.run_code(run_code)

    return terminal


p = argparse.ArgumentParser()
p.add_argument("--include", nargs="+", default=None)
p.add_argument("--exclude", nargs="+", default=None)
p.add_argument("--run-code", default=None)
args = p.parse_args()
loop = asyncio.new_event_loop()
terminal = loop.run_until_complete(shell(**vars(args)))
terminal.mainloop()
