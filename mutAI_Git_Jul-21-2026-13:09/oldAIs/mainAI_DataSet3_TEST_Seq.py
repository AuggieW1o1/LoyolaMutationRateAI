import torch 
import torch.nn as nn 
import torch.optim as optim 



#THIS PART BELOW DEFINES INPUTS AND OUTPUTS

#INPUT FORMAT: [kb Size, a, g, c, t] for a,g,c,t are the amount of that nucleotide in the virus genome


ready=0


def cuteLoadingScreen():
    count=0
    frames = ["",".","..","..."]
    while(ready==0):
        count+=1
        print(f"\rLoading{frames[count%4]:<4}",end="",flush=True)
        time.sleep(1/3)
        if count>=4:
            count=0
    print(f"\r",end="",flush=True)
        


import threading,time
cuteLoadThreadt = threading.Thread(target=cuteLoadingScreen)
cuteLoadThreadt.start()


inputs = torch.tensor(
[
[14274.48,4751512,2387147,2388460,4747361],
[39686.25,9485087,10338110,10349945,9505768],
[39112.55,9340513,10199767,10212192,9358737],
[18916.11,4897552,4558519,4560957,4898624],
[12071.33,3730180,2309287,2313713,3718146],
]
)

targets = torch.tensor([ 
[1.20E-10],
[3.20E-10],
[3.01E-10],
[3.02E-07],
[3.45E-07],
])

virusNames = [
"Candida albicans",
"IPO323*",
"IPO323△chr18",
"C. neoformans",
"S. cerevisiae",
]



#THIS PART BELOW SETS UP THE AI


class TestNN(nn.Module):
    def __init__(self):
        super(TestNN, self).__init__()
        self.fc1 = nn.Linear(5,25)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(25,100)
        self.fc3 = nn.Linear(100,500)
        self.fc4 = nn.Linear(500,100)
        self.fc5 = nn.Linear(100,10)
        self.fc6 = nn.Linear(10,1)
    def forward(self,x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x =self.relu(x)
        x =self.fc4(x)
        x =self.relu(x)
        x =self.fc5(x)
        x =self.relu(x)
        x =self.fc6(x)
        return x

import math


model = TestNN()


learning_rate=0.01

criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(),lr=learning_rate)

#The following converts inputs into numbers usable by the ai

dataLen = len(virusNames)

dataX = []
dataY = []
for x in range(dataLen):
    dataX.append(0)
    dataY.append(0)


count=0
for x in inputs:
    dataX[count]=math.log(x[0])
    x[0]=math.log(x[0])
    count+=1
count=0
for x in targets:
    dataY[count]=math.log(x[0])
    x[0]=math.log(x[0])
    count+=1

#The following covnerts input data for nucleotides total to percentage since otherwise the model explodes


for x in range(len(inputs)):
    total=inputs[x][1]+inputs[x][2]+inputs[x][3]+inputs[x][4]
    for y in range(1,len(inputs[x])):
        inputs[x][y]=float(inputs[x][y])
        inputs[x][y]=1+inputs[x][y]/total
time.sleep(1)
ready=1
time.sleep(0.4)

#THIS PART BELOW RUNS TRAINING

print("How many training scycles do you want? (Type zero for default of 1000)")
loops = int(input())

stopL = str(input("What loss value would you like to quit at? (Enter blank or -1 if you dont wish to quit)\n"))

if stopL == "":
    stopL=float(-1)
stopL=float(stopL)    

if loops ==0:
    loops = 1000

go=1

runs = 0

for epoch in range(loops):
   
    if go==1: 

        runs+=1

        optimizer.zero_grad()

        outputs=model(inputs)
        loss = criterion(outputs,targets)
        loss.backward()
        optimizer.step()
        print(f'Epoch [{epoch+1}/{loops}], Loss: {loss.item():.4f}')

        if stopL>=loss.item() and go==1:
            go=0
            loopsEnd=loops

if go == 0:
    loops=loopsEnd
                


#THIS PART BELOW GIVES THE OUTPUTS
def getData():
    rtn=[[],[],[],[],[],[],[],[],[]]
    count=0
    for x in targets:
        rtn[0].append(virusNames[len(rtn[0])])
        rtn[1].append(x.item())
        phold=model(inputs[count]).item()
        rtn[2].append(phold)
        rtn[3].append(x.item()-phold)
        for y in range(5):
            rtn[4+y].append(inputs[len(rtn[4+y])][y].item())
        count+=1
    return rtn


default_dir = "mutAI/dataOutputFiles/DataSet3_Seq/TEST_outData_mut_size_DataSet3_Seq.txt"

def howSave():
    rtn=["",""]
    inpt =""
    #There was code here for saving to dir but i removed it and made it default always unsless changed
    rtn[0]=default_dir
    inpt2=""
    inpt2 = input("Are you adding to an old file rather than making a new file/overiding a file? ")
    while inpt2.lower()!="yes" and inpt2.lower()!="no" and inpt2!="":
        print("Please respond with yes or no")
        inpt2 = input("Are you adding to an old file rather than making a new file/overiding a file? ")
    if inpt2.lower()=="yes" or inpt2=="":
        rtn[1]="a"
    else:
        rtn[1]="w"
    return [rtn[0],rtn[1]]


import datetime

def writeOutput(inRTN,file_name=default_dir,wrt="w"):
    global all
    out1=[[],[],[]]
    with open(file_name,wrt) as f:
        time = datetime.datetime.now()
        ctime=time.strftime("%c")
        f.write("_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________\n=============================================================================================================================================================================================================================================================\n")
        f.write(f"Date/Time: {ctime}\nLearning Rate: {learning_rate}\nEpochs: {runs}\nFinal Loss: {round(loss.item(),5)}\n\n")

        header = ["Name","Mutation Rate*","Predicted Rate*","Error","Genome Size (KB)*","A%","G%","C%","T%"]
        f.write(f"{header[0]:^50} | {header[1]:^25} | {header[2]:^25} | {header[3]:^25} | {header[4]:^25} | {header[5]:^20} | {header[6]:^20} | {header[7]:^20} | {header[8]:^20}")
        f.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~")
        for x in range(len(inRTN[0])):
                  space=" "
                  out1[0].append(inRTN[1][x])
                  out1[1].append(inRTN[2][x])
                  out1[2].append(inRTN[4][x])
                  if inRTN[3][x]<0:
                      space=""
                  f.write(f"\n{inRTN[0][x]:^50} | {inRTN[1][x]:<25} | {inRTN[2][x]:<25} | {space+str(inRTN[3][x]):<25} | {inRTN[4][x]:<25} | {inRTN[5][x]:<20} | {inRTN[6][x]:<20} | {inRTN[7][x]:<20} | {inRTN[8][x]:<20}")
        

        #THIS PART ALLOWS YOU TO RUN THE AI ON OTHER DATA NOT FROM THE TRAINING DATA
        out2=[[],[],[]]
        others=input("Would you like to run the AI on other data? ")
        if (others.lower()=="yes"):
            f.write("")
        while others.lower()=="yes":
            nameO = str(input("Please enter its name: "))
            mutRO = math.log(float(input("Please enter its mutation rate (NOT LOG OF RATE): ")))
            gSizeO = math.log(float(input("Please enter its genome size in KB (NOT LOG OF KB): ")))
            aCountO = float(input("Please enter the amount of \"a\" nucleotides: "))
            gCountO = float(input("Please enter the amount of \"g\" nucleotides: "))
            cCountO = float(input("Please enter the amount of \"c\" nucleotides: "))
            tCountO = float(input("Please enter the amount of \"t\" nucleotides: "))

            total = aCountO+gCountO+cCountO+tCountO

            reIn = torch.tensor([[gSizeO,aCountO/total,gCountO/total,cCountO/total,tCountO/total]])

            outO = model(reIn)
            
            out2[0].append(mutRO)
            out2[1].append(outO.item())
            out2[2].append(gSizeO)


            f.write(f"\n{nameO:^50} | {mutRO:<25} | {outO.item():<25} | {(mutRO-outO.item()):<25} | {gSizeO:<25} | {aCountO/total:<20} | {gCountO/total:<20} | {cCountO/total:<20} | {tCountO/total:<20}")
            
            others=input("\nWould you like to run the AI on other data? ")

        f.write("\n\n\n*The values listed is the natural log of the value indicated by the row header, for the rows containing an asterisk\n\n\n")
        return [out1[0],out1[1],out1[2],out2[0],out2[1],out2[2]]
    

def getResults():
    howSaveOut=howSave()
    vIn = writeOutput(getData(),howSaveOut[0],howSaveOut[1])
    visuals(vIn[0],vIn[1],vIn[2],vIn[3],vIn[4],vIn[5])






#BELOW IS GRAPHING: 



import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('Agg')



def visuals(targ,guess,gsize,targ2,guess2,gsize2):

    size=[]
    for x in range(len(targ)):
        size.append(1)
    for x in range(len(targ2)):
        targ.append(targ2[x])
        guess.append(guess2[x])
        gsize.append(gsize2[x])
        size.append(2)

    minGsize = min(gsize)

    maxGsize = max(gsize)

    lineP = [min(guess),max(guess)]
    linePX= [min(targ),max(targ)]


    lineN=min(lineP[0],linePX[0])
    lineX=max(lineP[1],linePX[1])

    #THERE IS REASON BEHIND "uhhWhat" HOWEVER IM TOO TIERD TO EXPLAIN IT.

    uhhWhat = 50 - 30 * ( 0.0* ( ( 1- ( ( 1/1.01 )**len(gsize) ) ) / ( 1- ( 1/0.01 ) ) ) )
  
    uhhList=[]
    for y in size:
        uhhList.append(uhhWhat*y)

    plt.plot([lineN,lineX],[lineN,lineX],c="#000000",zorder=-100,lw=2,alpha=1/3)

    plt.scatter(targ,guess,c=gsize,cmap='viridis',vmin=minGsize,vmax=maxGsize,alpha=1,s=uhhList)
   
    plt.gcf().set_layout_engine('constrained')

    for x in range(len(targ)):
        av=(targ[x]/2+guess[x]/2)
        plt.plot([av,targ[x]],[av,guess[x]],lw=1.5,zorder=-10000,alpha=0.25,c="#000000")


    cbar = plt.colorbar(pad=0.2,label="Color scale based on genome size")

    plt.xlabel("Actual mutation rate of virus")

    plt.ylabel("AI predicted mutationrate of virus")

    plt.title("Graphical Representation of Mutation Rate AI")

    cbar.ax.yaxis.set_ticks_position("left")


    plt.savefig('mutAI/dataVisuals/DataSet3_Seq/TEST_plot_mut_Size_ln.png')


def plotOut(Xpoints):
    visuals(getData(Xpoints))






getResults()