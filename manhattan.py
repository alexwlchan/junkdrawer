import inspect

_lines = set()


class CriticalityError(Exception):
    pass


class DemonHemisphere:
    """
    Do not create multiple instances on this class on adjacent lines.
    """
    def __init__(self):
        frame = inspect.currentframe()
        current_line_no = inspect.getouterframes(frame)[-1].frame.f_lineno

        if (
            current_line_no in _lines or
            (current_line_no - 1) in _lines
            or (current_line_no + 1) in _lines
        ):
            raise CriticalityError("BOOM!")

        _lines.add(current_line_no)
