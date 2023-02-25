from setuptools import find_packages, setup

setup(
    name="hackernews",
    packages=find_packages(exclude=["hackernews_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
