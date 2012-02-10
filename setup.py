# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import re
from setuptools import setup, find_packages

install_requires = ['SQLALchemy<=0.6.99', 'PasteDeploy', 'WebOb', 'Mako',
                    'recaptcha-client', 'Routes', 'simplejson',
                    'Services>=2.0', 'cef']

# extracting the version number from the .spec file
here = os.path.dirname(__file__)
spec = os.path.join(here, 'SyncReg.spec')
with open(spec) as f:
    spec = f.read()

_VERSION = re.compile('^%define version (.*)$', re.M)
version = _VERSION.findall(spec)[0]

entry_points = """
[paste.app_factory]
main = syncreg.wsgiapp:make_app

[paste.app_install]
main = paste.script.appinstall:Installer
"""


setup(name='SyncReg',
      version=version,
      packages=find_packages(),
      install_requires=install_requires,
      entry_points=entry_points,
      license='MPLv2.0',
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        ],
      package_data={'syncreg': ['templates/*.mako']}
)
