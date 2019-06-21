#!/usr/bin/env python
# -*- encoding: utf-8

# https://twitter.com/ticky/status/1141370988820480001

import inspect


def self_deprecating(*args, **kwargs):
    print("Called self_deprecating with %r, %r" % (args, kwargs))

    with open(__file__) as self_file:
        source_lines = self_file.readlines()

    name_of_this_function = inspect.stack()[0].function

    matching_lines = [
        idx
        for idx, line in enumerate(source_lines)
        if line.startswith("def %s(" % name_of_this_function)
    ]
    assert len(matching_lines) == 1
    first_line_of_function = matching_lines[0]

    if "warnings.warn" in source_lines[first_line_of_function + 1].strip():
        return
    else:
        source_lines.insert(
            first_line_of_function + 1,
            '    import warnings; '
            'warnings.warn('
            '"The self_deprecating function is deprecated", DeprecationWarning)\n'
        )

    with open(__file__, "w") as self_file:
        self_file.write("".join(source_lines))


if __name__ == "__main__":
    self_deprecating("hello", "ticky")
    import s
    self_deprecating = s.self_deprecating
    self_deprecating("hello", "alex")
