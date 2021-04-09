import sys
import traceback
from pathlib import Path
from typing import List

from clint.textui import colored
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters.terminal256 import TerminalTrueColorFormatter

lexer = PythonLexer()
formatter = TerminalTrueColorFormatter()


def render_exception(type, value, tb):
    return render_stack(traceback.format_exception(type, value, tb))


def render_stack(frames: List[str]) -> str:
    highlighted_frames = []
    modified_chunk = []
    for frame in frames:
        handled = False
        try:
            location, code = frame.splitlines(keepends=True)
        except ValueError:
            pass
        else:
            # Highlight the stack frame if it is in first-party code.
            # Red file path and syntax-highlighted code.
            virtualenv_path = Path(sys.executable).parent.parent
            if str(virtualenv_path) not in location:
                location = colored.red(location)
                code = highlight(code, lexer, formatter)
                modified_chunk.append(f"{location}{code}")
                handled = True
        if not handled:
            if modified_chunk:
                highlighted_frames.append("\n" + "\n".join(modified_chunk) + "\n")
                modified_chunk = []
            highlighted_frames.append(frame)
    # Highlight the exception code line itself in red, despite the fact that it
    # may be in third-party code.
    if highlighted_frames:
        exception_frame = highlighted_frames[-1]
        try:
            location, code = exception_frame.splitlines(keepends=True)
        except ValueError:
            pass
        else:
            code = colored.red(code, bold=True)
            highlighted_frames[-1] = f"{location}{code}"
    return "".join(highlighted_frames)


def _handle_exception(type, value, tb):
    print(render_exception(type, value, tb))


def patch_exception_handler():
    sys.excepthook = _handle_exception
