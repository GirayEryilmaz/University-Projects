Anaconda python3 project

Had to install face_recognition via pip though.

There is one source file face_detect.py. It takes one argument which has to be a valid path to either an image or a directory that contains image files to be processed and no other file.

The program saves edited images with 'result_' prefix added to their names, next to the originals.



Bug: If the image file is too large the library throws a MemoryError. The program catches the error and skips the image, also informs the user by printing an error message to standart output. Resizing the image works but I believe that the user should decide to what degree the image should be resized so I made no assumptions. I had this problem only with a few images, in some platforms this may not even be a problem at all. Sometimes you may need to restart the kernel or sadly the computer.


