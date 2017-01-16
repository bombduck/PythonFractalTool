import sys
import os
import math
import random
import matplotlib.image as mpimg
import numpy as np
import matplotlib.cm as cm
from Quasicrystal import * 

def RandBool():
	if random.randint(0,1) == 0:
		return True
	else:
		return False

w = 1024
r = math.pi

MaxPF = 30
MaxF = 50

MinR = math.pi/4
MaxR = math.pi*4
MaxRF = 20
MinGW = math.pi/8
MaxGW = math.pi
MaxL = 5
MaxLines = 1000

ranger = GenerateQuasiCrystalRanger(w,w,r,r)


def ProduceImg(method=None,fold=None,points=None):
	if method==None:
		method = random.randint(0,2)
	df = RandDF(method,(MaxPF,MaxF),(MinR,MaxR,MaxRF,MinGW,MaxGW,MaxL,MaxLines),fold,points)
	img = ranger(df)
	return img

if len(sys.argv) > 1:
	os.mkdir(sys.argv[1])

num=1
if len(sys.argv) > 2:
	num=int(sys.argv[2])

for k in range(num):
	name = '{0:05}'.format(k+1)
	print('start:'+name)

	method = random.randint(0,3)

	fixPC = GenPCoeff(MaxPF,MaxF)
	fixRC = GenRCoeff(MinR,MaxR,MaxRF,MinGW,MaxGW,MaxL,MaxLines)
	if method==0:
		img = ProduceImg(method=0,fold=fixPC[0],points=None)
	elif method==1:
		img = ProduceImg(method=1,fold=None,points=fixRC[0])
	elif method==2:
		img = ProduceImg(method=2,fold=fixPC[0],points=fixRC[0])
	else:
		img = ProduceImg()
	for c in AllCmp:
		fname = sys.argv[1]+'/'+name+'_'+c+'.png'
		mpimg.imsave(fname=fname,arr=np.array(img),cmap=c)
		fname = sys.argv[1]+'/'+name+'_'+c+'_r'+'.png'
		mpimg.imsave(fname=fname,arr=np.array(img),cmap=c+'_r')
