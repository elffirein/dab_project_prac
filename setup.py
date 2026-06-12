from setuptools import setup, find_packages

setup(
    name='dab_project_prac',
    version='0.0.2',
    description="This contains the code in ./src directory of the project",
    packages=find_packages(where="./src"),
    package_dir={"": "./src"},
    install_requires=["setuptools"],
    entry_points={
        'packages': [
            "main=dab_project_prac.main:main"
        ]
    }
)
