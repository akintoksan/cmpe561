#!/usr/bin/env python
from shutil import *
import os
import random
import sys

authors = []
training_set, test_set = {}, {}

src_dataset = sys.argv[1]
dest_training = sys.argv[2]
dest_test = sys.argv[3]

src_folder = os.listdir(src_dataset)


# dataset_builder classifies 

def file_creator(dataset, dest_set): 
	for author in dataset:
		if dest_set.endswith("/"):
			author_directory = dest_set + author
		else:
			author_directory = dest_set + "/" + author
	
		if not os.path.exists(author_directory):
			os.makedirs(author_directory)
			for i in range(0, len(dataset[author])):
				if src_dataset.endswith("/"):
					file_path = src_dataset + author + "/" + dataset[author][i]
				else:
					file_path = src_dataset + "/" + author + "/" + dataset[author][i]

				copy(file_path, author_directory)

def builder(src_folder, dest_training, dest_test):
	if not os.path.exists(dest_training) and not os.path.exists(dest_test) :
		os.makedirs(dest_training)	
		os.makedirs(dest_test)

		for author in src_folder:
			if not author.startswith("."):
				authors.append(author)
				if src_dataset.endswith("/"):
					temp_str = src_dataset + author
				else: 
					temp_str = src_dataset + "/" + author

				author_folder = os.listdir(temp_str)

				for file in author_folder:
					if not file.endswith(".txt"):
						author_folder.remove(file)

				training_set[author] = []
				num_of_doc = len(author_folder)

				for i in range(0, int(num_of_doc*0.6)):
					text = random.choice(author_folder)
					training_set[author].append(text)
					author_folder.remove(text)

				test_set[author] = author_folder
		
			file_creator(training_set, dest_training)
			file_creator(test_set, dest_test)
		print
		print "Training set (" + dest_training + ") and test set (" + dest_test + ") have been created"
		print
	else: 
		print
		print "Seems like you've already created the training and test sets in these directories."
		print "Please delete those folders before you create a new dataset in the same directory with the same names."
		print "You can then re-run the program."
		print

builder(src_folder, dest_training, dest_test)
