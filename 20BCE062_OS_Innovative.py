
import numpy as np
import matplotlib.pyplot as plt
import copy 
class Process():
    def __init__(self,num,at=0,bt=0):
        self.at = at
        self.bt = bt
        self.num = num
        self.ct = 0
        self.strt = 0
        self.tat = 0
        self.wt = 0
    def printProcess(self):
        self.calctat()
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format("Process " + str(self.num),self.at,self.bt,self.ct,self.tat,self.wt))
    def getCT(self,ct):
        self.ct = ct
    def start(self,st):
        self.strt = st
    def calctat(self):
        self.tat = self.ct - self.at
        self.wt = self.tat - self.bt
        
def fcfs(ls):
    cht = []
    ls.sort(key=lambda i : i.at)
    st = ls[0].at
    for i in range(len(ls)):
        if(st < (ls[i]).at):
            (ls[i]).start((ls[i]).at)
            st = (ls[i]).at
        else:
            (ls[i]).start(st)
        st += (ls[i]).bt
        tup = (ls[i].num,ls[i].strt,ls[i].bt,st)
        (ls[i]).getCT(st)
        cht.append(tup)
        #makeGantt(cht,ls,"First Come First Serve (FCFS)")
    #print(cht)
    printProcesses(ls)
    makeGantt(cht,ls,"First Come First Serve (FCFS)")

def srtn(ls):
    d = {}
    cht = []
    ls1 = copy.deepcopy(ls)
    for i in ls:
        d[i.num] = copy.deepcopy(i)
        
    def has_arrived(t,l):
        l.sort(key=lambda i : i.bt)
        #printProcesses(l)
        #flag = False
        for i in l:
            if(t >= i.at):
                return i.num, True
        return 0, False
            
            
    def reduce_rt(num,l):
       for i in range(len(l)):
           if(l[i].num == num):
               l[i].bt = l[i].bt -1
           if(l[i].bt == 0):
               del l[i]
               return l, True
       else:
           return l, False
    def alldone(l):
        if(len(l) == 0):
            return True
        else:
            return False
    t = min([x.at for x in ls])
    #print(t)
    while (not(alldone(ls))):
        num, arri = has_arrived(t,ls)
        if(arri):
            tup = (num,t,1,t)
            t+=1
            cht.append(tup)
            #makeGantt(cht,ls1,"Shortest Remaining Time Next(SRTN)")
            ls, done = reduce_rt(num,ls)
            if(done):
                (d[num]).ct = t
        else:
            t+=1 
    #print(cht)
    makeGantt(cht,ls1,"Shortest Remaining Time Next(SRTN)")
    printProcesses([val for key,val in d.items()])
    
def printProcesses(ls):
    print("ProcessName\tAT\tBT\tCT\tTAT\tWT\n")
    avgtat = 0
    avgwt = 0
    l = len(ls)
    for i in range(len(ls)):
        ls[i].printProcess()
        avgtat += ls[i].tat
        avgwt += ls[i].wt
    print("-"*50)
    print("Average Turn Around Time : {0:.2f}ms\nAverage Waiting Time: {1:.2f}ms".format(avgtat/l,avgwt/l))
    print("-"*50)
def makeGantt(ls,ls1,algo):
    fig,gnt = plt.subplots()
    di = {}
    for i in ls:
        t = (i[1],i[2])
        ke = i[0]
        #print(t)
        if(ke in di.keys()):
            temp = di[ke]
            temp.append(t)
            di[ke] = temp
        else:
            temp = []
            temp.append(t)
            di[ke] = temp
    cnt = len(ls1)
    y_ulim = (cnt * 10)
    #print(y_ulim)
    gnt.set_ylim(0, y_ulim + 5)
    a = np.array(ls,dtype=[('num',int),('strt',int),('bt',int),('ct',int)])
    x_ulim = (np.sort(a,order="ct")[-1])[-1]
    gnt.set_xlim(0, x_ulim + 2)
    #gnt.title(str(algo))
    gnt.set_xlabel('seconds since start')
    gnt.set_ylabel('Process')
    
    t = []
    for x in range(5,y_ulim,10):
        t.append(x)
    #print(t)
    gnt.set_yticks(t)
    t = []
    for x in ls1:
        t.append(x.num)
    t.sort()
    #print(t)
    gnt.set_yticklabels(t)
    for key,val in di.items():
        gnt.broken_barh(val,((key-1)*10,10))
    gnt.set_title(str(algo).upper())
    
    plt.savefig(algo+".png")

        
    
pro  = []
while(True):
    try:
        n = int(input("Please enter the number of process: "))
        if(n >= 0):
            break
        else:
            exit(0)
            print("Invalid Number Of Process")
    except:
        n = 0
        print("Invalid Input Type")
        
for i in range(n):
    while(True):
        try:
           at = int(input("Enter Arrival Time for Process {0} : ".format(i+1)))
           if(at >= 0):
               bt = int(input("Enter Burst Time for Process {0} : ".format(i+1)))
               if(bt > 0):
                   nm = i+1
                   p = Process(nm,at,bt)
                   pro.append(p)
                   break
               else:
                   print("Enter Valid Burst Time")
           else:
               print("Enter Valid Arrival Time")
        except:
           print("Invalid Input Type")

if(n >= 0):
    print("-"*50)
    print("{0:^25}\n".format("Proccess Entered"))
    print("ProcessName\tAT\tBT\n")
    for i in pro:
        print("{0}\t{1}\t{2}".format("Process " + str(i.num),i.at,i.bt))
    print("-"*50)
    print("\n\n")
    print("-"*50)
    print("{0:^25}\n{1:^25}".format("FIRST COME FIRST SERVE(FCFS)","NON PREEMPTIVE"))
    print("*\t"*10)
    ff=copy.deepcopy(pro)
    fcfs(ff)
    print("-"*50)
    print("{0:^25}\n{1:^25}".format("SHORTEST REMAINING TIME NEXT(SRTN)","PREEMPTIVE"))
    print("*\t"*10)
    sr=copy.deepcopy(pro)
    srtn(sr)
    print("\nKey : \nAT - Arrival Time\nBT - Burst Time\nCT - Completion Time\nTAT - Turn Around Time\nWT - Waiting Time\n")
else:
    print("-"*50)
    print("Found 0 Process ... ")
    print("-"*50)

            
