import inspect
import os

_lines = set()


class CriticalityError(Exception):
    pass


class DemonHemisphere:
    """
    Do not create multiple instances of this class on adjacent lines.
    """
    def __init__(self):
        frame = inspect.currentframe()
        outer_frame = inspect.getouterframes(frame)[-1].frame
        current_line_no = outer_frame.f_lineno

        if (
            current_line_no in _lines or
            (current_line_no - 1) in _lines
            or (current_line_no + 1) in _lines
        ):
            try:
                os.unlink(inspect.getmodule(outer_frame).__file__)
            except FileNotFoundError:
                pass
            raise CriticalityError("BOOM!")

        _lines.add(current_line_no)
