Implemented in python, on ubuntu. Unfortunately the code became somewhat messy, I am dreadfully sorry about that.

The code has a bunch of python scripts serving as libraries and a bunch of jupyter notebooks that are used as mains. This is mainly because I had to use colab for running the code since I needed to use GPUs. There are also a few data files needed.

scripts are:
    evaluation.py
    FaceRecognizer.py
    helpers.py
    LBP.py
    preprocessign.py

files are:
    shape_predictor_68_face_landmarks.dat
    mmod_human_face_detector.dat
    vgg_face_weights.h5
    people.txt                          
    g_i_538_684.json                    //this file contains genuine and imposter pairs printed from triplet_generation.ipynb
    ll2_ul1000_triplets_10_10.json      //this file contains triplets for training printed from triplet_generation.ipynb

notebooks are:
    transfer_learning_face_recognition.ipynb
    svm_lbp_face_recognition.ipynb
    cv2_lbp_face_recognition.ipynb
    knn_lbp_face_recognition.ipynb
    triplet_finetuning.ipynb
    model_evaluation.ipynb
    triplet_generation.ipynb
    
    I will explain them below.
    
    General notes about notebooks: On colab I had to access to drive, so on each notebook first cell connects to the drive and adds the folder in which the python scripts live to the path. You may delete the first cell and keep the scripts next to the notebooks if you are not going to use colab.
    If you are going to use colab, when you run the first cell it will ask you to authorize access to your drive where the scripts and the data lives (defaults to '/content/gdrive/My Drive/workspace'). Sorry for this inconvenience.
    Also colab sometimes breaks while loading images, it complains "RuntimeError: Unable to open file: lfw/<person>/<person>_<number>.jpg". Just re-run the cell and it should do fine. Colab also crashes when multiple notebooks are run in parallel giving os errors, internal errors and similar.
    
    On second cell there are imports. Nothing needs to be done here.
    
    On third cells of each notebook, paths to necessary are files and folders are defined. The default is next to the notebooks you should not need to change these.
    
    triplet_finetuning.ipynb notebook also needs one extra path to "modified weights" : path_to_save_weights
    

I will explain notebooks:
    transfer_learning_face_recognition.ipynb is for  running face recognition demo with transfer learning
    
    svm_lbp_face_recognition.ipynb is for running demo for lbph face recognition with svm
    
    cv2_lbp_face_recognition.ipynb is for  running face recognition demo with opencv
    
    knn_lbp_face_recognition.ipynb is for running lbph face recognition with 1NN
    
    triplet_finetuning.ipynb is for fine tuning the transfer learning model
    
    model_evaluation.ipynb is for evaluating deep learning model with identification

    triplet_generation.ipynb is actually a helper, it generates two files for fine tuning and evaluating transfer learning models. This was needed because of technical problems. I had to use colab for running training and evaluations but accessing to drive for too frequently crashes Colab. So I had to prepare these two files on local then load them on colab. I will provide these two files as example so you wont need to run this code.
    
3rd party libraries used:

Unfortunately I don’t have a yaml file because colab takes care of the environment. But the list is as follows:

dlib : for loading images, face detection, cropping and alignment.
cv2 (openface) : for comparing my lbp implementation with.
sklearn: for train test split and svm classifier
matplotlib : for drawing plots
keras: for building the and training the neural network
numpy and pandas for data analysis, (reading csv, making arrays etc).
PIL: I was using this to load images and cropping etc before I switched to dlib.
scipy: for distance testing different distance functions (it is more efficient than pure python) 

If you encounter any problems just open an issue.





 








