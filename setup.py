from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pygame-golf",
    version="1.0.0",
    author="Ziad Elhusiny",
    author_email="ziad.elhusiny@gmail.com",
    description="A physics-based golf game with 10 levels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zezo386/pygame-golf",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pygame>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "pygame-golf=main:main",
        ],
    },
)