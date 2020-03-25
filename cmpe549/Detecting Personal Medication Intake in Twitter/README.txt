CmpE549 Term Project READ ME file.
The project is developed and tested with python, in colab environment.
There are 3 ipynb files, 
1) drug_intake_bert.ipynb
2) drug_intake_bilstm.ipynb
3) ner_sentence_analysis.ipynb

They all connect to dgrive. (The cell that makes the connection will give an url, you need to click it to login and give permission to access to the gdrive AND you must have the provided 549_data.zip file in the drive)
They fetch the zip file provided and extract the training and test files (both are csv) to current working directory. Then they load the data.
You will need to upload 549_data.zip file to a gdrive to be able to fetch it.
I don't recommend any other way because it will require more work to get the GPU working and downloading the bert model, word vectors etc.
I don't recommend tpu or cpu. Gpu is much faster and the code assumes gpu.


1) drug_intake_bert.ipynb :
This notebook loads a bert model, adds a layer and fine tunes the model.

2) drug_intake_bilstm.ipynb:
This one trains a bidirectional lstm with GPU. It needs cudnn, please enable gpu support in colab.


3) ner_sentence_analysis.ipynb:
This one investigates what verbs, names and, objects can be extracted from the tweets.
Then tries to identify if they can be useful.

All work totally fine in colab.
If need further help, please open an issue.
Note: When I try to run them all in parallel colab complains and disconnects.
