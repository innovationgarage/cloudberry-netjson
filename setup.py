#!/usr/bin/env python

import setuptools

setuptools.setup(name='cloudberry-netjson',
      version='0.1.1',
      description='Cloudberry netjson extensions',
      author='Egil Moeller',
      author_email='egil@innovationgarage.no',
      url='https://github.com/innovationgarage/cloudberry-netjson',
      packages=setuptools.find_packages(),
      install_requires=[
          "requests",
          "netjsonconfig"
      ],
      include_package_data=True
  )
