Python Version: 2.7.10

# CMPE561 Project 1 - Authorship Recognition

##dataset_builder.py##
You can use dataset_builder.py to create a new training and test set using a source folder.


This will create a training set in the directory *training_dir* and test set in the directory *test_dir* from the source dataset in the directory *source_dir*.
You can run the program as below: 

`python dataset_builder.py source_dir training_dir test_dir`




##project1.py##
This program classifies given documents in a test set to an author in the training set.


This will traverse all the training set in the *training_dir* to create a lexicon and decides which document in *test_dir* belongs to which author.
You can run the program as below: 

`python project1.py training_dir test_dir`

_If you have any problems, please contact me from the e-mail address: **akintoksan@gmail.com**_


# CMPE561 Project 2 - Hidden Markov Model (HMM) Tagger

**Dependencies:** Did not include any other modules than "sys" and "os".

##train_hmm_tagger.py##
train_hmm_tagger.py takes the “training file” and Part-of-Speech tagset (cpostag or postag) as arguments and trains the tagger.
You can run the program as below:

`python train_hmm_tagger.py traning_file tagset`

Example: 

`python train_hmm_tagger.py /Users/akintoksan/Desktop/cmpe_561_pr2/metu_sabanci_cmpe_561/metu_sabanci_cmpe_561/train/turkish_metu_sabanci_train.conll cpostag`

or 

`python train_hmm_tagger.py /Users/akintoksan/Desktop/cmpe_561_pr2/metu_sabanci_cmpe_561/metu_sabanci_cmpe_561/train/turkish_metu_sabanci_train.conll postag`

##hmm_tagger.py##
hmm_tagger.py takes the “test file” and “output file” as arguments and tags the unseen
test data and writes the computed tags into output file.
You can run the program as below:

`python hmm_tagger.py test_file output_file`

Example: 

`python hmm_tagger.py /Users/akintoksan/Desktop/cmpe_561_pr2/metu_sabanci_cmpe_561/metu_sabanci_cmpe_561/validation/turkish_metu_sabanci_val.conll output.txt`

##evaluate_hmm_tagger.py##
evaluate_hmm_tagger.py takes “output file” and “gold file” as arguments and compares the output of your tagger with the gold standard for the test data. It prints out the overall accuracy of the tagger, accuracy for the known words and for the unknown words. It also produces and print a confusion matrix.
You can run the program as below:

`python evaluate_hmm_tagger.py output_file test_gold_file`

Example:

`python evaluate_hmm_tagger.py output.txt /Users/akintoksan/Desktop/cmpe_561_pr2/metu_sabanci_cmpe_561/metu_sabanci_cmpe_561/validation/turkish_metu_sabanci_val.conll`



