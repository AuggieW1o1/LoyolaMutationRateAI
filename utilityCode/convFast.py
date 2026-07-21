
import threading,time,math
 
def findNth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)
def count(chr=">"):
    with open (fileName,"r") as text:
        file = text.read()
        amt = file.count(chr)
        rtn=[amt,[]]
        for x in range(amt):
            file2=file
            pos=findNth(file,">",x)
            rtn[1].append(pos)
            #print(pos)
        rtn[1].append(len(file))
        return rtn
def initArrayStr(amt):
    ary=[]
    for x in range(amt):
        ary.append("")
    return ary
def initArrayObj(amt):
    ary=[]
    for x in range(amt):
        ary.append(None)
    return ary
def countSeq(posIn,next,idx):
    global done, started,spli

    with open (fileName,"r") as f:
                
        rtn=""
        seq=0
        f.read(posIn+2)
        next_char=f.read(0)
        past8=""

        pos=posIn+2
        
        while seq==0:
            pos+=1

            if len(past8)>=8:
                past8=past8[1:9]
            past8+=next_char
            #if (past8=="sequence" or past8[-3:]=="cds") or past8[-7:]=="regions":
            if (past8[-1:]=="\n"):
                seq=1
            else:
                next_char=f.read(1)
        
        rtn=f.read(next-pos)
    rtn=rtn.replace(" ","")
    rtn=rtn.replace("\n","")
    out[idx]=rtn
    done+=1
    print(rtn)
def cuteLoadingScreen():
    global all
    global done,started,spli
    count=0

    while(ready==0):
        count+=1
        print(f"\r{done}/{rtnd[0]} Finished {space}Loading{frames[count%4]:<4}",end="",flush=True)
        time.sleep(1/3)
        if count>=4:
            count=0
    print(f"\r{done}/{rtnd[0]} Finished {space}Loading{frames[count%4]:<4}",end="",flush=True)        
    print(f"\r",end="",flush=True)
    print()

  
fileName=input("Please input file:\n")    
rtnd=count()
threads=initArrayObj(rtnd[0])
out=initArrayStr(rtnd[0])
done=0
ready=0
space="     "
al=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
past8=""
seq=0
frames = ["",".","..","..."]
a=[""]



#THIS RUNS PROCESSING OF FILE
for x in range(rtnd[0]):
    threads[x]=threading.Thread(target=countSeq,args=(rtnd[1][x],rtnd[1][x+1],x))
    threads[x].start()
cuteLoadThreadt = threading.Thread(target=cuteLoadingScreen)
cuteLoadThreadt.start()
for x in threads:
    x.join()
ready=1
time.sleep(1)
print()
#END PROCESSING



#ALL BELOW PRINTS OUTPUT

aa=out
for xxx in aa:
    x=xxx.replace(" ","").lower()
    l=len(x)
    s=math.ceil(math.log10(len(x)))
    for aaa in range(25-s-math.floor((s-1)/3)):
        print(" ",end="")
    for xx in range(s):
        S=s-xx-1
        if (S+1)%3==0 and xx!=0:
            print(",",end="")
        print(math.floor(l/(10**(S)))-10*math.floor(l/(10**(S+1))),end="")
        nc=x.count("n")
    print(f"    POS: {aa.index(xxx)+1}            {nc}"       )
    ##print(l)
    a[0]=a[0]+x

    
b=[]
c=[]
for x in a:
    x=x.lower()
    b.append([math.floor( (len(x)/10)+0.5)/100,x.count("a"),x.count("g"),x.count("c"),x.count("t")])
    
s="[\n"
for x in b:
    s=s+f"[{x[0]},{x[1]},{x[2]},{x[3]},{x[4]}],\n"
    for xx in x:
        print(xx)
    print(x[1]+x[2]+x[3]+x[4]-len(a[0]))
    print("\n") 
    
s=s+"]"
print(s)
ready = 1
