import torch 
import torch.nn as nn 
import torch.optim as optim 



#THIS PART BELOW SETS UP THE AI



class TestNN(nn.Module):
    def __init__(self):
        super(TestNN, self).__init__()
        self.fc1 = nn.Linear(1,10)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(10,100)
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


model = TestNN()

criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(),lr=0.001)
import math






#THIS PART BELOW DEFINES INPUTS AND OUTPUTS







inputs = torch.tensor([ 
          [6.4],[7.44],[31.4],[13.6],
          [14.5],[13.4],[7.8],[8.33],
          [8.42],[8.5],[9.18],[5.39],
          [6.41],[48.5],[152.0],[169.0]
         
          ])

targets = torch.tensor([  
          [8.7*10**-6],[9.0*10**-5],[3.5*10**-6],[2.3*10**-5],
          [1.7*10**-6],[1.6*10**-6],[3.7*10**-5],[3.0*10**-5],
          [1.7*10**-5],[1.6*10**-5],[2.4*10**-5],[1.1*10**-6],
          [7.8*10**-7],[5.4*10**-7],[5.9*10**-8],[9.8*10**-8]
        
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
"Spleen necrosis virus",
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
"Bacteriophage T2"
]


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




#THIS PART BELOW RUNS TRAINING


print("How many training scycles do you want? (Type zero for default)")
loops = int(input())
if loops ==0:
    loops = 5000

for epoch in range(loops):
    optimizer.zero_grad()

    outputs=model(inputs)
    loss = criterion(outputs,targets)
    loss.backward()
    optimizer.step()

   
    print(f'Epoch [{epoch+1}/{loops}], Loss: {loss.item():.4f}')

test_data = torch.tensor([[2.2502386]])
pred=model(test_data)

print("TEST")
print(f'pred: {pred.item():.4f} \nGoal: -11.330604')

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
matplotlib.use('Agg')





#THIS PART BELOW GIVES THE OUTPUTS

def getData(Xpoints):
    rtn = [[],[]]
    for x in Xpoints:
        x1 = torch.tensor([[x]])
        inMdl=model(x1)
        rtn[0].append(x)
        rtn[1].append(float(f'{inMdl.item():.4f}'))
    return rtn



def visuals(points):

    xpoints =  [ [], []]
    ypoints =  [ [], []]
    yguess  =  [ [], []]
    error   =  [ [], []] 

    fig0,axs0=plt.subplots()

    xpoints1=np.array(points[0])
    ypoints1=np.array(points[1])
    
    axs0.scatter(xpoints1,ypoints1)

    xpoints2 = np.array(dataX)
    ypoints2 = np.array(dataY)

    axs0.scatter(xpoints2,ypoints2)


    xpoints[0] = xpoints2.tolist().copy()
    ypoints[0] = ypoints2.tolist().copy()
    


    xpoints3=np.array(xpoints2)
    ypoints3=np.array(ypoints2)


    lineP = np.array([0,0])
    linePX =np.array([1.5,5.5])

    axs0.plot(linePX,lineP)

    guessYpoint3=[]

    for x in range(len(xpoints2)):
         guessYpoint3.append(ypoints1[np.where( xpoints1==min(xpoints1,key=lambda a:abs(a-xpoints2[x]) ))[0][0]]) 
         ypoints3[x]= guessYpoint3[x]-ypoints2[x]


    axs0.scatter(xpoints3,ypoints3)

    yguess[0] = guessYpoint3.copy()
    error[0] = ypoints3.tolist().copy()

    fig0.savefig('mutAI/dataVisuals/DataSet1/plot_mut_Size_ln.png')

    #NOW FOR BASE SCALING RATHER THAN LN SCALING

    fig1,axs1=plt.subplots()

    xpoints1=np.array(points[0])
    ypoints1=np.array(points[1])

    for x in range(len(xpoints1)):
        xpoints1[x]=math.e**xpoints1[x]
        ypoints1[x]=math.e**ypoints1[x]
    
    axs1.scatter(xpoints1,ypoints1)

    xpoints2 = np.array(dataX)
    ypoints2 = np.array(dataY)

    for x in range(len(xpoints2)):
        xpoints2[x]=math.e**xpoints2[x]
        ypoints2[x]=math.e**ypoints2[x]

    axs1.scatter(xpoints2,ypoints2)



    xpoints[1] = xpoints2.tolist().copy()
    ypoints[1] = ypoints2.tolist().copy()
    

    xpoints3=np.array(xpoints2)
    ypoints3=np.array(ypoints2)

    lineP = np.array([0,0])
    linePX =np.array([min(xpoints1),max(xpoints1)])

    axs1.plot(linePX,lineP)

    guessYpoint3=[]

    for x in range(len(xpoints2)):
         guessYpoint3.append(ypoints1[np.where( xpoints1==min(xpoints1,key=lambda a:abs(a-xpoints2[x]) ))[0][0]]) 
         ypoints3[x]= guessYpoint3[x]-ypoints2[x]

    axs1.scatter(xpoints3,ypoints3)
     
    yguess[1] = guessYpoint3.copy()
    error[1] = ypoints3.tolist().copy()

    fig1.savefig('mutAI/dataVisuals/DataSet1/plot_mut_Size_e.png')

    #NOW FOR BASE ONLY ON Y BUT LN ON X

    fig2,axs2=plt.subplots()

    xpoints1=np.array(points[0])
    ypoints1=np.array(points[1])
    for x in range(len(ypoints1)):
        ypoints1[x]=math.e**ypoints1[x]
    
    axs2.scatter(xpoints1,ypoints1)

    xpoints2 = np.array(dataX)
    ypoints2 = np.array(dataY)

    for x in range(len(ypoints2)):
        ypoints2[x]=math.e**ypoints2[x]

    axs2.scatter(xpoints2,ypoints2)

    xpoints3=np.array(xpoints2)
    ypoints3=np.array(ypoints2)

    lineP = np.array([0,0])
    linePX =np.array([min(xpoints1),max(xpoints1)])

    axs2.plot(linePX,lineP)

    for x in range(len(xpoints2)):
         ypoints3[x]= ypoints1[np.where( xpoints1==min(xpoints1,key=lambda a:abs(a-xpoints2[x]) ))[0][0]] -  ypoints2[x]


    axs2.scatter(xpoints3,ypoints3)
     
    fig2.savefig('mutAI/dataVisuals/DataSet1/plot_mut_Size_e-ln.png')

    rtn = [virusNames,xpoints,ypoints,yguess,error]

    return rtn


def writeOutput(inRTN,file_name="mutAI/dataOutputFiles/outData_mut_size_DataSet1.txt",wrt="w"):
    

    with open(file_name,wrt) as f:
        header =       ["Name","Error LN*","Error Base","Virus Size LN","Virus Size Base","Mutation Rate LN","Mutation Rate Base","Mutation Guess LN","Mutation Guess Base"]
        f.write(f"{header[0]:<50} | {header[1]:^25} | {header[2]:^25} | {header[3]:^25} | {header[4]:^25} | {header[5]:^25} | {header[6]:^25} | {header[7]:^25} | {header[8]:>25}\n")
        for x in range(len(inRTN[0])):
                  f.write(f"\n{inRTN[0][x]:<50} | {inRTN[4][0][x]:^25} | {inRTN[4][1][x]:^25} | {inRTN[1][0][x]:^25} | {inRTN[1][1][x]:^25} | {inRTN[2][0][x]:^25} | {inRTN[2][1][x]:^25} | {inRTN[3][0][x]:^25} | {inRTN[3][1][x]:>25}")
        f.write("\n\n*note that unlike virus size and mutation rates, for which the ln output is fond by taking the natual log of the base, the natural log error value is not the \nnatural log of the base error (with the base error being the diffrence from the base guessed mutation rate and the base actual mutation rate) but rather the natural log \nerror rate is the diffrence between the error of the natural log of the guseed mutation rate and the natural log of hte actuall mutation rate")

def plotOut(Xpoints):
    return visuals(getData(Xpoints))

pntMax=torch.max(inputs)
pntMin=torch.min(inputs)
pntDis=abs(pntMin-pntMax)
pntBuff = pntDis/10
#10 chosen based on vibes. only impacts visuals so not important
pntStart = max(0,(pntMin-pntBuff))
pntDisStart = pntMin-pntStart
pntEnd=pntMax+pntDisStart
pntDisScl = 5000/(pntEnd-pntStart)

inp=[]
for x in range(5000):
    inp.append(pntStart+x/pntDisScl)



writeOutput(plotOut(inp))