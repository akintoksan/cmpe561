#!/usr/bin/env python

import os
import random
from math import *
import numpy
from scipy.stats import *
import sys
# reload(sys)  
# sys.setdefaultencoding('Cp1254')

count, total_doc_num_training, total_doc_num_testing, avg_len, prob_df = 0, 0, 0, 0, 0

cont_table_for_authors = {}

fp_list = []

total = 0

authors, prob_author, prob_doc_given_class, pdf_author = [], [], [], []
meanAuthor, varianceAuthor = [], []
meanNumWords, varianceNumWords = [], []
word_given_class, lexicon, avg_word_length_doc, author_folder_length = {}, {}, {}, {}
num_of_words_for_doc = {}
training_set = sys.argv[1]
test_set = sys.argv[2]

training_folder = os.listdir(training_set)
test_folder = os.listdir(test_set)

# this method normalizes the given token due to non-alphabetic characters and apostrophe
# (trims only the first and last characters) it also converts the token to
# all-lowercase
def tokenize(token):
	lower = token.lower()
	while lower and not lower[-1].isalpha():
		if len(lower) > 1:
			lower = lower[:-1]
		else:
			lower = ""		
	while lower and not (lower[0].isalpha()):
		if len(lower) > 1:
			lower = lower[1:]
		else:
			lower = ""
	if "\'" in lower:
		lower = lower.split("\'")[0]
	return lower

# 1- this method creates a lexicon and keeps word frequencies for each class
# for the given training set
# 2- also calculates the average word length and number of words for each author
# (with their means and variances for calculating probability density functions)
# 3- lastly, it calculates the class probabilities eg. P("abbasGuclu")
def indexing(training_folder):

	#counting the total number of classes
	for author in training_folder:
		if not author.startswith("."):
			global count
			count += 1
	
	# total appearance is the total number of words in a class
	lexicon["Total Appearance"] = []
	for i in range(0,count):
		lexicon["Total Appearance"].append(0)

	for author in training_folder:
		#eliminating .DS_Store files
		if not author.startswith("."):
			avg_word_length_doc[author] = []
			authors.append(author)
			if training_set.endswith("/"):
				temp_str = training_set + author
			else: 
				temp_str = training_set + "/" + author

			#listing files in an author's folder
			author_folder = os.listdir(temp_str)

			# again eliminating .DS_Store files
			for file in author_folder:
				if not file.endswith(".txt"):
					author_folder.remove(file)

			# this keeps the number of documents in each class
			author_folder_length[author] = len(author_folder)

			# keeps number of words for each class
			num_of_words_for_doc[author] = []

			for article in author_folder:
				global total_doc_num_training
				total_doc_num_training += 1
				total_words = 0
				total_length = 0
				f = open(temp_str + "/" + article)
				line = f.read()
				tokens = line.split()

				# putting each new token in the lexicon, updating the list
				# for the tokens that are already in the lexicon
				for token in tokens: 
					lower = tokenize(token)
					if lower != "":
						total_words += 1
						total_length += len(lower)
						if lower not in lexicon:
							lexicon[lower] = []
							for i in range(0,count):
								lexicon[lower].append(0)

						lexicon[lower][authors.index(author)] += 1
						lexicon["Total Appearance"][authors.index(author)] += 1
				f.close()
				num_of_words_for_doc[author].append(total_words)
				avg_word_length_doc[author].append(float(total_length) / total_words)
			
			#calculating mean and variance for each author in terms of
			# average word length 
			meanAuthor.append(numpy.mean(avg_word_length_doc[author]))
			varianceAuthor.append(numpy.var(avg_word_length_doc[author]))

			#calculating mean and variance for each author in terms of
			# number of words in documents
			meanNumWords.append(numpy.mean(num_of_words_for_doc[author]))
			varianceNumWords.append(numpy.var(num_of_words_for_doc[author]))

	# calculating the class probabilities
	for author in authors:
		prob = float(author_folder_length[author])/float(total_doc_num_training)
		prob_author.append(float(prob))

# this method classifies the documents in the given test set
def testing(test_folder):
	print "List of documents and their guessed authors according to the Naive Bayes:"
	global count
	for i in range(0,count):
		prob_doc_given_class.append(0.0)
		fp_list.append(0)

	for author in test_folder:
		# true positive, false positive, false negative
		tp, fp, fn = 0, 0, 0
		if not author.startswith("."):
			if test_set.endswith("/"):
				temp_str = test_set + author
			else: 
				temp_str = test_set + "/" + author

			author_folder = os.listdir(temp_str)

			for file in author_folder:
				if not file.endswith(".txt"):
					author_folder.remove(file)

			for article in author_folder:
				total_words = 0
				total_length = 0
				global total_doc_num_training
				total_doc_num_training += 1
				for i in range(0,count):
					prob_doc_given_class[i] = 0.0

				f = open(temp_str + "/" + article)
				line = f.read()
				tokens = line.split()

				prob_word_given_class = 0

				for token in tokens:
					lower = tokenize(token)
					if lower != "":
						total_words += 1
						total_length += len(token)
						if lower in lexicon:
							for i in range(0, count):
								#calculating naive bayes with alpha = 0.025
								dividend = (lexicon[lower][i]+0.025)
								denominator = lexicon["Total Appearance"][i]+0.025*len(lexicon)
								prob_word_given_class = float(log(float(dividend)/denominator))
								prob_doc_given_class[i] += prob_word_given_class

				avg_len = float(total_length) / total_words

				# calculating probability density function (pdf) 
				# for average word length
				tmp_mean = meanAuthor[authors.index(author)]				
				tmp_var = varianceAuthor[authors.index(author)]
				tmp_base = 1/sqrt(2*pi*tmp_var)
				tmp_pow = -((avg_len-tmp_mean)**2)/(2*tmp_var)
				prob_df = tmp_base*exp(tmp_pow)
				
				# calculating probability density function (pdf) 
				# for number of words
				tmp_mean2 = meanNumWords[authors.index(author)]
				tmp_var2 = varianceNumWords[authors.index(author)]
				tmp_base2 = 1/sqrt(2*pi*tmp_var2)
				tmp_pow2 = -((total_words-tmp_mean2)**2)/(2*tmp_var2)
				prob_df2 = tmp_base2*exp(tmp_pow2)
				
				# weighted overall probability for a document given class
				prob_doc_given_class[authors.index(author)] = 0.8*(prob_doc_given_class[authors.index(author)] + float(log(prob_author[authors.index(author)]))) + 0.1*(float(log(prob_df2))) + 0.1*(float(log(prob_df)))

				f.close()

				# guessing the author according the maximum probability
				guessed_author = authors[prob_doc_given_class.index(max(prob_doc_given_class))]
				print author + "/" + article  + " ---> " + guessed_author
				#print

				if author == guessed_author:
					tp += 1
				else: 
					fn += 1
					fp_list[authors.index(guessed_author)] += 1


			cont_table_for_authors[author] = [tp, fn]
			global total 
			total += tp
			
	macro_avg_precision, macro_avg_recall, micro_avg_precision, micro_avg_recall, \
	macro_avg_fscore, micro_avg_fscore = 0, 0, 0, 0, 0, 0
	
	total_tp, total_fp, total_fn = 0, 0, 0

	# calculating the macro and micro average values (precisions, recalls, f-scores)
	for key in cont_table_for_authors:
		tp = cont_table_for_authors[key][0]
		fp = fp_list[authors.index(key)]
		fn = cont_table_for_authors[key][1]
		if (tp + fp) != 0:
			macro_avg_precision = macro_avg_precision + (tp / (tp + fp))

		macro_avg_recall += tp / (tp + fn)

		total_tp += tp
		total_fp += fp
		total_fn += fn
	
	macro_avg_precision = float(macro_avg_precision) / count
	macro_avg_recall = float(macro_avg_recall) / count

	micro_avg_precision = float(total_tp) / (total_tp + total_fp)
	micro_avg_recall = float(total_tp) / (total_tp + total_fn)

	if (macro_avg_precision + macro_avg_recall) != 0:
		macro_avg_fscore = float(2*macro_avg_precision*macro_avg_recall)/(macro_avg_precision+macro_avg_recall)
	if (micro_avg_precision + micro_avg_recall) != 0:
		micro_avg_fscore = float(2*micro_avg_precision*micro_avg_recall)/(micro_avg_precision+micro_avg_recall)

	print
	print "Macro Average Precision: " + str(macro_avg_precision)
	print "Macro Average Recall: " + str(macro_avg_recall)
	print "Macro Average F-score: " + str(macro_avg_fscore)
	print
	print "Micro Average Precision: " + str(micro_avg_precision)
	print "Micro Average Recall: " + str(micro_avg_recall)
	print "Micro Average F-score: " + str(micro_avg_fscore)

indexing(training_folder)
testing(test_folder)










