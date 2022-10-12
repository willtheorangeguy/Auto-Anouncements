from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="auto-announcements",
    version="0.2.0",
    description="A bot framework that automatically sends announcements (or any other file) to a specified email address on Saturday night or when the script is run.",
    long_description=readme(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email",
    ],
    keywords="auto announcement email bot cli",
    url="https://github.com/Dog-Face-Development/Auto-Anouncements",
    author="willtheorangeguy",
    entry_points={"console_scripts": ["auto-announcements=send:main"]},
)
