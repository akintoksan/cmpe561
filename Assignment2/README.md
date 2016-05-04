Python Version: 2.7.10

# CMPE561 Project 2 - Hidden Markov Model (HMM) Tagger

**Dependencies:** Did not include any other modules than "sys" and "os".

**IMPORTANT:** When you are giving a file name as an argument, please give the full path of the file. I didn't implement any error handling there'. If you are sure that the file is in the same directory with the python file, you can use the name without the full path.

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


ps. When we run the train_hmm_tagger.py file, I keep the tagset type (cpostag or postag) in the file tag_order.txt. So, hmm_tagger.py and evaluate_hmm_tagger.py takes the tagset type from this file.


ps2. The confusion matrix that I put on the report is not the percentage but a value between 0 and 1. So, a value of 0.18 means 18% in the matrix. I updated the code to give the results in terms of percentage. But I had already submitted the report so I couldn't change the matrix in the report.




_If you have any problems, please contact me from the e-mail address: **akintoksan@gmail.com**_

