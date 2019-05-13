# Posted at:
# https://stackoverflow.com/a/55741590/5353461 (A to my own Q)
# https://stackoverflow.com/a/55742015/5353461 (A to Q with most upvotes)
# https://stackoverflow.com/a/55741959/5353461 (A to: How to override bad symlink with python)
# https://stackoverflow.com/a/56115053/5353461 racey answer to Q with most upvotes

# https://bugs.python.org/issue36656 (python issue)
# https://code.activestate.com/lists/python-ideas/55992/

import os, tempfile

def symlink(target, link_name, overwrite=False):
    '''
    Create a symbolic link named link_name pointing to target.
    If link_name exists then FileExistsError is raised, unless overwrite=True.
    When trying to overwrite a directory, IsADirectoryError is raised.
    '''

    if not overwrite:
        os.symlink(target, linkname)
        return

    # os.replace() may fail if files are on different filesystems
    link_dir = os.path.dirname(link_name)

    # Create link to target with temporary filename
    while True:
        temp_link_name = tempfile.mktemp(dir=link_dir)

        # os.* functions mimic as closely as possible system functions
        # The POSIX symlink() returns EEXIST if link_name already exists
        # https://pubs.opengroup.org/onlinepubs/9699919799/functions/symlink.html
        try:
            os.symlink(target, temp_link_name)
            break
        except FileExistsError:
            pass

    # Replace link_name with temp_link_name
    try:
        # Pre-empt os.replace on a directory with a nicer message
        if os.path.isdir(link_name):
            raise IsADirectoryError(f"Cannot symlink over existing directory: '{link_name}'")
        os.replace(temp_link_name, link_name)
    except:
        if os.path.islink(temp_link_name):
            os.remove(temp_link_name)
        raise

# # Race condition if link_name must always exist
# def symlink_force(target, link_name):
#     '''
#     Create a symbolic link link_name pointing to target.
#     Overwrites link_name if it exists.
#     '''
#
#     if os.path.isdir(link_name):
#         raise IsADirectoryError(f"Cannot symlink over existing directory: '{link_name}'")
#
#     while True:
#         # os.* functions mimic as closely as possible the underlying system functions
#         # The POSIX symlink() returns EEXIST if link_name already exists
#         # https://pubs.opengroup.org/onlinepubs/9699919799/functions/symlink.html
#         try:
#             os.symlink(target, link_name)
#             break
#         except FileExistsError:
#             os.remove(link_name)
