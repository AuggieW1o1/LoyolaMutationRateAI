data = [[6.4,8.7*10**-6],[7.44,9.0*10**-5],[32.4,3.5*10**-6],[13.6,2.3*10**-5],
          [14.5,1.7*10**-6],[13.4,1.6*10**-6],[7.8,3.7*10**-5],[8.33,3*10**-5],
          [8.42,1.7*10**-5],[8.5,1.6*10**-5],[9.18,2.4*10**-5],[5.39,1.1*10**-6],
          [6.41,7.8*10**-7],[48.5,5.4*10**-7],[152.0,5.9*10**-8],[169.0,9.8**10**-8]]
c0 = 1
c1 = 1
c2 = 1
c3 = 1
c4 = 1 
c5 = 1
c6 = 1
c7 = 1
c8 = 1
c9 = 1
c10 = 1
c11 = 1
c12 = 1
ls = 0.000000000001
c = [c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]
cp =[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1]

import math
import random
def main(input):
    global all
    inpt = data[input][0]
    guess=c0+c1*inpt+c2*(c3**inpt)+c4*(inpt**c5)+c6 *math.log((math.fabs(c7+c8*inpt+(c9**inpt)+c10*(inpt**c11))),(max(c12,1)+0.1)) 
    error = data[input][1]-guess
    for x in range(13):
        c[x]+=(error)/math.fabs(error)*ls*math.tanh((random.random())**2)*cp[x]

it = 0

while(it<1000000):
    for x in range(16):
        main(x)
    it+=1
    ls*=0.999999999999999
    if(it%1000==0):
        for x in range(13):
            print("c"+str(x)+": "+str(c[x]))