import numpy as np
import skimage
from main import model
import scipy.misc
import scipy.stats
import ops
import imageio
def compress(U,X):
  '''

  :param U: A 64*64 learned basis vector
  :param X: An 8*8 image patch flattend to a 64*1 vector.
  :return: X* - recovered from U*A
  '''


  X = X.flatten()
  a = np.matmul(U.transpose(),X)

  dict_a = dict()
  for i in range(64):
    dict_a[i] = a[i]
  dict_index = dict()
  i = 1
  for key, value in sorted(dict_a.iteritems(), key=lambda
                (k, v): (v, k),reverse=True):
    dict_index[key] = value
    i += 1
    if (i >32):
      break
  a_star = np.zeros(64)
  for key in dict_index:
    a_star[key] = dict_index[key]
  X_star = np.matmul(U,a_star)
  return X_star.reshape(8,8)


def genU(myargs,genX='False'):
  '''
  method to generate U for given set of natural images
  data set images are in directory naturalimages/  and are
  named image_0001.jpg to image_0526.jpg

  :param myargs: Command line arguments
  :param genX: a bool value to specify to generate X from given pool of data set
  :return: returns a dictionary of SNR vs K/N
  '''
  op = dict()
  if(genX == 'True'):
    X = np.zeros(64)
    if(myargs['-input'] == 'natimages'):
      for i in range(1,527):
        print "image:",i
        image_name = ''
        if(len(str(i)) == 1):
          image_name = 'image_000'+str(i) + '.jpg'
        elif(len(str(i)) == 2):
          image_name = 'image_00'+str(i) + '.jpg'
        elif(len(str(i)) == 3):
          image_name = 'image_0'+str(i) + '.jpg'
        image = scipy.misc.imread('naturalimages/'+image_name,mode = 'L',flatten=True)
        for patches in range(100):
          rand_i = np.random.randint(0, image.shape[0] / 8)
          rand_j = np.random.randint(0, image.shape[1] / 8)
          patch = ops.extarctpatch_image(rand_i, rand_j, image)
          patch = np.array(patch).flatten()
          X = np.vstack((X, patch))
      X = X[1:, ]

    elif(myargs['-input'] == 'imgcomp'):
      for i in range(1, 11):
        img = imageio.imread('compdata/' + str(i) + '.pgm')
        number_of_patches = img.shape[0] * img.shape[1] / 64
        for patches in range(1000):
          rand_i = np.random.randint(0, img.shape[0] / 8)
          rand_j = np.random.randint(0, img.shape[1] / 8)
          patch = ops.extarctpatch_image(rand_i, rand_j, img)
          patch = np.array(patch).flatten()
          X = np.vstack((X, patch))
      X = X[1:, ]

    elif(myargs['-input'] == 'MNIST'):
      input_file = 'train.csv'
      X = np.genfromtxt(input_file, delimiter=',', dtype=np.uint8)
      X = skimage.img_as_float(X)
      print X[1]
      X = X[1:, 1:]
    else:
      print "Input format:", "python main.py -input [imgcomp | train.csv | natimages ] -t [integer] -k [[0,1] float ratio k/n] -genX [bool - True to regnerate X or  flse for " \
                             "using the .csv file"
      return
    np.savetxt("output/output_"+myargs['-input']+"_X_" + ".csv", X, delimiter=',')

  X = np.genfromtxt('output/output_'+myargs['-input']+'_X_', delimiter=',', dtype=np.uint8)
  X = skimage.img_as_float(X)
  n = X.shape[1]
  l = X.shape[0]
  t_max = int(myargs['-t'])
  e_init = 2.8
  e_final = 2.8 * (10) ** -3
  U = np.identity(n)
  k = int(myargs['-k']) * n
  m = model(X=X, U=U, t_max=t_max, e_init=e_init, e_final=e_final, k=k, n=n, l=l)
  trained_U = m.init_training()
  np.savetxt("output/output_output_"+myargs['-input']+"_U" + str(t_max) + '_' + str(k / float(n)) + ".csv", trained_U, delimiter=',')
  img = scipy.misc.toimage(trained_U, high=255, low=0)
  img.save("output/output_output_"+myargs['-input']+"_U" + str(t_max) + '_' + str(k / float(n)) + ".png")
  op[k / float(n)] = scipy.stats.signaltonoise(trained_U, axis=None)
  return op
