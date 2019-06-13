import sys
delimiter = "/"
if (sys.platform == "win32"):
    delimiter = "\\"

cle = sys.argv[1]

file = sys.argv[2]

if (len(sys.argv) > 3 and sys.argv[3] == "utf8"):
    content = open(file,"r", encoding='utf8').read()
else:
    content = open(file,"r").read()

contentDecrypted = ""

i = 0
while (i<len(content)):
    firstChar = ord(cle[i%len(cle)])
    contentDecrypted += chr((ord(content[i])-firstChar)%1425)
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

newFile = path+filename+"_decrypted."+ext

file = open(newFile,"w", encoding='utf8')
file.write(contentDecrypted)