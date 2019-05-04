# Print the line and filename, function call, the class, str representation and some other info

# Inspired by https://stackoverflow.com/a/8856387/5353461

import inspect
import re

def describe(arg):
    frame = inspect.currentframe()
    callerframeinfo = inspect.getframeinfo(frame.f_back)
    try:
        context = inspect.getframeinfo(frame.f_back).code_context
        caller_lines = ''.join([line.strip() for line in context])
        m = re.search(r'describe\s*\((.+?)\)$', caller_lines)
        if m:
            caller_lines = m.group(1)
            position = str(callerframeinfo.filename) + "@" + str(callerframeinfo.lineno)

            # Add additional info such as shape, length, datatype
            additional = []

            if hasattr(arg, "dtype"):
                additional.append("{}".format(arg.dtype))

            additional.append(type(arg).__qualname__)

            if hasattr(arg, "shape"):
                additional.append("shape={}".format(tuple(t.shape)))
            elif hasattr(arg, "__len__"):  # shape includes length information
                additional.append("[len={}]".format(len(arg)))

            # Use str() representation if it is printable
            str_arg = str(arg)
            str_arg = str_arg if str_arg.isprintable() else repr(arg)

            print(position, "describe(" + caller_lines + ") = ", end='')
            print(" ".join(additional) + " ", end='')
            if "\n" in str_arg; print()  # It's multi-line, line up arrays
            print(str_arg)
        else:
            print("Describe: couldn't find caller context")

    finally:
        del frame
        del callerframeinfo

#
# import numpy
#
# describe((3, 2))
# describe(numpy.zeros((2, 4)))
# describe("fo\\o\n")
# describe('foo' + 'bar')
# describe(5/2)
