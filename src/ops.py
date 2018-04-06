
import numpy as np
import imageio

'''parse the command line arguments

'''
def getopts(argv):
  '''

  :param argv: command line args in the form of list
  :return: A dictionary of flag as key and next arg as value
  Example python main.py -input MNIST -k 1 -t 100000 -genX True
  returns {'-input' : MNIST , '-k' : '1' , '-t' : 100000 ,'-genX' : True }
  '''
  opts = {}
  while argv:
    if argv[0][0] == '-':
      opts[argv[0]] = argv[1]
    argv = argv[1:]
  return opts


''' calculating PSNR'''
def calcSNR(U):
  signal = U.mean()
  print signal
  noise = U.std()
  print noise
  PSNR = 10*np.log10(signal/float(noise))
  return PSNR

'''
returns image patch of random number i,j from image
'''
def extarctpatch_image(i,j,image):
  return image[i*8:(i*8)+8,j*8:(j*8)+8]
