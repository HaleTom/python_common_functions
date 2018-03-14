# Print the function call, the class, str representation, line and filename

# From https://stackoverflow.com/a/8856387/5353461
def describe(arg):
    frame = inspect.currentframe()
    callerframeinfo = inspect.getframeinfo(frame.f_back)
    try:
        context = inspect.getframeinfo(frame.f_back).code_context
        caller_lines = ''.join([line.strip() for line in context])
        m = re.search(r'describe\s*\((.+?)\)$', caller_lines)
        if m:
            caller_lines = m.group(1)
            print(caller_lines)
            position = str(callerframeinfo.filename) + "@" + str(callerframeinfo.lineno)
            print("describe(" + caller_lines + ") = " + arg.__class__.__name__ + "(" + str(arg) + ")", position)
        else:
            print("Describe: couldn't find caller context")

    finally:
        del frame
        del callerframeinfo

