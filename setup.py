from setuptools import find_packages, setup

MAJOR_VERSION = "0"
MINOR_VERSION = "0"
MICRO_VERSION = "1"
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)


setup(
    name="clidoro",
    packages=find_packages(exclude=["docs", "tests*", "examples"]),
    version=VERSION,
    license="MIT",
    zip_safe=False,
    platforms="Linux",
    description="clidoro: pomodoro in your cli",
    long_description_content_type="text/markdown",
    url="https://github.com/kingjuno/clidoro",
    entry_points={"console_scripts": ["clidoro = clidoro.clidoro:main"]},
    keywords=["Productivity", "Pomodoro"],
    install_requires=["playsound", "alive-progress", "simple-term-menu"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: System Administrators",
        "Operating System :: Unix",
        # TODO: Add Windows support
        # TODO: Add Mac support
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)
