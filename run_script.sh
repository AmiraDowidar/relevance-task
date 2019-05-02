#!/bin/sh

# Create virtual env
# https://docs.python.org/3/library/venv.html
python3 -m venv venv

# Activate the venv
. venv/bin/activate

# Upgrade Python pip
pip3 install --upgrade pip

# Install python required libs
pip3 install -r requirements.txt

# Install nltk libs 
python3
nltk.download('stopwords')
nltk.download('punkt')
exit()

python3 relevance.py