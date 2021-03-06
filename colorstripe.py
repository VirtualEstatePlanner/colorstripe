import numpy
import cv2
import os
import sys

# confirm the user has given all arguments
if len(sys.argv) < 2:
    print('Please enter video path')
    sys.exit()
elif len(sys.argv) < 3:
    print('Please enter output image height')
    sys.exit()
elif len(sys.argv) < 4:
    print('Please enter output image width')
    sys.exit()

# convert CLI arguments to program variables
path = os.path.expanduser(sys.argv[1])
imgWidth = int(os.path.expanduser(sys.argv[2]))
imgHeight = int(os.path.expanduser(sys.argv[3]))

def colorsOfFilm(path, imgWidth, imgHeight):
    vidcap = cv2.VideoCapture(path)
    success,image = vidcap.read()

    frames = []

# check if there are remaining frames to process, and if there are then process them
    success = True
    while success:
      try:
          success,image = vidcap.read()
          avg_row_col = numpy.average(image, axis=0)
          avg_color = numpy.average(avg_row_col, axis=0)
          avg_color = numpy.uint8(avg_color)
          frames.append(avg_color)
      except IndexError:
          break

# get the average of the bucket size
    new_image = []
    frame_per_bucket_as_float = len(frames) / imgWidth
    frame_per_bucket = numpy.uint8(frame_per_bucket_as_float)
    if frame_per_bucket < 1:
        frame_per_bucket = 1
    for frames in numpy.split(frames, range(frame_per_bucket, len(frames), frame_per_bucket)):
        av = numpy.average(frames, axis=0)
        new_image.append(av)

    new_image = numpy.array(new_image)

    n,d = new_image.shape
    image = numpy.repeat(new_image, imgHeight, axis=0)
    image = numpy.reshape(image, (n, imgHeight, d))
    cv2.imwrite('/output/output.png', image.transpose(1,0,2))

# run the program
colorsOfFilm(path, imgWidth, imgHeight)
