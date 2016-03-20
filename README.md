# CMPE561 Project 1 - Author Recognition

##dataset_builder.py##
###You can use dataset_builder.py to create a new training and test set using a source folder.###
This will create a training set in the directory *training_dir* and test set in the directory *test_dir* from the source dataset in the directory *source_dir*.
You can run the program as below: 

`python dataset_builder.py source_dir training_dir test_dir`




##project1.py##

### This program classifies given documents in a test set to an author in the training set ###
This will traverse all the training set in the *training_dir* to create a lexicon and decides which document in *test_dir* belongs to which author.
You can run the program as below: 

`python project1.py training_dir test_dir`

_If you have any problems, please contact me from the e-mail address: **akintoksan@gmail.com**_
