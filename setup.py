from setuptools import find_packages, setup

# ARGUMENTS FOR SETUP EXPLAINED
#   name                    --> Self explanatory
#   version                 --> Self explanatory
#   packages                --> Tells Python what package directories (and the Python files they contain) to include
#   find_packages()         --> Finds package directories automatically so you don’t have to type them out
#   include_package_data    --> Set this to include other files, such as the static and templates directories
#   MANIFEST.in             --> Python needs this file to determine what this other data (static/template) is
#   zip_safe                --> Can the package be run directly from a ZIP file? If so than we set this to True
#   install_requires        --> Similar to requirements.txt... doesn't tell the user what they need for Python env.
#
#       NOTE:       Our MANIFEST.in file tells Python to copy the static & templates dirs, & the schema.sql file,
#                   but exclude all bytecode files.
setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
