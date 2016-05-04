#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

test_blind_file = sys.argv[1]
output_file = sys.argv[2]

transition_matrix = {}
likelihood_matrix = {}
tags = []
unknown = ""
unknown_words = []

#reading the transition matrix info from file
with open("transition.txt") as f:
    content = f.readlines()

#reading the likelihood matrix info from file
with open("likelihood.txt") as f2:
    content2 = f2.readlines()

#reading the list of tags, most common tag and tagset type from file
with open("tag_order.txt") as f3:
	content3 = f3.readlines()

with open(test_blind_file) as f4:
    content4 = f4.readlines()

#filling the transition matrix 
for i in range(0, len(content)):
	line = content[i].split()
	if line:
		transition_matrix[line[0]] = {}
		for j in range(1, len(line)):
 			if j%2 == 1:
 				transition_matrix[line[0]][line[j]] = float(line[j+1])

#filling the likelihood matrix
for i in range(0, len(content2)):
	line2 = content2[i].split()
	if line2:
		likelihood_matrix[line2[0]] = []
		for j in range(1, len(line2)):
 			likelihood_matrix[line2[0]].append(float(line2[j]))

#getting the tag list
tag_line = content3[0].split()
for i in range(0, len(tag_line)):
	tags.append(tag_line[i])

#assigning the unknown words with the most common tag
tag_line2 = content3[1].split()
unknown = tag_line2[0]

word = ""
stem = ""
tag = ""
prev_tag = ""
current_tag = ""
count = 1

prob1 = 0.0
prob2 = 0.0


#viterbi algorithm
output_txt = open(output_file, 'w')
for i in range(0, len(content4)):
	line4 = content4[i].split()
	if line4:
		if line4[1] != "_":
			word = line4[1]
			if line4[2] != "_":
				stem = line4[2]
		else:
			if line4[2] != "_":
				stem = line4[2]
				word = ""

		if word != "":
			prob_result = []
			if count == 1:
				prev_tag = "Start"
			else: 
				prev_tag = current_tag

			if stem in likelihood_matrix:
				for i in range(0, len(likelihood_matrix[stem])):
					prob1 = likelihood_matrix[stem][i]
					prob2 = transition_matrix[prev_tag][tags[i]]
					prob_result.append(prob1*prob2)

				max_prob = 0
				max_index = 0
				for i in range(0, len(prob_result)):
					if prob_result[i] > max_prob:
						max_prob = prob_result[i]
						max_index = i

				current_tag = tags[max_index]
			else: 
				current_tag = unknown
				if stem not in unknown_words:
					unknown_words.append(stem)

			output_txt.write(word + "|" + current_tag + "\n")
			
			count += 1
	else: 
		count = 1
		output_txt.write("\n")

#writing the list of unknown words into a file so that we can calculate accuracies later
file_likelihood = open("unknown_words.txt", 'w')
for i in range(0, len(unknown_words)):
	file_likelihood.write(unknown_words[i] + " ");
file_likelihood.close()

