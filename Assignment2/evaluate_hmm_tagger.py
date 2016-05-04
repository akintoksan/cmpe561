#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

output_file = sys.argv[1]
test_gold_file = sys.argv[2]

output_array = []
output_stem = []
gold_array = []
confusion_matrix = {}

#reading the output file
with open(output_file) as f:
    content = f.readlines()

#reading the test gold file
with open(test_gold_file) as f2:
	content2 = f2.readlines()

#reading the tag list, most common tag and tagset type from file
with open("tag_order.txt") as f3:
    content3 = f3.readlines()

#reading the list of unknown words from file
with open("unknown_words.txt") as f4:
    content4 = f4.readlines()

unknown_words = content4[0].split()

tagset = 0
if content3[2][0] == "3":
	tagset = 3
elif content3[2][0] == "4":
	tagset = 4
else: 
	print
	print "ERROR: System could not retrieve the tagset type correctly."
	print

tags_str = content3[0].split()
most_common = content3[1].split()
most_common = most_common[0]

#filling the confusion matrix
for i in range(0, len(tags_str)):
	confusion_matrix[tags_str[i]] = []
	for j in range(0, len(tags_str)):
		confusion_matrix[tags_str[i]].append(0)

#checking the output tags 
for i in range(0, len(content)):
	line_array = content[i].split("|")
	if len(line_array) > 1:
		tag_array = line_array[1].split("\n")
		output_array.append(tag_array[0])

#checking the tags in the test gold files
for i in range(0, len(content2)):
	line_array2 = content2[i].split()
	if line_array2:
		if line_array2[1] != "_":
			gold_array.append(line_array2[tagset])
		if line_array2[2] != "_":
			output_stem.append(line_array2[2])

#comparing the two files and filling the confusion matrix with occurrences
match = 0
for i in range(0, len(output_array)):
	confusion_matrix[gold_array[i]][tags_str.index(output_array[i])] += 1
	if output_array[i] == gold_array[i]:
		match += 1

total_errors = {}
for key in confusion_matrix:
	total_errors[key] = 0

#calculating the probabilities and updating the matrix
for key in confusion_matrix:
 	for i in range(0, len(confusion_matrix[key])):
 		if key != tags_str[i]:
 			total_errors[key] += confusion_matrix[key][i]

for key in confusion_matrix:
	for i in range(0, len(confusion_matrix[key])):
		if key != tags_str[i] and total_errors[key] != 0:
			confusion_matrix[key][i] = float(confusion_matrix[key][i])/total_errors[key] 

#for unknown accuracy
count = 0
total = 0
for i in range(0, len(output_array)):
	if output_stem[i] in unknown_words:
		total += 1
		if gold_array[i] == most_common:
			count += 1

print
print "Accuracy for unknown: " + str(float(count)/total)
print "Accuracy for known: " + str(float(match-count)/(len(output_array)-total))
print "Overall Accuracy: " + str(float(match)/len(output_array))
print
print "CONFUSION MATRIX:"
print
print("columns: "),

for i in range(0, len(tags_str)):
	print(tags_str[i]+ " "),
print
print
print("rows: "),
for key in confusion_matrix:
	print(key),
print
print

#printing the confusion matrix
for key in confusion_matrix:
 	for i in range(0, len(confusion_matrix[key])):
 		if key == tags_str[i]:
 			print("- "),
 		else:
 			print(str("%.2f" % confusion_matrix[key][i]) + " "),
 	print

		