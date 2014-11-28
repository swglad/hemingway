Write Like Hemingway
=========
Authors: Alex Gerstein, Scott Gladstone, Vikram Narayan

Problem Description and Motivations
-----------
This problem consists of translating input text into text from a given author or
corpus. Our motivation for the project was to come up with a tool that enables anyone to enter input and learn how Hemingway or another famous author would say that input. 

Requirements
------------
1. NLTK
2. NLTK-Data - wordnet
3. NLTK Punkt
4. pattern.en (pip install pattern)

To Install Punkt (+ other NLTK tools)
---------------------------------
* Open Python interpreter
>>> import nltk
>>> nltk.download()
Then an installation window appears. Go to the 'Models' tab and select 'punkt' from under the 'Identifier' column. Then click Download and it will install the necessary files. 

WebApp
------
App: https://damp-peak-7452.herokuapp.com/

Source: https://github.com/alexgerstein/hemingway-web

Command Line
------------
python main.py -a [author] -i [input] -o [output] [no_lesk_mode]

[author]: hemingway, shakespeare, dickens, rappers

[input]: .txt file name

[output]: file name

[no_lesk_node] (optional): '--fast' to run without word-sense disambiguation
