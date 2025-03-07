from random import choice
import pygame
from base import pb as pyb
from math import sqrt
import ast
pygame.init()
pygame.mixer.init()
X = 1100
Y = 700



#NEED TO FIX INS/OUTS SO THEY ARE DICTS




screen = pygame.display.set_mode((X, Y),pygame.RESIZABLE)#,pygame.FULLSCREEN)
clk=pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 20)
pb=pyb(screen,font)
ltrs="1234567890-=!@#$%^&*()_+qwertyuiop[]asdfghjkl;zxcvbnm,./QWERTYUIOP{}|ASDFGHJKL:ZXCVBNM<>?"
def dist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)
def gen():
    return "".join([choice(ltrs)for i in range(10)])
ms=pms=[0,0,False]
class LogicWires:
    def __init__(self,startID,x,y,ID="",endID=[],pos=None):
        self.strt=startID
        self.end=endID
        self.pos=pos if pos else [[x,y]]
        self.value=0
        self.ID=ID
    def disp(self,mx=-231,my=-231):
        for i in range(0,len(self.pos)-1):
            p1=self.pos[i]
            p2=self.pos[i+1]
            pb.line(p1[0],p1[1],p2[0],p2[1],width=5,col=((255,0,0)if self.value else (0,0,0)))
        if self.end==[]:pb.line(self.pos[-1][0],self.pos[-1][1],mx,my,width=5)
    def build(self,mx,my,spot=""):
        if spot=="":self.pos.append([mx,my])
        else:self.end=spot
    def update(self):
        global updateNext,gates_wires
        if self.strt[2]=="in":self.value=gates_wires[self.strt[0]].ins[self.strt[1]]
        else:self.value=gates_wires[self.strt[0]].outs[self.strt[1]]
        updateNext=updateNext+[self.end[0]]
    def isPress(self,mx,my,pmx,pmy):pass
    def __repr__(self):
        return f"LogicWires({self.strt},{None},{None},ID=r'{self.ID}',endID={self.end},pos={self.pos})"
class logicGate:
    def __init__(self,x,y,ins={},outs={},name="NothingToSeeHere",ID='',ties=[]):
        self.x,self.y=x,y
        self.ins=ins
        self.outs=outs
        self.width=len(name)*10+20
        self.name=name
        self.height=max(len(self.ins),len(self.outs))*20
        self.ID=ID
        self.ties=ties
    def disp(self,mx,my):
        pb.rect(self.x,self.y,self.width,self.height,col=(100,100,100))
        for x,i in enumerate(self.ins):
            cx,cy=self.x,self.y+x*20+10
            pb.circle(cx,cy,6,col=((255,0,0)if self.ins[i]else (0,0,0)))
            if dist(cx,cy,mx,my)<10:pb.text(i,mx,my-10)#,col=(120,120,120))
        for x,i in enumerate(self.outs):
            cx,cy=self.x+self.width,self.y+x*20+10
            pb.circle(cx,cy,6,col=((255,0,0)if self.outs[i] else (0,0,0)))
            if dist(cx,cy,mx,my)<10:pb.text(i,mx,my-10)#,col=(120,120,120))
        pb.text(self.name,self.x+10,self.y+self.height/2-10)
    def update(self):
        global updateNext
        self.logic()
        updateNext=updateNext+self.ties
    def logic(self):
        pass
    def inOrOut(self,mx,my):
        for i in range(len(self.ins)):
            cx,cy=self.x,self.y+i*20+10
            if dist(cx,cy,mx,my)<10:return[self.ID,i,"in"]
        for i in range(len(self.outs)):
            cx,cy=self.x+self.width,self.y+i*20+10
            if dist(cx,cy,mx,my)<10:return[self.ID,i,"out"]
        return False
    def isPress(self,mx,my,pmx,pmy):
        if mx>self.x and my>self.y and mx<self.x+self.width and my<self.y+self.height:
            if pmx!=mx or my!=pmy:
                self.x+=(mx-pmx)
                self.y+=(my-pmy)
            self.onPress(mx,my)
    def onPress(self,mx,my):
        pass
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x},{self.y},ins={self.ins},outs={self.outs},name='{self.name}',ID=r'{self.ID}',ties={self.ties})"
class And(logicGate):
    def __init__(self,x,y,ins={},outs={},name="",ID="",ties=[]):
        super().__init__(x,y,ins={"A":0,"B":0},outs={"O":0},name="AND",ID=ID,ties=ties)
    def logic(self):
        self.outs["O"]=int(self.ins["A"] and self.ins["B"])
class Not(logicGate):
    def __init__(self,x,y,ins={},outs={},name="",ID="",ties=[]):
        super().__init__(x,y,ins={"A":0},outs={"O":0},name="NOT",ID=ID,ties=ties)
    def logic(self):
        self.ins["A"]=int(not self.ins["A"])
class Or(logicGate):
    def __init__(self,x,y,ins={},outs={},name="",ID="",ties=[]):
        super().__init__(x,y,ins={"A":0,"B":0},outs={"O":0},name="Or",ID=ID,ties=ties)
    def logic(self):
        self.outs["O"]=int(self.ins["A"] or self.ins["B"])
class Nand(logicGate):
    def __init__(self,x,y,ins={},outs={},name="",ID="",ties=[]):
        super().__init__(x,y,ins={"A":0,"B":0},outs={"O":0},name="NAND",ID=ID,ties=ties)
    def logic(self):
        self.outs["O"]=int(not (self.ins["A"] and self.ins["B"]))
class Nor(logicGate):
    def __init__(self,x,y,ins={},outs={},name="",ID="",ties=[]):
        super().__init__(x,y,ins={"A":0,"B":0},outs={"O":0},name="NOR",ID=ID,ties=ties)
    def logic(self):
        self.outs["O"]=int(not (self.ins["A"] or self.ins["B"]))
class Xor(logicGate):
    def __init__(self,x,y,ins={},outs={},name="",ID="",ties=[]):
        super().__init__(x,y,ins={"A":0,"B":0},outs={"O":0},name="XOR",ID=ID,ties=ties)
    def logic(self):
        self.outs["O"]=int((self.ins["A"] or self.ins["B"])and not(self.ins["A"] and self.ins["B"]))
class Xnor(logicGate):
    def __init__(self,x,y,ins={},outs={},name="",ID="",ties=[]):
        super().__init__(x,y,ins={"A":0,"B":0},outs={"O":0},name="XNOR",ID=ID,ties=ties)
    def logic(self):
        self.outs["O"]=int(not ((self.ins["A"] or self.ins["B"])and not(self.ins["A"] and self.ins["B"])))
class Lever(logicGate):
    def __init__(self,x,y,ins={},outs={},name="",ID="",ties=[]):
        super().__init__(x,y,ins=[],outs={"O":0},name="Lever",ID=ID,ties=ties)
    def onPress(self,mx,my):
        self.outs["O"]=int(not self.outs["O"])
gates=[And,Not,Or,Nand,Nor,Xor,Xnor,Lever]
def clear():
    with open("save.txt","w")as save:save.write("{}")
# clear()
bob=[]
with open("save.txt","r")as save:
    bob=save.read()
gates_wires=eval(bob)
updateNext=update=[]
select=-1
k1,k2,k3,k4,k5,k6,k7,k8,k9,k0=pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0
# print("its on")
wire=None
pMF=False
while True:
    update=updateNext
    # updateNext=[]
    screen.fill((200,200,200))
    # pms=ms.copy()
    pms=[pms[0]if pMF else ms[0],pms[1]if pMF else ms[1],ms[2]]
    pMF=False
    ms=[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],False]
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            print("Saving...")
            with open("save.txt","w")as save:
                print(gates_wires)
                save.write(str((gates_wires)))
            quit()
        elif i.type==pygame.MOUSEBUTTONDOWN and i.button==1:
            ms[2]=True
            if select==9:
                if wire==None:
                    for i in gates_wires:
                        if i[:4]=="gate":
                            frog=gates_wires[i].inOrOut(ms[0],ms[1])
                            if frog:
                                wire=LogicWires(frog,ms[0],ms[1],ID="wire"+gen())
                                # gates_wires[i].
                                break
                else:
                    for i in gates_wires:
                        if i[:4]=="gate":
                            frog=gates_wires[i].inOrOut(ms[0],ms[1])
                            if frog and frog!=wire.strt:
                                wire.end=frog
                                gates_wires[wire.ID]=wire
                                wire.build(ms[0],ms[1])
                                gates_wires[wire.strt[0]].ties.append(wire.ID)
                                gates_wires[wire.end[0]].ties.append(wire.ID)
                                wire=None
                                select=-1
                                break
                    else:wire.build(ms[0],ms[1])
            elif select!=-1:
                bob="gate"+gen()
                gates_wires[bob]=gates[select](ms[0],ms[1],ID=bob)
                select=-1
    if select!=-1:
        if select==9:
            if wire!=None:wire.disp(ms[0],ms[1])
            pb.text("Wire",0,0)
        elif select<len(gates):
            gates[select](ms[0],ms[1]).disp(0,0)
    if pygame.mouse.get_pressed()[0]:
        pMF=True
    pb.text(f"{updateNext}",0,20)
    keys=pygame.key.get_pressed()
    if keys[k1]:select=1
    elif keys[k2]:select=2
    elif keys[k3]:select=3
    elif keys[k4]:select=4
    elif keys[k5]:select=5
    elif keys[k6]:select=6
    elif keys[k7]:select=7
    elif keys[k8]:select=8
    elif keys[k9]:select=9
    elif keys[k0]:select=0
    for i in gates_wires:
        gates_wires[i].disp(ms[0],ms[1])
        if ms[2]==False and pms[2]:
            gates_wires[i].isPress(ms[0],ms[1],pms[0],pms[1])
    for i in update:
        gates_wires[i].update()
    pygame.display.flip()