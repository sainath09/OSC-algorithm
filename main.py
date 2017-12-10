import numpy as np
from sklearn import preprocessing
import warnings
import ops
import imgutils as imu
import scipy.misc
import imageio
from sys import argv
import cv2

warnings.filterwarnings("ignore")

class model:
  def __init__(self,X,U,t_max=10,e_init=10.0,e_final=1.0,k=256,n=256,l=10):
    '''

    :param X: Input dictionary with key as index and a numpy
               array is value for each input
    :param t_max: maximun iterations
    :param e_init: learning rate initial
    :param e_final: final learning rate
    :param k: sparsity level
    '''
    self.X=X
    self.t_max=t_max
    self.e_init=e_init
    self.e_final=e_final
    self.K=k
    self.U=U
    self.n=n
    self.l=l


  def init_training(self):
    for t in range(self.t_max):
      print t,self.K
      e_t = self.e_init*(self.e_final/self.e_init)**(t/float(self.t_max))
      rand_int = np.random.randint(0,self.l)
      x_res = self.X[rand_int]

      seqnce=dict() # dictionary of index and (u_nt *x)^2
      for ni in range(self.n):
        seqnce[ni] = (np.matmul(self.U[ni],x_res))**2

      sorted_n = []
      for key, value in sorted(seqnce.iteritems(), key=lambda
                (k, v): (v, k),reverse=True):
        #print "%s: %s" % (key, value)
        sorted_n += [key]

      for k in range(0,self.n):
        for l in range(0,k-1):
          self.U[sorted_n[k]] = self.U[sorted_n[k]] - np.matmul(self.U[sorted_n[k]],self.U[sorted_n[l]]) * self.U[sorted_n[l]]
        if(k<self.K):
          y = np.matmul(self.U[sorted_n[k]],x_res)
          self.U[sorted_n[k]] = self.U[sorted_n[k]] + (e_t*y)*x_res
        temp = np.array(self.U[sorted_n[k]]).reshape(1,-1)
        temp = preprocessing.normalize(temp,norm ='l2')
        self.U[sorted_n[k]] = temp[0]
        x_res = x_res-(np.matmul(self.U[sorted_n[k]],x_res)) * self.U[sorted_n[k]]

    return self.U

def main():
 print "hello"
 myargs = ops.getopts(argv)
 print(myargs)
 #input
 if(myargs['-istrain'] == 'True'):
   if '-genX' in myargs:
    op = imu.genU(myargs, myargs['-genX'])
   else:
    op = imu.genU(myargs)
 else:
   print 'image compression part'
   input_file = ''
   if('-inputimg' in myargs):
    input_file = myargs['-inputimg']
   else:
     print 'file not found'
     return
   t_max = myargs['-t_max']
   k = 64
   n = 64 # always 64
   U = np.genfromtxt("output/output_image_" + str(t_max) + '_' + str(k / float(n)) + ".csv" , delimiter=',')

   img = imageio.imread(input_file)
   output_image = np.zeros(img.shape[0]*img.shape[1]).reshape(img.shape[0] , img.shape[1])

   for i in range(0,img.shape[0]/8,1):
     for j in range(0,img.shape[1]/8,1):
       #print index, i ,j
       output_image[i*8 : i*8 + 8 , j*8 : j*8+8]= imu.compress(U,X = img[i*8 : i*8 + 8 , j*8 : j*8+8])
   compressed_image = scipy.misc.toimage(output_image,high=255,low=0)
   print "saving to output/",input_file
   compressed_image.save('output/'+ input_file )
   img = cv2.imread('output/'+ input_file)
   equalized = cv2.equalizeHist(img[:,:,0])
   cv2.imwrite('output/'+ input_file+'.png',equalized)
   print "written ",'output/'+ input_file+'.png'


''' uncomment  and put a loop in genU method to plot for varous k
   print op
   lists = sorted(op.items())
 
 x, y = zip(*lists)
 plt.xlabel('K/N')
 plt.ylabel('SNR*100')
 plt.plot(x, y)
 plt.savefig('output/graph_'+myargs['-input']+'.png')
'''


if __name__ == '__main__':
  main()
