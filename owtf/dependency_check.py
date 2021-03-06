"""
owtf.dependency_check
~~~~~~~~~~~~~~~~~~~~~

This is the script which checks the owtf pip dependencies before loading the framework
"""

import os
import uuid

try:
    # Is pip even there?
    import pip
    # We do this in order to check for really old versions of pip
    pip.get_installed_distributions()
except ImportError:
    print("We recommend you run install script before launching OWTF for first time")
    print("\t\t\tpython2 install/install.py")
    exit(1)


def is_present(module_name):
    """Checks if module can be imported

    :param module_name: Name of the module to import
    :type module_name: `str`
    :return: True or False based on whether module can be imported
    :rtype: `boolean`
    """
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


def verify_dependencies(root_dir):
    """Goes over the requirements file, parses it and checks if all requirements are satisfied

    :param root_dir: Root directory for OWTF
    :type root_dir: `str`
    :return:
    :rtype: None
    """
    # Get all the installed libraries
    # installed_libraries = {"tornado": "version"}
    installed_libraries = dict((i.project_name, i.version) for i in pip.get_installed_distributions())

    # Get all the libraries required by owtf
    # owtf_libraries = ["tornado", "lxml"...]
    owtf_reqs = pip.req.parse_requirements(os.path.join(root_dir, "install", "owtf.pip"), session=uuid.uuid1())
    owtf_libraries = [req.req.name for req in owtf_reqs]

    # Iterate over requirements and check if existed
    missing_libraries = []
    for library_name in owtf_libraries:
        if library_name not in list(installed_libraries.keys()):
            # Check if the module is installed via package manager
            if not is_present(library_name):
                missing_libraries.append(library_name)

    # If there are missing libraries bail out :P
    if len(missing_libraries) > 0:
        print("The following python libraries seem missing : ")
        print("\t%s\n" % (','.join(missing_libraries)))
        print("Haven't you run the install script? ")
        print("\t%s\n" % ("python2 install/install.py"))
        print("If you are sure you ran the install script, install the missing libraries seperately")
        print("\t%s\n" % ("pip install --upgrade -r install/owtf.pip"))
        exit(1)
