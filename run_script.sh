#!/bin/sh

# Create virtual env
# https://docs.python.org/3/library/venv.html
python -m venv task-env

# Activate the venv
. task-env/bin/activate

# Upgrade Python pip
pip install --upgrade pip

# Install python required libs
pip install -r requirements.txt

# python
# nltk.download('stopwords')
# nltk.download('punkt')
# exit()

python relevance.py