#!/usr/bin/env python
"""
Package metadata for openedx_ltistore
"""
from gettext import find
from importlib.metadata import entry_points
import os
import re
import sys

from setuptools import setup, find_packages


def get_version(*file_paths):
    """
    Extract the version string from the file.

    Input:
     - file_paths: relative path fragments to file with
                   version string
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split("#")[0].strip()
            for line in open(path).readlines()
            if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.

    Returns:
        bool: True if the line is not blank, a comment, a URL, or
              an included file
    """
    return line and not line.startswith(("-r", "#", "-e", "git+", "-c"))


VERSION = get_version("lti_store", "__init__.py")

if sys.argv[-1] == "tag":
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
CHANGELOG = open(os.path.join(os.path.dirname(__file__), "CHANGELOG.md")).read()

setup(
    name="openedx-ltistore",
    version=VERSION,
    description="""An app for storing LTI provider configurations centrally.""",
    long_description=README + "\n\n" + CHANGELOG,
    author="edX",
    author_email="oscm@edx.org",
    url="https://github.com/openedx/openedx-ltistore",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django"],
    python_requires=">=3.8",
    license="AGPL 3.0",
    zip_safe=False,
    keywords="Python edx",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        "lms.djangoapp": [
            "lti_store = lti_store.apps:LtiStoreConfig",
        ],
        "cms.djangoapp": [
            "lti_store = lti_store.apps:LtiStoreConfig",
        ],
    }
)
