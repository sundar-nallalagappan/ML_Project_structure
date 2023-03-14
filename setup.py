#To make the application as a package

#Requirements
from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str)->List[str]:
    requirements_list = []
    
    with open("requirements.txt") as f:
        requirements_list = f.readlines()

    requirements_list = [req.replace("\n", "") for req in requirements_list]
    print(requirements_list)

    if HYPHEN_E_DOT in requirements_list:
        requirements_list.remove(HYPHEN_E_DOT)
        
    return requirements_list

setup(
name = "ML_Project_structure",
version = "0.0.1",
description = "ML Project structure",
author = "Sundar",
author_email="nsundar.1990@gmail.com",
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)

# find_packages tries to find the folders with __init__.py (For ex: src)
# such folders are considered as packages and tries to build the same. so this can be imported in the application flow
