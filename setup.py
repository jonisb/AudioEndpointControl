# -*- coding: utf-8 -*-

from setuptools import setup

PKG_NAME = "AudioEndpointControl"

def get_version():
    with open('AudioEndpointControl/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

setup(
    name=PKG_NAME,
    version=get_version(),
    author="jonisb",
    # author_email="",
    # maintainer="",
    # maintainer_email="",
    # license="",
    # url="",

    description="A library to access and control audio devices",
    long_description=(
        " A library to access and control audio devices (Soundcard "
        "speakers/mics) written in Python, no DLLs are needed (at the"
        "moment at least) it communicates directly with Windows Core "
        "Audio Interfaces."
    ),
    packages=[PKG_NAME],
    package_data={
        PKG_NAME: ["mmdeviceapi.tlb"]
    },
)
