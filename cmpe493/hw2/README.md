


Code written in python3 tested and working on Ubuntu 16.04LTS
The program consists of 5 python files:

Article.py				=> Article class representation of an article
pprocs.py				=> in charge of preprocess
utils.py				=> holds some helper methods and fields
mnb_all_words_fs.py		=> makes the classification using all words as features - prints some statistics
mnb_mi_fs.py			=> makes the classification using k=50 words as features - prints some statistics

These all need to be in the same directory. And the .sgm files should be in the folder called Dataset which is next to these python scripts.

No arguments needed for any script.
First run pprocs.py, this will produce data_collection.pickle file which will be used by other scripts.
Then:
	For making test using all words as features  : run mnb_all_words_fs.py, this will print some statistics
	For making test using k=50 words as features : run mnb_mi_fs.py, this too will print some statistics
These two will read data_collection.pickle file for further process

The program is divided like this for easier implementation. Sorry for any inconvenience this might cause to you.

you don’ t need to do anything to utils.py or Article.py, they are used behind the scenes.
