# Get a package's version as a string
# https://stackoverflow.com/a/32965521/5353461
def package_version(package_name):
    import pkg_resources
    return pkg_resources.get_distribution(package_name).version
