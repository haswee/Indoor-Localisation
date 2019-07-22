import socket
s = socket.socket()
port = 3000
import json
s.bind(('', port))
print ("socket binded to %s" %(port) )


j=0
while 1:
  s.listen(5)
  print(j)
  j+=1
  print ("socket is listening")
  c, addr = s.accept() 
  print ('Got connection from', addr )
  
  data= c.recv(1024).decode("utf-8")
  print(data)
  fo = open("map.txt", "a+")
  fo.write(data+";")


  # listOfReading = (data.split(",")[-1]).split("$")

  # for x in range(0,len(listOfReading)):
  #   temp = listOfReading[x].split("+")[0]
  #   if temp in not listOfBluetooth:
  #     listOfBluetooth.append(data)

  c.close()
  fo.close()
