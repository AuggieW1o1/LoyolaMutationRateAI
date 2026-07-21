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





inputs = torch.tensor([ 
    #ROW 0
          [6.4,1862,1545,1223,1765],
          [7.44,2206,1711,1737,1786],
          [31.4,8138,7487,5614,10118],
          [13.59, 4480, 3299, 2596, 3213],
    #ROW 1
          [14.45, 5182, 3252, 2552, 3466],
          [13.38, 2697, 3688, 3783, 3217],
          #[7.8],
          [8.33,2143,2025,2395,1769],
    #ROW 2
          [8.42, 1850, 1770, 2790, 2009],
          [8.5,1976,1562,2986,1983],
          [9.18,3411,2373,1772,2163],
          [5.39,1291,1254,1157,1694],
    #ROW 3
          [6.41,1576,1314,1296,2221],
          [48.5,12334,12820,11362,11986],
          [152.0,24248,52422,51308,24033],
          [163.82, 52305, 27182, 30677, 53661],
    
    #BONUS DATA
    
    #ROW 4
          [4.22, 1016, 1035, 1011, 1153],
          [7.13,2314,1476,1450,1972],
          [9.49, 2976, 2283, 1817, 2418],
          [9.65,1889,2724,2893,2140],
    #ROW 5
          [11.2,3467,2431,2227,3036],
          [15.9,4634,3732,3802,3726],
          [2.02,894,625,675,827],
          [13.2,4371,2656,2448,3745],
    #ROW 6
          [9.4,2230,2704,2378,2080],
          [235,50536,68279,67176,49655],

          ])

targets = torch.tensor([  
    #ROW 0
          [8.7*10**-6],
          [9.0*10**-5],
          [3.5*10**-6],
          [2.3*10**-5],
    #ROW 1
          [1.7*10**-6],
          [1.6*10**-6],
          #[3.7*10**-5],
          [3.0*10**-5],
    #ROW 2 
          [1.7*10**-5],
          [1.6*10**-5],
          [2.4*10**-5],
          [1.1*10**-6],
    #ROW 3
          [7.8*10**-7],
          [5.4*10**-7],
          [5.9*10**-8],
          [9.8*10**-8],

    #BONUS DATA
    
    #ROW 4
          [1.4E-4],
          [6.9E-5],
          [1.2E-5],
          [3.8E-5],
    #ROW 5
          [3.7E-5],
          [3.5E-5],
          [2E-5],
          [2.1E-5],
    #ROW 6
          [1.4E-4],
          [2E-7],    

          ])


virusNames = [
#Row 0
        "Tobacco mosaic virus",
        "Poliovirus 1",
        "Murine hepatitis virus",
        "Influenza A virus",
#Row 1
        "Influenza B virus",
        "Bacteriophage φ6",
        #"Spleen necrosis virus",
        "Murine leukemia virus",
#Row 2
        "Bovine leukemia virus",
        "Human T-cell leukemia virus type 1",
        "Human immunodeficiency virus (MULTIPLE TPYES)",
        "Bacteriophage φX174",
#Row 3
        "Bacteriophage M13",
        "Bacteriophage λ",
        "Herpes simplex virus type 1",
        "Bacteriophage T2",

#BONUS DATA

#ROW 4
        "Bacteriophage Qβc",
        "Human rhinovirus 14",
        "Tobacco etch virus",
        "Hepatitis C virus",
#ROW 5
        "Vesicular stomatitis virus",
        "Measles virus d",
        "Duck hepatitis B virus",
        "Foamy virus",
#ROW 6     
        "Rous sarcoma virus",
        "Human cytomegalovirus",      
]



#THIS PART BELOW SETS UP THE AI



class TestNN(nn.Module):
    
    def __init__(self):
        super(TestNN, self).__init__()
        self.fc1 = nn.Linear(5,10)
        self.relu = nn.ReLU()
        self.dout = nn.Dropout(p=0)
        self.fc2 = nn.Linear(10,25)
        self.fc3 = nn.Linear(25,50)
        self.fc4 = nn.Linear(50,25)
        self.fc5 = nn.Linear(25,10)
        self.fc6 = nn.Linear(10,1)
         
    def go(self,x):
        x=self.relu(x)
        #x=self.dout(x)
        return x

    def forward(self,x):
        x = self.fc1(x)
        x = self.go(x) 
        x = self.fc2(x)
        x = self.go(x)
        x = self.fc3(x)
        x = self.go(x)      
        x =self.fc4(x)
        x = self.go(x)       
        x =self.fc5(x)
        x =self.fc6(x)
        return x


class smolNN(nn.Module):
    def __init__(self):
        super(smolNN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(5, 16),
            nn.ReLU(),
            nn.Linear(16, 24),
            nn.ReLU(),
            nn.Linear(24, 16),
            nn.ReLU(),
            nn.Linear(16, 5),
            #nn.ReLU(),
            nn.Linear(5, 1) 
        )
        
    def forward(self, x):
        return self.net(x)
import math

#IT TURNS OUT MAKING THE AI SMALL HELPS A LOT

model = smolNN()


learning_rate=0.003

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
        inputs[x][y]=2*inputs[x][y]/total
time.sleep(1)
ready=1
time.sleep(0.4)





# Convert inputs to a float tensor for math operations
inputs = inputs.float()

# Calculate mean and standard deviation along the dataset rows
input_means = inputs.mean(dim=0)
input_stds = inputs.std(dim=0)

# Normalize the data: (X - mean) / std
# This gives every feature equal footing in the eyes of the AI
inputs = (inputs - input_means) / input_stds




#THIS PART BELOW RUNS TRAINING
default_loops=500
print(f"How many training scycles do you want? (Type zero for default of {default_loops})")
loops = int(input())

stopL = str(input("What loss value would you like to quit at? (Enter blank or -1 if you dont wish to quit)\n"))

if stopL == "":
    stopL=float(-1)
stopL=float(stopL)    

if loops ==0:
    loops = default_loops

go=1

runs = 0

import random

def randArray(amount=10):
    amount=min(amount,len(virusNames))
    rtn = [0]*amount
    for x in range(amount):
        ran=random.randint(1,len(virusNames))
        while ran in rtn:
            ran=random.randint(1,len(virusNames))
        rtn[rtn.index(0)]=ran
    return rtn


def randTargets(randOut):
    randTarg=[]
    #print(randOut)
    for x in randOut:
        randTarg.append(targets[x-1].tolist())
    randTargTens=torch.tensor(randTarg)
    return randTargTens

def randInputs(randOut):
    randIn=[]
    #print(randOut)
    for x in randOut:
        randIn.append(inputs[x-1].tolist())
    randInTens=torch.tensor(randIn)
    return randInTens

def randData(a=10):
    pHold=randArray(a)
    return[randInputs(pHold),randTargets(pHold)]

def reRandData(c,inI,inT,a=10):
    rtn=[inI.tolist(),inT.tolist()]
    phold=[randData(a)[0].tolist(),randData(a)[1].tolist()]
    if c%2==0:
        for x in range(5):
            rtn[0][x]=phold[0][x]
            rtn[1][x]=phold[1][x]
    else:
        for x in range(5,10):
            rtn[0][x]=phold[0][x]
            rtn[1][x]=phold[1][x]
    return rtn

print(randData())

avLossMtr=[0]*5
for epoch in range(loops):
   
    if go==1: 
        if epoch==0:
            randOt=randData()
        else:
            rand05=reRandData(epoch,randIn,randTr)
        randIn=randOt[0]
        randTr=randOt[1]

        runs+=1

        optimizer.zero_grad()

        outputs=model(randIn)
        loss = criterion(outputs,randTr)
        loss.backward()
        optimizer.step()


        lossInt=round(loss.item(),5)
        avLossMtr.pop(0)
        avLossMtr.append(lossInt)
        avLoss=round(sum(avLossMtr)/5,5)


        print(f'Epoch [{epoch+1}/{loops}]       Loss: {lossInt:<13} Average Loss: {avLoss:<10}')
        


        if stopL>=avLoss and go==1:
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


default_dir = "outData_mut_size_DataSet1_Seq.txt"

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

        header = ["Name","Mutation Rate*","Predicted Rate*","Error","Genome Size (KB)*","A%**","G%**","C%**","T%**"]
        f.write(f"{header[0]:^50} | {header[1]:^25} | {header[2]:^25} | {header[3]:^25} | {header[4]:^25} | {header[5]:^20} | {header[6]:^20} | {header[7]:^20} | {header[8]:^20}")
        f.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~")
        for x in range(len(inRTN[0])):
                  space=" "
                  out1[0].append(inRTN[1][x])
                  out1[1].append(inRTN[2][x])
                  out1[2].append(inRTN[4][x])
                  if inRTN[3][x]<0:
                      space=""
                  f.write(f"\n{inRTN[0][x]:^50} | {inRTN[1][x]:<25} | {inRTN[2][x]:<25} | {space+str(inRTN[3][x]):<25} | {inRTN[4][x]:<25} | {inRTN[5][x]:<25} | {inRTN[6][x]:<25} | {inRTN[7][x]:<25} | {inRTN[8][x]:<25}")
        

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

            #reIn = torch.tensor([[gSizeO,aCountO/total,gCountO/total,cCountO/total,tCountO/total]])
            # Update your manual entry block to use the exact same scaling factors:
            reIn = torch.tensor([[gSizeO, aCountO/total, gCountO/total, cCountO/total, tCountO/total]]).float()
            eIn = (reIn - input_means) / input_stds

            outO = model(reIn)
            
            out2[0].append(mutRO)
            out2[1].append(outO.item())
            out2[2].append(gSizeO)


            f.write(f"\n{nameO:^50} | {mutRO:<25} | {outO.item():<25} | {(mutRO-outO.item()):<25} | {gSizeO:<25} | {aCountO/total:<50} | {gCountO/total:<25} | {cCountO/total:<25} | {tCountO/total:<25}")
            
            others=input("\nWould you like to run the AI on other data? ")

        f.write("\n\n\n*The values listed is the natural log of the value indicated by the row header, for the rows containing an asterisk\n**Yup, these precentages sure are wrong. Nope, it wont be explained.\n\n\n")
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


    plt.savefig('plot_mut_Size_ln.png')


def plotOut(Xpoints):
    visuals(getData(Xpoints))






getResults()