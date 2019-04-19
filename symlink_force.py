import os, tempfile, time

def symlink_force(target, link_name):
    '''
    Create a symbolic link pointing to target named link_name.
    Overwrite target if it exists.
    '''
    # Posted at:
    # https://stackoverflow.com/a/55741590/5353461 (A to my own Q)
    # https://stackoverflow.com/a/55742015/5353461 (A to Q with most upvotes)
    # https://stackoverflow.com/a/55741959/5353461 (A to: How to override bad symlink with python)

    # Possible race condition between temp link creation and overwriting link_name
    # https://bugs.python.org/issue36656 (python issue)

    # os.replace may fail if files are on different filesystems.
    # Therefore, use the directory of target
    link_dir = os.path.dirname(target)

    # os.symlink requires that the target does NOT exist.
    # Avoid race condition of file creation between mktemp and symlink:
    while True:
        temp_pathname = tempfile.mktemp(suffix='.tmp', \
                        prefix='symlink_force_tmp-', dir=link_dir)
        try:
            os.symlink(target, temp_pathname)
            break  # Success, exit loop
        except FileExistsError:
            time.sleep(0.001)  # Prevent high load in pathological conditions
        except:
            raise
    os.replace(temp_pathname, link_name)
