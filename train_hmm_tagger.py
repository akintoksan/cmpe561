#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

training_file = sys.argv[1]
postag = sys.argv[2]

tagset = 0
if postag == "cpostag":
	tagset = 3
elif postag == "postag":
	tagset = 4
else:
	print
	print "ERROR: Second argument should be either \"cpostag\" or \"postag\""
	print
	sys.exit()

likelihood_matrix = {}
transition_matrix = {}
tags = []
temp = 0
total_tags = {}
unknown = ""

with open(training_file) as f:
    content = f.readlines()

for i in range(0, len(content)):
	line_array = content[i].split()
	if line_array:
		if not (line_array[tagset] in tags):
			tags.append(line_array[tagset])

transition_matrix["Start"] = {}
for i in range(0, len(tags)):
	transition_matrix[tags[i]] = {}

#constructing the likelihood matrix
for i in range(0, len(content)):
	line_array = content[i].split()
	if line_array:
		if not ((line_array[2] in likelihood_matrix) and (line_array[2] != "_")):
			likelihood_matrix[line_array[2]] = []
			for j in range(0, len(tags)):
				likelihood_matrix[line_array[2]].append(0)

		likelihood_matrix[line_array[2]][tags.index(line_array[tagset])] += 1
		count = i + 1
		line_array2 = content[count].split()
		if line_array2 and line_array2[2] == "_":
			while line_array2[2] == "_":
				likelihood_matrix[line_array[2]][tags.index(line_array2[tagset])] += 1
				count = count + 1
				line_array2 = content[count].split()	
			i = count

for key in transition_matrix:
	for i in range(0, len(tags)):
		transition_matrix[key][tags[i]] = 0

#constructing the transition matrix
for i in range(0, len(content)):
	line_array = content[i].split()
	if line_array:
		if line_array[1] != "_":
			if line_array[0] == "1":
				transition_matrix["Start"][line_array[tagset]] += 1
			else: 
				transition_matrix[prev_tag][line_array[tagset]] += 1
			prev_tag = line_array[3] 
		else: 
			if line_array[0] == "1":
				prev_tag = "Start"

for key in transition_matrix:
 	total_tags[key] = 0

#counting the total occurrences of the tags in the file
for key in transition_matrix:
	for key2 in transition_matrix[key]:
 		total_tags[key2] += transition_matrix[key][key2]

#counting the total occurrences of the tag Start in the file
for key in transition_matrix["Start"]:
 	total_tags["Start"] += transition_matrix["Start"][key]

#writing the transition matrix into a file after calculating the probabilities
file_transition = open("transition.txt", 'w')
for key in transition_matrix:
	file_transition.write(key + " ");
	for key2 in transition_matrix[key]:
		transition_matrix[key][key2] = float(transition_matrix[key][key2])/total_tags[key]
		file_transition.write(key2 + " " + str(transition_matrix[key][key2]) + " ");
	file_transition.write("\n\n");
file_transition.close()


#writing the likelihood matrix into a file after calculating the probabilities
file_likelihood = open("likelihood.txt", 'w')
for key in likelihood_matrix:
	file_likelihood.write(key + " ");
	for i in range(0, len(likelihood_matrix[key])):
 		likelihood_matrix[key][i] = float(likelihood_matrix[key][i])/total_tags[tags[i]] 
 		file_likelihood.write(str(likelihood_matrix[key][i]) + " ");
 	file_likelihood.write("\n\n");
file_likelihood.close()

#writing all the tags and the tagset type and the most common tag into a file
file_tags = open("tag_order.txt", 'w')
for i in range(0, len(tags)):
	file_tags.write(tags[i] + " ")
file_tags.write("\n")

maximum = 0
for key in total_tags:
	if maximum < total_tags[key]:
		maximum = total_tags[key]
		unknown = key

file_tags.write(unknown)
file_tags.write("\n")
file_tags.write(str(tagset))

file_tags.close()


