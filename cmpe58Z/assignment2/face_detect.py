from PIL import Image, ImageDraw
import face_recognition
from os.path import join, isdir, isfile, basename, dirname
from os import listdir
from numpy import asarray
from sys import argv, exit


parameter = argv[1]

if isdir(parameter):
    images = sorted(afile for afile in listdir(parameter) if isfile(join(parameter, afile)))
    folder = parameter
elif isfile(parameter):
    folder = dirname(parameter)
    images = (basename(parameter),)
else:
    exit("Given argument must either be a folder path or an image file path.\nAborting...")
    

for image_name in images:
    image = Image.open(join(folder, image_name))

    # height, width = image.size
    # image = image.resize((height//2, width//2))
    image_array = asarray(image)

    d = ImageDraw.Draw(image)

    try:
        face_locations = face_recognition.face_locations(image_array, number_of_times_to_upsample=0, model="cnn")
    except MemoryError as mem_err:
        print('Skipped', image_name, 'because of memory error. You can resize the image and try again')
        continue
    
    # Draw red rectangles around faces
    for face_location in face_locations:
        top, right, bottom, left = face_location
        d.line(((left,top),(right,top),(right,bottom),(left,bottom),(left,top)),fill='red',width=3)


    face_landmarks_list = face_recognition.face_landmarks(image_array)
    # Draw landmarks with default white
    for face_landmarks in face_landmarks_list:
        for facial_feature in face_landmarks.keys():
            d.line(face_landmarks[facial_feature], width=5)

    image.save(join(folder, 'result_' + image_name))
    print('saved', 'result_' + image_name)



