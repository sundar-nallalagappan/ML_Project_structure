      
End to End Machine Learning Project

1) Create virtual environment within the project folder
    conda create -p venv python==3.8 -y

2) Create .gitignore file in github

3) Create README.md in VS

4) Create requirements.txt - to list the packages used in the project
   -e .   :: This is to trigger the setup.py which in turn considers the folders with __init__.py file as package and builds the same

5) create setup.py :: Responsible for creating the ML application as a package (package ex: matplotlib, seaborn). Note: Packages can be deployed in PyPi for global use

6) Folder Src --> will have the actual project code

7) src/components - have individual python files for data ingesttion, transformation & model