from setuptools import setup, find_packages

setup(
    name="viperlang",
    version="1.0.0",
    description="Viper Programming Language Interpreter",
    author="GSEJ Company",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "viper=viper.__main__:main",
            "vpm=vpm.cli:main"
        ],
    },
    install_requires=[],
    python_requires=">=3.8",
)
