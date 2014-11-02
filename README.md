Write Like Hemingway
=========
Authors: Alex Gerstein, Scott Gladstone, Vikram Narayan

Problem Description and Motivations
-----------
This problem consists of translating input text into text from a given author or
corpus. Our motivation for the project was to come up with a tool that enables anyone to enter input and learn how Hemingway or another famous author would say that input. 

Survey of Existing Work/Work Already Completed
--------------
We have started preliminary background research on writing style imitation. Our research has uncovered previous approaches to translating between writing styles. Sites like LINGOJAM allow users to create manual word/phrase mappings to convert text between authorial styles. For our project, we hope to automate this mapping process. Misha Denil’s “Structured Nonsense: Automatic Imitation of Writing Style” presents an automated system to generate nonsense sentences in a specified style. The article provides a system architecture to add context to given text, which will prove useful when we try to solve the issue of word sense disambiguation for Milestone 2.
To approach word sense disambiguation, we looked into the Lesk algorithm and how to integrate this with WordNet. This approach has been taken before, as written in Santanjeev Banerjee’s “Adapting the Lesk Algorithm for Word Sense Disambiguation to WordNet.”

Proposed Solution Description
-----------------
Our basic model is as follows:

1. Read in a corpus X from author (e.g. Hemingway)
2. For each word w in corpus X:
3.    >   Increment count of w in dict thesaurus
4.    >   Look up all synonyms of w in WordNet
5.    >   Map all synonyms of w to thesaurus[w]
6. Read in a user input Y
7. For each word y in input Y:
8.    >   If y is in thesarus:
9.        >   Use pdf to map y --> synonym(y)

After developing this basic model, we will embellish it by adding word sense disambiguation, and part of speech tagging. For data, we will use corpuses from a couple different authors, including Hemingway. In terms of tools, we plan to use WordNet, a software that maps words to their synonyms, and Stanford’s part of speech tagger. 

Responsibilities of Each Team Member
-----------------------
Alex: Write the functions to create a dictionary by parsing a corpus and look up the synonyms for each word

Scott: Translate input into output using dictionary

Vikram: Word sense disambiguation (Lesk algorithm)

Everyone: Part of speech tagging, GUI 

Milestones
-------------
We plan to first implement the basic model described above (milestone 1), and then embellish it with features such as word sense disambiguation/part of speech recognition (milestone 2), and then add a user interface (milestone 3). By November 5, we will have completed milestone 1. The minimum outcome by the final submission date is a prototype that replaces words, similar to the English to Shakespearean generator mentioned above. It would be a command line interface. Our ideal outcome would include: (a) the minimum outcome previously described, (b) the minimum outcome embellished with word sense disambiguation, and (c) a graphical user interface.
