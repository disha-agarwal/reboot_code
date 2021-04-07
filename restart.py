def getIP():
    import socket
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def restoreNumRebootsFromFile(stateFileName):
    numRebootsSoFar = 0
    import os.path
    if(os.path.isfile(stateFileName)):
        f = open(stateFileName, "r")
        numRebootsSoFar = f.readline().split()[0]
        f.close()
    return numRebootsSoFar


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
        nodeNum = generators[self.currGeneratorIdx][1][self.nextGeneratedNumIdx]
        if(self.nextGeneratedNumIdx == n):
            self.nextGeneratedNumIdx = 0
            self.currGeneratorIdx = (self.currGeneratorIdx + 1)% len(generators)
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
        print(self.currNodeIdx)
        self.numRebootsSoFar = restoreNumRebootsFromFile(stateFileName)
        print(self.numRebootsSoFar)




ips = ["172.31.8.98", "172.31.37.196", "172.31.35.132", "172.31.45.217"]
attackTime = 60
rebootTime = 10
t = 2
stateFileName = "reboot_state"
n = 17
nodePicker = RandomNodePicker(n)
print(nodePicker.generators)
algo = Algorithm(ips,n,attackTime,rebootTime,t,nodePicker,stateFileName)