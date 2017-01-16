import math
import numpy as np
import matplotlib.cm as mpcm
import matplotlib.colors as mpcrs


#將 v 週期化到 (-T,T] 區間
def PeriodicCorrect(T,v):
    if (v<=T)&(v>-T):
        return v
    elif v==-T:
        return T
    else:
        T2 = 2*T
        s = (v+T)/T2
        N = math.floor(s)
        if s==N:
            return T
        else:
            return (s-math.floor(s))*T2-T

#找出如果從 (cx,cy) 輻射出直線時，(px,py) 和最接近的那條直線以及連接 (px,py) 和 (cx,cy) 的直線的夾角
def FindLeastAngle(px,py,cx,cy,base,delta):
    theta = math.atan2(py-cy,px-cx)
    return PeriodicCorrect(delta,theta-base)

#產生函數的函數，決定圖片大小和範圍後，先計算每個點的長度和旋轉角度，之後可省下這個計算時間
def GenerateQuasiCrystalRanger(xPixels,yPixels,xRange,yRange):
    x = np.linspace(-xRange,xRange,xPixels)
    y = np.linspace(-yRange,yRange,yPixels)
    radius = np.hypot(x[:,np.newaxis],y[np.newaxis,:])
    angle = np.arctan2(y[np.newaxis,:],x[:,np.newaxis])
    def RetFunc(DensityFunc):
        ret = np.zeros((xPixels,yPixels))
        for m in range(xPixels):
            for n in range(yPixels):
                ret[m][n] = DensityFunc(float(x[m]),float(y[n]),float(radius[m][n]),float(angle[m][n]))
        return ret
    return RetFunc

def GenPCosDF(fold,lineFreq,lOffset,CanNeg=False,aOffset=0):
    ang = [math.pi*2*k/fold+aOffset for k in range(fold)]
    def DensityFunc(x,y,r,t):
        v = 0.0
        for a in ang:
            d = r*math.sin(t+a)
            h = math.cos((d+lOffset)*lineFreq)
            if (h>0)|CanNeg:
                v += h
        v = v/fold
        return v if ((v > 0) | CanNeg) else 0
    return DensityFunc

def GenRCosDF(points,nLines,offset,CanNeg=False):
    delta = math.pi/nLines
    l = len(points)
    scale = math.pi/delta
    def DensityFunc(x,y,r,t):
        v = 0.0
        for p in points:
            h = math.cos(FindLeastAngle(x,y,p[0],p[1],p[3]+offset,delta)*scale)
            if (h>0)|CanNeg:
                v += h
        v /= l
        return v
    return DensityFunc

def MixDF(DFunc):
    if not hasattr(DFunc,'__len__'):
        return None
    def retFunc(x,y,r,t):
        v = 0.0
        num = len(DFunc)
        for f in DFunc:
            v += f(x,y,r,t)
        return v/num
    return retFunc
        

def GenCPoints(r,n,phase=0):
    delta = math.pi*2/n
    ang = [phase+delta*k for k in range(n)]
    return [(r*math.cos(t),r*math.sin(t),r,t-math.pi) for t in ang]

def FillAxisInfo(x,y):
    return (x,y,math.hypot(x,y),math.atan2(y,x)-math.pi)

def GenSPoints(w,ls,bOri):
    ret = []
    if bOri:
        for l in ls:
            ret.extend([FillAxisInfo(m*w,l*w) for m in range(-l,l+1)])
            ret.extend([FillAxisInfo(m*w,-l*w) for m in range(-l,l+1)])
            ret.extend([FillAxisInfo(-l*w,m*w) for m in range(-l+1,l)])
            ret.extend([FillAxisInfo(l*w,m*w) for m in range(-l+1,l)])
    else:
        for l in ls:
            ret.extend([FillAxisInfo(m*w+w/2,l*w-w/2) for m in range(-l,l)])
            ret.extend([FillAxisInfo(m*w+w/2,-l*w+w/2) for m in range(-l,l)])
            ret.extend([FillAxisInfo(-l*w+w/2,m*w+w/2) for m in range(-l+1,l-1)])
            ret.extend([FillAxisInfo(l*w-w/2,m*w+w/2) for m in range(-l+1,l-1)])
    return ret

def GenPCoeff(MaxFold=25,MaxDensity=60):
    f = float(np.random.random()*MaxDensity + 10) # line density
    p = float(np.random.random()*math.pi/f) # line offset
    n = int(np.random.randint(3,MaxFold+1)) # fold
    b = (np.random.randint(0,2)==1)
    return [n,f,p,b]

def GenRPoints(rMin,rMax,nMax,wMin,wMax,lMax):
    t = np.random.randint(3)
    r = float(np.random.rand()*(rMax-rMin)+rMin)
    n = int(np.random.randint(nMax)+6)
    w = float(np.random.rand()*(wMax-wMin)+wMin)
    l1 = int(np.random.randint(1,lMax))
    if np.random.randint(2):
        l2 = int(np.random.randint(l1+1,lMax+1))
    else:
        l2 = l1
    if t==0:
        return GenCPoints(r,n)
    elif t==1:
        return GenSPoints(w,(l for l in range(l1,l2+1)),np.random.randint(2))
    else:
        ret = GenCPoints(r,n, float(np.random.rand()*math.pi) if np.random.randint(2) else 0)
        ret.extend(GenSPoints(w,(l for l in range(l1,l2+1)),np.random.randint(2)))
        return ret
    
def GenRCoeff(rMin=math.pi/3,rMax=math.pi*4,nMax=12,wMin=math.pi/8,wMax=math.pi*2,lMax=5,MaxLines=800):
    pts = GenRPoints(rMin,rMax,nMax,wMin,wMax,lMax)
    nLines = np.random.randint(100,MaxLines)
    offset = np.random.rand()*math.pi/nLines
    b = (np.random.randint(0,2)==1)
    return [pts,nLines,offset,b]

def RandDF(method=None,PCoeffMax=None,RCoeffMax=None,fixFold=None,fixPoints=None):
	pc = GenPCoeff(*PCoeffMax) if PCoeffMax else GenPCoeff()
	if fixFold:
		pc[0] = fixFold
	rc = GenRCoeff(*RCoeffMax) if RCoeffMax else GenRCoeff()
	if fixPoints:
		rc[0] = fixPoints
	if method==0:
		return GenPCosDF(*pc)
	if method==None:
		method = np.random.randint(3)
	elif method==1:
		return GenRCosDF(*rc)
	else:
		a = float(np.random.random()*math.pi)
		pf = GenPCosDF(*pc,aOffset=a)
		rf = GenRCosDF(*rc)
		return MixDF((pf,rf))


AllCmp = ['jet','hsv','viridis','winter','summer','spring','spectral','seismic','rainbow','prism','plasma','pink',
		'ocean','nipy_spectral','magma','inferno','hot','gray','gnuplot','gnuplot2','gist_yarg','gist_stern',
		'gist_gray','gist_earth','flag','cubehelix','copper','coolwarm','cool','bwr','brg','bone','binary','autumn',
		'afmhot','Accent', 'Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'Dark2', 'GnBu', 'Greens', 'Greys', 'OrRd',
		'Oranges', 'PRGn', 'Paired', 'Pastel1', 'Pastel2', 'PiYG', 'PuBu', 'PuBuGn', 'PuOr', 'PuRd', 'Purples',
		'RdBu', 'RdGy', 'RdPu', 'RdYlBu', 'RdYlGn', 'Reds', 'Set1', 'Set2', 'Set3', 'Spectral', 'Wistia', 'YlGn',
		'YlGnBu', 'YlOrBr', 'YlOrRd']

def RandColorMap():
	cmap = AllCmp[np.random.randint(0,len(AllCmp))]
	if np.random.randint(2):
		return cmap
	else:
		return cmap + '_r'

def MergeColor(imgpart):
	num = len(imgpart)
	s = imgpart[0].shape
	rgb = np.zeros((s[0],s[1],3))
	hsv = np.zeros((s[0],s[1],3))
	v = np.zeros((s[0],s[1],1))
	for k in range(num):
		rgb += imgpart[k][:,:,0:3]
		c = mpcrs.rgb_to_hsv(imgpart[k][:,:,0:3])
		v += c[:,:,2:3]
	rgb /= num
	v /= num
	c = mpcrs.rgb_to_hsv(rgb)
	hsv[:,:,0:2] = c[:,:,0:2]
	hsv[:,:,2:3] = v
	return mpcrs.hsv_to_rgb(hsv)

def MergeRGB(imgr,imgg,imgb,xPixels,yPixels,toHSV):
	if toHSV:
		imgpart = [np.zeros((xPixels,yPixels,3)) for k in range(3)]
		imgpart[0][:,:,0] = imgr
		imgpart[1][:,:,1] = imgg
		imgpart[2][:,:,2] = imgb
		img = MergeColor(imgpart)
	else:
		img = np.zeros((xPixels,yPixels,3))
		img[:,:,0] = imgr
		img[:,:,1] = imgg
		img[:,:,2] = imgb
	return img
