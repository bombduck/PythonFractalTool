import sys,math,random
from tkinter import *

def addline(line,p,v):
	pnew=(p[0]+v[0],p[1]+v[1])
	line.append((p[0],p[1],pnew[0],pnew[1]))
	return pnew

def rotate(v,angle):
	return (v[0]*math.cos(angle)-v[1]*math.sin(angle),v[0]*math.sin(angle)+v[1]*math.cos(angle))

def RegPoly(v,n,clock=True):
	ret=[]
	ang=-math.pi*2/n if clock else math.pi*2/n
	p=v
	m=0
	while m<n-1:
		pnew=rotate(p,ang)
		ret.append((p[0],p[1],pnew[0],pnew[1]))
		p=pnew
		m=m+1
	ret.append((p[0],p[1],v[0],v[1]))
	return ret

def KnockIter(line):
	ret=[]

	p1=(line[0],line[1])
	p2=(line[2],line[3])
	vec=((p2[0]-p1[0])/3,(p2[1]-p1[1])/3)
	p=p1
	p=addline(ret,p,vec)
	p=addline(ret,p,rotate(vec,math.pi/3))
	p=addline(ret,p,rotate(vec,-math.pi/3))
	p=addline(ret,p,vec)
	return ret

def KnockIter2(line):
	ret=[]

	p1=(line[0],line[1])
	p2=(line[2],line[3])
	vec=((p2[0]-p1[0])/3,(p2[1]-p1[1])/3)
	p=p1
	p=addline(ret,p,vec)
	ptemp=p
	p=addline(ret,p,rotate(vec,math.pi/3))
	p=addline(ret,p,rotate(vec,-math.pi/3))
	p=ptemp
	p=addline(ret,p,rotate(vec,-math.pi/3))
	p=addline(ret,p,rotate(vec,math.pi/3))
	p=addline(ret,p,vec)
	return ret

def KnockIter3(line):
	ret=[]

	p1=(line[0],line[1])
	p2=(line[2],line[3])
	vec=((p2[0]-p1[0])/3,(p2[1]-p1[1])/3)
	p=p1
	p=addline(ret,p,vec)
	p=addline(ret,p,rotate(vec,math.pi/3))
	p=addline(ret,p,rotate(vec,-math.pi/3))
	p=addline(ret,p,rotate(vec,-math.pi*2/3))
	p=addline(ret,p,rotate(vec,math.pi*2/3))
	p=addline(ret,p,vec)
	p=addline(ret,p,vec)
	return ret

def KnockIter4(line):
	ret=[]

	p1=(line[0],line[1])
	p2=(line[2],line[3])
	vec=((p2[0]-p1[0])/3,(p2[1]-p1[1])/3)
	p=p1
	p=addline(ret,p,vec)
	p=addline(ret,p,rotate(vec,math.pi/3))
	p=addline(ret,p,rotate(vec,-math.pi/3))
	ptemp=p
	p=addline(ret,p,rotate(vec,-math.pi*2/3))
	p=addline(ret,p,rotate(vec,math.pi*2/3))
	p=ptemp
	p=addline(ret,p,vec)
	return ret

def LinesIterate(lines,func):
	ret=[]
	for l in lines:
		ret.extend(func(l))
	return ret

def CompositeIterate(first,second):
	def NewFunc(line):
		ret=[]
		lines=first(line)
		for l in lines:
			ret.extend(second(l))
		return ret
	return NewFunc
	
def CommonVecIterate(lines):
	def NewFunc(line):
		ret=[]
		v=(line[2]-line[0],line[3]-line[1])
		if abs(v[0])<0.00000000000001:
			ang=math.pi/2 if v[1] > 0 else -math.pi/2
		elif v[0] > 0:
			ang=math.atan(v[1]/v[0])
		else:
			ang=math.atan(v[1]/v[0])+math.pi
		r=(v[0]**2+v[1]**2)**(1/2)
		rm=((r*math.cos(ang),-r*math.sin(ang)),(r*math.sin(ang),r*math.cos(ang)))
		for l in lines:
			ret.append((line[0]+rm[0][0]*l[0]+rm[0][1]*l[1],line[1]+rm[1][0]*l[0]+rm[1][1]*l[1],
						line[0]+rm[0][0]*l[2]+rm[0][1]*l[3],line[1]+rm[1][0]*l[2]+rm[1][1]*l[3]))
		return ret
	return NewFunc

def RandomIterate(iterFuncs):
	def NewFunc(line):
		f=iterFuncs[random.randint(0,len(iterFuncs)-1)]
		return f(line)
	return NewFunc
		

## Draw lines on canvas c.
def draw(c, lines):
	centerx=c.winfo_width()//2
	centery=c.winfo_height()//2
	s=min(centerx,centery)
	c.delete(ALL)
	for l in lines:
		c.create_line(centerx+s*l[0],centery-s*l[1],centerx+s*l[2],centery-s*l[3],fill='black',width=2)

## Main program.
def main(argv=None):
	global alllines
	global iterFunc
	oneline=[(-1,0,1,0)]
	xline=[(0.5,0.5,-0.5,-0.5),(0.5,-0.5,-0.5,0.5)]
	alllines=RegPoly((0,0.5),4,True)
	#alllines=oneline

	pattern1=[(0,0,0.25,0),
			  (0.25,0,0.25,0.25),
			  (0.25,0.25,0.5,0.25),
			  (0.5,0.25,0.75,0.25),
			  (0.75,0.25,0.75,0),
			  (0.75,0,1,0)]
	pattern2=[(0,0,0.25,0),
			  (0.25,0,0.25,0.25),
			  (0.25,0.25,0.5,0.25),
			  (0.5,0.25,0.5,0),
			  (0.5,0,0.5,-0.25),
			  (0.5,-0.25,0.75,-0.25),
			  (0.75,-0.25,0.75,0),
			  (0.75,0,1,0)]
	pattern3=[(0,0,0.25,0),
			  (0.25,0,0.25,0.25),
			  (0.25,0.25,0.25,0.5),
			  (0.25,0.5,0.5,0.5),
			  (0.5,0.5,0.5,0.25),
			  (0.5,0.25,0.5,0),
			  (0.5,0,0.5,-0.25),
			  (0.5,-0.25,0.5,-0.5),
			  (0.5,-0.5,0.75,-0.5),
			  (0.75,-0.5,0.75,-0.25),
			  (0.75,-0.25,0.75,0),
			  (0.75,0,1,0)]
	sfi1=CommonVecIterate(pattern1)
	sfi2=CommonVecIterate(pattern2)
	sfi3=CommonVecIterate(pattern3)
	#iterFunc=CompositeIterate(CommonVecIterate(pattern3),KnockIter3)
	#iterFunc=CommonVecIterate(pattern3)
	iterFunc= RandomIterate((KnockIter,KnockIter2,KnockIter3,KnockIter4,sfi1,sfi2,sfi3))

	def resize(event=None):
		draw(canvas,alllines)

	def iterate_once():
		global alllines
		global iterFunc
		alllines=LinesIterate(alllines,iterFunc)
		resize()

	root = Tk()
	root.title("Koch Snow")
	bot=Frame(root)
	bot.pack(side=BOTTOM)
	canvas = Canvas(root,width=400,height=400);
	canvas.bind("<Configure>",resize)
	canvas.pack(expand=YES,fill=BOTH)

	itButton=Button(bot,text="iterate",command=iterate_once)
	itButton.pack()

	mainloop()

if __name__=='__main__':
	sys.exit(main())
