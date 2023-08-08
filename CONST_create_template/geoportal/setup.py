#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="geoserver_gmf_geoportal",
    version="1.0",
    description="geoserver_gmf, a c2cgeoportal project",
    author="geoserver_gmf",
    author_email="info@geoserver_gmf.com",
    url="https://www.geoserver_gmf.com/",
    install_requires=[
        "c2cgeoportal_geoportal",
        "c2cgeoportal_admin",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "paste.app_factory": [
            "main = geoserver_gmf_geoportal:main",
        ],
        "console_scripts": [],
    },
)
