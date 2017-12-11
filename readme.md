# Orthogonal sparse coding

> Dictionary learning and image compression using state of art efficient method

##Data sets

* make sure you have data set mnist 'MNIST/train.csv' in the current directory

   *download link : https://s3.amazonaws.com/sparsefiles/train.csv
* make sure you have the dataset natural images in 'naturalimages/image_0001.jpg' to naturalimages/image_0526.jpg
download link : 
https://s3.amazonaws.com/sparsefiles/naturalimages/image_0001.jpg 
*** replace 0001 with 0001,0002...0526 to download images ***

3)  extract these files in './compdata/' for image compresion application
Download link : 
https://s3.amazonaws.com/sparsefiles/output/output/pgmfiles.zip


## running command :
 python main.py [flags]
 different flags 
	-input description of input data set - one of  MNIST | imgcomp | natimages
	-t_max maximum mumber of iterations
	-k ratio of k/N to run - any integer between 0.1 to 0.9
	-genX a boolean to generate X from data set or use the existing csv file
	  set it to false for initial run.
        -inputimg specify the path of input file for compression
        -istrain a bool value to train the system or compress 
	  set it to true for generating U.
	warning : give t_max to same value for testing and training as the name U saves depends on t_max to retrive U for compression.

## Example usages :

* '''python main.py -input MNIST -t_max 1000000 -k 1 -genX True  -istrain True '''
* ''' python main.py -input imgcomp -t_max 1000000 -k 1 -genX True  -istrain False -inputimg /compimg/1.pgm '''
[do this only after generating U]
* '''python main.py -input natimages -t_max 1000000 -k 1 -genX True  -istrain False -inputimg '''

## required python libraries : 
* numpy
* skimage
* scipy.misc
* scipy.stats
* imageio
* cv2
* sklearn - preprocessing	  
* matplotlib - pyplot
      




## Directory structure

* compdata
    * 15 images of benchmark data set [link](http://imagecompression.info/test_images/) 
    * 1.pgm
    * 2.pgm
    * ...
    * 15.pgm
*  imgutils.py
    * a python utils script which will be used nby main.py  
* main.py
    * this is where program starts execution as in given above format
* ops.py
  * math ops used by main.py and mathutils
* MNIST/
    * MNIST data set in the form of .csv file[link](https://www.kaggle.com/c/digit-recognizer/data)
    * train.csv
* naturalimages/
    * data set of natural images [link](http://www.vision.caltech.edu/html-files/archive.html)
    * image_0001.jpg
    * image_0002.jpg 
    * ....
    * image_0526.jpg
* output/
    * compdata/ (make sure you have this directory or else python throws an error)
    * all other output data from code generation
* readme.md



