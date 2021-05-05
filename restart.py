import logging
import subprocess


logging.basicConfig(filename='/home/ubuntu/reboot_code/app.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')


def getIP():
    import socket
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def findNextPrime(n):
    if(n <= 1):
        return 2
    prime = n
    while(1):
        prime += 1
        if(isPrime(prime)):
            break
    return prime

def isPrime(n):
    if (n <= 1):
        return False 
    if (n <= 3):
        return True 
    if (n%2 == 0 or n%3 == 0):
        return False
    i= 5
    while(i*i<=n):
        if(n%i ==0 or n%(i+2)==0):
            return False
        i = i+6
    return True

def getCurrNodeIdx(ips,ip):
    current_node = -1
    for i in range(len(ips)):
        if(ips[i] == ip):
            current_node = i
            break
    return current_node

class RandomNodePicker:
    def __init__(self, n):
        self.n = n
        self.prime = findNextPrime(n)
        self.generators = []
        for i in range(1,n+1):
            generatedNums = []
            generatedNums = self.findGeneratedNums(i,generatedNums)
            if(len(generatedNums) == n):
                self.generators.append((i,generatedNums))
                break
            self.currGeneratorIdx = 0
            self.nextGeneratedNumIdx = 0


    def nextNode(self):
        nodeNum = self.generators[self.currGeneratorIdx][1][self.nextGeneratedNumIdx]
        self.nextGeneratedNumIdx += 1
        if(self.nextGeneratedNumIdx == n):
            self.nextGeneratedNumIdx = 0
            self.currGeneratorIdx = (self.currGeneratorIdx + 1)% len(self.generators)
        return nodeNum

    def findGeneratedNums(self,i,generatedNums):
        generatedNumsSet = []
        powersOfiModPrime = 1
        for x in range(0,self.prime):
            if(powersOfiModPrime not in generatedNumsSet):
                generatedNumsSet.append(powersOfiModPrime)
                if(powersOfiModPrime >= 1 and powersOfiModPrime <= self.n):
                    generatedNums.append(powersOfiModPrime-1)
            powersOfiModPrime = (powersOfiModPrime * i ) % self.prime
        return generatedNums


class Algorithm:
    def __init__(self,ips, n, attackTime, rebootTime, t, nodePicker, stateFileName):
        self.ip = getIP()
        self.mIntervals = max(1,attackTime//rebootTime)
        self.currNodeIdx = getCurrNodeIdx(ips,self.ip)
        self.t = t
        self.attackTime = attackTime
        self.rebootTime = rebootTime
        self.nodePicker = nodePicker
        self.n = n 
        self.stateFileName = stateFileName
        self.numRebootsSoFar = self.restoreNumRebootsFromFile()
       
    def restoreNumRebootsFromFile(self):
        numRebootsSoFar = 0
        import os.path
        if(os.path.isfile(self.stateFileName)):
            f = open(self.stateFileName, "r")
            numRebootsSoFar = int(f.readline().split()[0])
            f.close()
        # print(numRebootsSoFar)
        logging.debug(numRebootsSoFar)
        return numRebootsSoFar

    def rebootAfterTime(self, timeToReboot):
        import time
        import os
        self.numRebootsSoFar += 1
        f = open(self.stateFileName, "w")
        f.write(str(self.numRebootsSoFar))
        f.close()
        try:
            process = subprocess.run("/home/ubuntu/redise/dise/bin/test",universal_newlines=True,capture_output=False,timeout=timeToReboot)
        except subprocess.TimeoutExpired:
            # logging.debug(process.stdout)
            print("timeout done")
        finally:
            time.sleep(20)
        

    def run(self):
        if ((self.t) < self.mIntervals):
            subsetSize = self.t
            # print("subset size: ", subsetSize, " mIntervals:",self.mIntervals)
            logging.debug("node number: "  + str(self.currNodeIdx))
            logging.debug("subset size: " + str(subsetSize) + " mIntervals:" + str(self.mIntervals))
            N = self.numRebootsSoFar*n
            while(self.nodePicker.nextNode() != self.currNodeIdx):
                N += 1
            # print("N",N)
            logging.debug("N" + str(N))
            if(self.numRebootsSoFar == 0):
                N = ((N//subsetSize) * self.mIntervals) + (N % subsetSize)
                timeToReboot = N* rebootTime
            else:
                M = N - self.n
                N = ((N//subsetSize) * self.mIntervals) + (N % subsetSize)
                M = ((M//subsetSize) * self.mIntervals) + (M % subsetSize)
                timeToReboot = (N - M-1) * self.rebootTime
            # print("timeToReboot: ", timeToReboot) 
            logging.debug("timeToReboot: " + str(timeToReboot))
            if(self.numRebootsSoFar>0):
                timeToReboot += 10
            self.rebootAfterTime(timeToReboot)

        else:
            import math
            subsetSize = int(math.ceil(self.t/self.mIntervals))
            # print("subset size: ", subsetSize, " mIntervals:",self.mIntervals)
            logging.debug("node number: "  + str(self.currNodeIdx))
            logging.debug("subset size: " +  str(subsetSize) + " mIntervals:" + str(self.mIntervals))
            N = self.numRebootsSoFar*n
            while(self.nodePicker.nextNode() != self.currNodeIdx):
                N += 1
            # print("N",N)
            logging.debug("N" + str(N))
            if(self.numRebootsSoFar == 0):
                timeToReboot = N//subsetSize * rebootTime
            else:
                M = N - self.n
                M = (M//subsetSize)*subsetSize + subsetSize
                N = (N//subsetSize)*subsetSize
                print(N,M)    
                timeToReboot = ((N-M)//subsetSize)*self.rebootTime
            
            # print("timeToReboot: ", timeToReboot) 
            logging.debug("timeToReboot: " +  str(timeToReboot))
            if(self.numRebootsSoFar>0):
                timeToReboot += 10
            self.rebootAfterTime(timeToReboot)




ips = ["10.0.0.228","10.0.0.6", "10.0.0.204", "10.0.0.135", "10.0.0.198", "10.0.0.231"]
attackTime = 120
rebootTime = 30
t = 4
stateFileName = "/home/ubuntu/reboot_code/reboot_state"
n = len(ips)
nodePicker = RandomNodePicker(n)
# print(nodePicker.generators)
logging.debug(nodePicker.generators)
algo = Algorithm(ips,n,attackTime,rebootTime,t,nodePicker,stateFileName)
while(1):
    algo.run()










#case 2
# timeToReboot = (((N//subsetSize) + (N % subsetSize)) - ((M//subsetSize) + (M % subsetSize)) ) * self.rebootTime
# if(self.numRebootsSoFar > 0):
#     self.nodePicker.currGeneratorIdx = (self.numRebootsSoFar-1) % len(self.nodePicker.generators)
#     self.nodePicker.nextGeneratedNumIdx = 0
#     while(self.nodePicker.nextNode()!= self.currNodeIdx):
#         N = N + 1
#     while(self.nodePicker.nextGeneratedNumIdx % subsetSize != 0):
#         self.nodePicker.nextNode()
# # print("Generator's state: (", self.nodePicker.currGeneratorIdx,", ", self.nodePicker.nextGeneratedNumIdx, ")" )
# nodesToWait = 0
# while(self.nodePicker.nextNode() != self.currNodeIdx):
#     nodesToWait += 1
# print("nodesToWait: ", nodesToWait)
# timeToReboot = (nodesToWait//subsetSize)*rebootTime

#case 1

