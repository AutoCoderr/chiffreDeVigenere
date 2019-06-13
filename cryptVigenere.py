import sys
delimiter = "/"
if (sys.platform == "win32"):
    delimiter = "\\"

cle = sys.argv[1].replace("_"," ")

file = sys.argv[2]

if (len(sys.argv) > 3 and sys.argv[3] == "utf8"):
    content = open(file,"r", encoding='utf8').read()
else:
    content = open(file,"r").read()

contentCrypted = ""

i = 0
while (i<len(content)):
    firstChar = ord(cle[i%len(cle)])
    contentCrypted += chr((firstChar+ord(content[i]))%1425)
    i += 1

filename = ""
i = len(file)-1
while(file[i] != delimiter and i >= 0):
    filename = file[i] + filename
    i -= 1

ext = filename.split(".")[-1]
filename = filename.split(".")[0]

path = ""
j = 0
while(j<=i):
    path += file[j]
    j += 1

newFile = path+filename+"_crypted."+ext

print ("file => "+newFile)

file = open(newFile,"w", encoding='utf8')
file.write(contentCrypted)

