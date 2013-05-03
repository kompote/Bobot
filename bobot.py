###
### TODO:
    ### - tag smileys & ponctuation
    ### - ajoute . en fin de phrase

from random import *
import sys

pre = 'pre'
post = 'post'

class Bobot():
        
    def __init__(self):
        self.database = []
        self.datapair = []
        self.lastword = "l'anus"

    def save_bases(self):
        print("Saving Bases...")
        file = open('datapair.bin','w')
        for i in self.datapair:
            #file.write(" ".join(str(i))+"\n")
            file.write(i[0] + " " + i[1]+ " " + i[2] + "\n")
        file.close()
        """
        file = open('database.bin','w')
        for i in self.database:
            file.write(str(i) + "\n")
        file.close()
        print("Done.")
        """
        
    def load_bases(self):
        print("Load Bases...")
        self.database = []
        self.datapair = []
        file = open('datapair.bin','rb')
        print("Load datapair...")
        lines = file.readlines()
#        print("Load datapair...1")
        for line in lines:
            tmp = line.split()
            self.datapair.append([tmp[0].decode('latin-1','ignore'),tmp[1].decode('latin-1','ignore'),tmp[2].decode('latin-1','ignore')])
#            print(line.decode('latin-1','ignore'))
#        print("Load datapair...2")
        file.close()
        """
        print("Load database...")
        file = open('database.bin','r')
        lines = file.readlines()
        for line in lines:
#            tmp = line.split()
            self.database.append(line)
        file.close()
        """
        print("Done.")


    def get_infos(self):
        insultlist=[u"connard",u"batârd",u"sale con",u"petit con",
                    u"petite merde de rat", u"pet de fouffe",
                    u"chacal", u"tapette", u"petite bite",
                    u"enculeur de mouches"]
        message = "Je connais " + str(len(self.database)) + " mots (" + str(len(self.datapair)) +" associations), " + insultlist[randint(0,len(insultlist)-1)]
        return message
    
    def parse_phrase(self, message, parse):
#        message=message.
        print(" Parsing : " + message)
        #message = message.encode('utf-8')
        if len(message) < 4 :
           return ""
            #    message = message.replace(";",",")
            #    message = message.replace("'","' ")
            #    message = message.replace(","," , ")
        message = message.replace("!"," !")
        message = message.replace("?"," ?")
        message = message.replace("...",".")
        message = message.replace("."," .")
        #message = message.replace(" - "," . ")
        #message = message.replace("-","")
        wordlist = message.split()

        if not(wordlist[-1]== "." or wordlist[-1]== "?" or wordlist[-1]== "!") :
            wordlist.append(".")
        #wordlist[0] = wordlist[0].title()
 #       print(wordlist)
        if not parse:
            return wordlist
        #print(str(wordlist))
        for word in wordlist:
            if not word in self.database:
                self.database.append(word)
        flag = False
        if len(wordlist) < 3:
            return wordlist
#        print(len(wordlist))
        for i in range(len(wordlist)-2):
#            print("   " + str(i))
#            print("   " +wordlist[i])
#            print("   " + wordlist[i+2])
            for data in self.datapair:
                
                if (data[0]==wordlist[i] and data[1]==wordlist[i+1]and data[2]==wordlist[i+2]):
                    #self.datapair[j][3]+=1 # Nombre d'occurences
                    flag = True
                    break
                else:
                    flag = False

            if not flag:
                tmp = [wordlist[i], wordlist[i+1],wordlist[i+2]]
                self.datapair.append(tmp)

#        print(self.get_infos())
        return wordlist

    def gen_phrase(self, word):
        print("Generating... " + word)
        keyword = word
        notFound = True
        finallist = []
        tmplist = []
        datapairtmp = self.datapair[:]
        limit = 2
# "        print(str(datapairtmp))
#        print(len(self.datapair))
       #choose first pair
        while notFound and limit > 0:
            limit-=1
            for data in datapairtmp:
                if data[0]==keyword or data[1]==keyword or data[2]==keyword:
                    tmplist.append(data)
            """
            for i in range(0,len(datapairtmp)-1):
                if datapairtmp[i][0]==keyword or datapairtmp[i][1]==keyword or datapairtmp[i][2]==keyword or datapairtmp[i][0]==keyword.title() or datapairtmp[i][1]==keyword.title() or datapairtmp[i][2]==keyword.title():
                    tmplist.append(datapairtmp[i])
            """
            #print(str(tmplist))
            try:
                choosenpair = tmplist[randint(0,len(tmplist)-1)][:]
                notFound = False
                self.lastword = keyword
            except:
                try:
                    print("except! with " + str(keyword))
                    keyword = self.lastword
                except:
                    pass
        
        if notFound:
            return ""
        datapairtmp.remove(choosenpair)
#        print("ChoosenPair : " + str(choosenpair))
#choose pre
        prelist = []
        flPre = True
        lastfound = choosenpair[:]
        limit = 100
        while flPre and limit > 0:
            limit-=1
            tmplist = []
            tmplist2 = []
            flPre = False
            for data in datapairtmp:
#                print(str(data))
                if (data[1]==lastfound[0] and data[2]==lastfound[1]):
                    tmplist.append(data)
                    flPre=True
#                    print("keepit :" + str(data))

            if not flPre:
                break
            lastfound = tmplist[randrange(len(tmplist))][:]
            datapairtmp.remove(lastfound)
            if lastfound[0]=="." or lastfound[0]=="?" or lastfound[0]=="!":
                lastfound[0]=""
                break
            prelist.append(lastfound)

        prelist.reverse()
#        print("Prelist : " + str(prelist))
        if prelist:
            for pre in prelist:
                finallist.append(pre[0])
              #  finallist.append(pre[1])
 
        finallist.append(choosenpair[0])
        finallist.append(choosenpair[1])
        finallist.append(choosenpair[2])

            #    print(finallist)
            #    print("Do post ")
            
        postlist = []
        flPost = True
        lastfound = choosenpair[:]

        limit = 100
        while flPost and limit > 0:
            limit-=1
            tmplist = []
            tmplist2 = []
            flPost = False
#            print(str(datapairtmp))
#            print(len(datapairtmp))
            for data in datapairtmp:
                if (data[0]==lastfound[1] and data[1]==lastfound[2]):
                    tmplist.append(data)
                    flPost=True

            """
            for i in range(0,len(datapairtmp)-1):
                print("check : " + str(i) + " " + str(datapairtmp[i]))
#                if datapairtmp[i][0]==lastfound[2] or (datapairtmp[i][0]==lastfound[1] and datapairtmp[i][1]==lastfound[2]):
                if (datapairtmp[i][0]==lastfound[1] and datapairtmp[i][1]==lastfound[2]):
                    tmplist.append(datapairtmp[i])
                    flPost=True
                    print("keepit")
            """
            if not flPost:
                break
            lastfound = tmplist[randint(0,len(tmplist)-1)]
#            print("lastfound : " + str(lastfound))
            datapairtmp.remove(lastfound)
            postlist.append(lastfound)
            if lastfound[2]=="." or lastfound[2]=="?" or lastfound[2]=="!":
                break

#        print("PostList : " + str(postlist))
        if postlist:
            for post in postlist:
#                finallist.append(post[1])
                finallist.append(post[2])

#            finallist.append(postlist[-1][2])

#    finallist[0]=''
        finalstr=" ".join(finallist)
        finalstr = finalstr.replace(" .",".")
        finalstr = finalstr.replace(" !","!")
        finalstr = finalstr.replace(" ?","?")
#        print("Final response : " + finalstr)
        print("Done.")
        return finalstr


if __name__ == "__main__":
    bb = Bobot()    
    if "--help" in sys.argv:
        print("Tu veux de l'aide? Ta mere en string.")
        sys.exit(0)
    start = 3
    while True:
        foo=input("? ")
        if foo == "!q":
            break
        if foo == "!words":
            print("I know :")
            print(bb.get_infos())
            continue
        if foo == "!data ":
            for t in bb.datapair:
                print(str(t))
            continue
        mess=bb.parse_phrase(foo,True)
        if  start>0:
            start-=1
        else:
            #mess=mess.split()
            word=mess[randint(0,len(mess)-1)]
            try:
                print(bb.gen_phrase(word))
            except:
                print("raté!")
                pass
# code...     

#  f = open("text.txt",'r')
##  for line in f:
    ##      parse_phrase(line)
    #
    #
    #  
    ##  print("self.database lenght : ")    
    ##  print(len(self.database))
    ##  print("self.datapair lenght : ")    
    ##  print(len(self.datapair))

#   gen_phrase("il")
#    gen_phrase("elle")
#    gen_phrase("rentrez")

