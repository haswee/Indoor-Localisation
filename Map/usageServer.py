import socket 
import numpy as np
from sklearn.neighbors import KDTree
import math


def get2DIndex(dataArray, index):
  out = 0
  for x in range(0,len(dataArray)):
    if (index> (out + len(dataArray[x]))):
      out = out + len(dataArray[x])
    else:
      return (x, index-out)
  return (-1,-1)

def distance(array1,array2):
  dist = 0
  for x in range(0,3):
    dist = dist + math.pow(float(array1[x])-float(array2[x]),2)
  return math.sqrt(dist)

def returnBestMatch(stack):
  ansArray= []
  for x in stack:
    avg = 0
    for y in x:
      avg = avg + y[-1]
    if len(x)==0:
      avg =0
    else:
      avg = avg/len(x)
    ansArray.append(avg)
  return ansArray.index(min(ansArray))   


f=open("map_p.txt", "r")
data= f.read()
listOfData = data.split("\n")
dataArray = [] 
magArray = []

last = listOfData[-1].split(",")

for x in range(0,int(last[2])): #total number of paths in the floor
  dataArray.append([])

for x in listOfData:
  a = x.split(",")
  dataArray[int(a[2])-1].append(a)
  float_a = []
  for y in range(len(a)-3,len(a)):
    float_a.append(float(a[y]))
  magArray.append(float_a)

dataArray = np.array(dataArray)
magArray = np.array(magArray)
tree = KDTree(magArray)

# inputArray=[[-37.12616,-4.73938,-11.936951],[-37.026978,-5.7403564,-9.191895],[-34.327698,2.9891968,-1.0375977],[-25.396729,17.036438,2.6916504]]
# # inputArray=[[-37.026978,-5.7403564,-9.191895],[-34.327698,2.9891968,-1.0375977],[-25.396729,17.036438,2.6916504]]
# inputArray = np.array(inputArray)

history = []
stepsWalked = 0

s = socket.socket()
import json
port = 3000
s.bind(('', port))
print ("Show is on %s" %(port))


j=0
while 1:
  s.listen(5)
  print(j)
  j+=1
  print ("socket is listening")
  c, addr = s.accept() 
  print ('Got connection from', addr )
  data= c.recv(1024).decode("utf-8") 
  inputArray = data.split(",")
  x = inputArray[len(inputArray)-3:] 
  print("input: "+str(x))
  print("History: "+str(history))
  stepsWalked=stepsWalked+1

  if stepsWalked<3:
    history.append(x)
    dist, ind = tree.query([x], k=2)
    start = -100
    (a,b) = get2DIndex(dataArray,ind[0][0])
    print("best match: "+ str(ind[0][0]) + " "+ str(a) + ","+str(b))
    st = ",".join([dataArray[a][b][3],dataArray[a][b][4]])
    st = str(start) +","+ st
  else:
    dist, ind = tree.query([x], k=2)
    stack = [[],[],[],[]]
    iteri = 0
    for y in ind[0]:
      i = -2
      (a,b) = get2DIndex(dataArray,y)
      while i!=3:
        if (((b+i) > (-1)) and ((b+i) < len(dataArray[a]))):
          if i==0:
            stack[iteri].append([y,a,b+i, distance(x,dataArray[a][b][-3:])])
            iteri = iteri + 1
            stack[iteri].append([y,a,b+i, distance(x,dataArray[a][b][-3:])])
          else:
            stack[iteri].append([y,a,b+i, distance(history[abs(abs(i)-2)],dataArray[a][b+i][-3:])])
        i=i+1
      iteri = iteri + 1
    # print(returnBestMatch(stack))
    match = returnBestMatch(stack)
    matchArray = []
    for k in stack[match]:
      a,b = k[1],k[2]
      matchArray.append(dataArray[a][b][3])
      matchArray.append(dataArray[a][b][4])

    start = 0
    if len(stack[match])<2:
      start = 0
    else:
      start = stack[match][0][2]-stack[match][1][2]
    
    print("best match: "+ str(stack[match]))


    st = ",".join(matchArray)
    st = str(start)+","+ st
    history.pop(0)
    history.append(x)
    print("History: "+str(history))

  print(st)
  c.send(st.encode('utf-8')) 
  c.close()