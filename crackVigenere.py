import sys
import os

delimiter = "/"
if (sys.platform == "win32"):
    delimiter = "\\"

def decrypt(content,cle):

    contentDecrypted = ""

    i = 0
    while (i<len(content)):
        firstChar = ord(cle[i%len(cle)])
        contentDecrypted += chr((ord(content[i])-firstChar)%1425)
        i += 1

    return contentDecrypted


file = sys.argv[1]

repetitions = {}

if (len(sys.argv) > 2 and sys.argv[2] == "utf8"):
    content = open(file,"r", encoding='utf8').read()
else:
    content = open(file,"r").read()

if (len(content) > 1000):
    content = content[:1000]

lenRepet = 4
i = 0
while (i<len(content)-lenRepet):
    uneChaine = ""
    j = i
    while (j<i+lenRepet):
        uneChaine += content[j]
        j += 1
    espaceRepetition = lenRepet
    j = i+lenRepet
    while (j<len(content)-lenRepet):
        uneAutreChaine = ""
        k = j
        while (k<j+lenRepet):
            uneAutreChaine += content[k]
            k += 1
        j += 1
        if (uneChaine == uneAutreChaine):
            if (uneChaine in repetitions):                
                repetitions[uneChaine]["nbRepet"] += 1
            else:
                repetitions[uneChaine] = {"nbRepet": 2, "espaceRepetition": espaceRepetition}
        espaceRepetition += 1
    i += 1

diviseurs = {}

for rep in repetitions:
    i = 2
    while(i<repetitions[rep]["espaceRepetition"]):
        if (repetitions[rep]["espaceRepetition"]%i == 0):
            if (i in diviseurs):
                diviseurs[i] += 1
            else:
                diviseurs[i] = 1
        i += 1

nbMaxDiviseurs = 10

maxs = []

i = 0
while(i<nbMaxDiviseurs):
    max = 0
    for div in diviseurs:
        if(max == 0):
            max = div
        elif (diviseurs[div] >= diviseurs[max]):
            max = div
    if (max != 0):
        maxs.append(max)
        del diviseurs[max]
    i += 1

if (len(maxs) == 0):
    print ("Aucune repetitions n'a ete trouve.")
else:
    print (maxs)

exist = False
while(exist == False):
    max = int(input("Quel longueur pour la cle voulez vous supposer ? : "))
    if (len(maxs) > 0):
        exist = False
        i = 0
        while(i<len(maxs)):
            if (maxs[i] == max):
                exist = True
                break
            i += 1
    else:
        exist = True

lenKey = max

frequenceLettre = {}

i = 0
while (i<lenKey):
    frequenceLettre[i] = {}
    j = 0
    while(j<len(content)):
        if (j%lenKey == i):
            if (content[j] in frequenceLettre[i]):
                frequenceLettre[i][content[j]] += 1
            else:
                frequenceLettre[i][content[j]] = 1
        j += 1
    i += 1

nbPossibleLetter = int(input("Le nombre de lettre a tester pour chaque rang du mot cle : "))

maxs1 = {}


for i in frequenceLettre:
    maxs1[i] = []
    j = 0
    while(j<nbPossibleLetter):
        max = None
        uneLettre = ""
        for lettre in frequenceLettre[i]:
            if (max == None):
                max = lettre
            elif(frequenceLettre[i][lettre] > frequenceLettre[i][max]):
                max = lettre
        maxs1[i].append(max)
        del frequenceLettre[i][max] 
        j += 1

bestLetter = " " #on suppose que le caractere le plus utilise dans un texte non chiffre est l'espace, on va donc se baser dessus pour casser le chiffrement

rangBetter = ord(bestLetter)

maxs = {}

for l in maxs1:
    maxs[l] = []
    i = 0
    while (i<len(maxs1[l])):
        letter = maxs1[l][i]
        rang = ord(letter)
        dif = rang-rangBetter
        if (dif < 0):
            j = len(alphabetBase)+dif
        elif (dif > 0):
            j = dif
        else:
            j = 0
        maxs[l].append(chr(j))
        i += 1

print ("\nliste :")
print (maxs)


indexKeyWord = []
i = 0
while(i<lenKey):
    indexKeyWord.append(0)
    i += 1

indexKeyWordR = []
i = 0
while(i<lenKey):
    indexKeyWordR.append(0)
    i += 1

wordToSearch = input("Rentrer un mot a chercher pour mieux trouver la bonne cle : ")
displayed = []

i = 0
while(i<nbPossibleLetter**lenKey):
    keyWord = {}
    j = 0
    while(j<lenKey):
        keyWord[j] = maxs[j][indexKeyWord[j]]
        j += 1
    secretWord = ""
    for l in keyWord:
        secretWord += keyWord[l]
    present = False
    j = 0
    while(j<len(displayed)):
        if (displayed[j] == secretWord):
            present = True
            break
        j += 1
    if (present == False):
        displayed.append(secretWord)
        contentTmp = decrypt(content,secretWord)
        if (len(contentTmp.replace(wordToSearch,"")) != len(contentTmp)):
            print ("Essayez : '"+secretWord+"' ("+str((len(contentTmp)-len(contentTmp.replace(wordToSearch,"")))/len(wordToSearch))+")")
        elif (wordToSearch == ""):
            print ("Essayez : '"+secretWord+"'")

    r = len(indexKeyWord)-1
    while (r >= 0):
        if (indexKeyWord[r] < nbPossibleLetter-1):
            indexKeyWord[r] += 1
            r = -1
        else:
            indexKeyWord[r] = 0
            r -= 1

    keyWord = {}
    j = 0
    while(j<lenKey):
        keyWord[j] = maxs[j][indexKeyWordR[j]]
        j += 1
    secretWord = ""
    for l in keyWord:
        secretWord += keyWord[l]
    present = False
    j = 0
    while(j<len(displayed)):
        if (displayed[j] == secretWord):
            present = True
            break
        j += 1
    if (present == False):
        displayed.append(secretWord)
        contentTmp = decrypt(content,secretWord)
        if (len(contentTmp.replace(wordToSearch,"")) != len(contentTmp)):
            print ("Essayez : '"+secretWord+"' ("+str((len(contentTmp)-len(contentTmp.replace(wordToSearch,"")))/len(wordToSearch))+")")

    r = 0
    while (r < len(indexKeyWordR)):
        if (indexKeyWordR[r] < nbPossibleLetter-1):
            indexKeyWordR[r] += 1
            r = len(indexKeyWordR)
        else:
            indexKeyWordR[r] = 0
            r += 1

    i += 1