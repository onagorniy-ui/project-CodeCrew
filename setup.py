from setuptools import setup, find_packages

setup(
    name="nora-assistant",
    version="1.1.2",
    description="NORA - персональний помічник IT-рекрутера",
    author="CodeCrew",
    license="MIT",
    packages=find_packages(),
    py_modules=["Main", "classes", "commands", "storage", "tests"],
    install_requires=[
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "nora = Main:main",
        ]
    },
)
