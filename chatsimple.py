import sys
import socket
import bobot
from random import randint
from time import sleep

HOST="irc.freenode.net"
PORT=6667
NICK="GlandHumide"
IDENT="kompote"
REALNAME="Kompote"
readbuffer=""
channel = '#PT_IRM'
s=socket.socket( )
s.connect((HOST, PORT))
s.send(bytes("NICK %s\r\n" % NICK, 'utf-8'))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME),'utf-8'))
s.send(bytes("JOIN %s\r\n" % channel,'utf-8'))

one = True
bobot = bobot.Bobot()
startup = 0
run = True
replyrate = 60
parse = False
talk = True
print("Starting BOBOT...")
try:
    bobot.load_bases()
except(e):
    startup = 10
    print("No bases. Learning mode during 10 passes.")
#run = False
def send_truc(message):
    s.send(bytes('PRIVMSG ' + channel + " :" + message + "\r\n", 'utf-8'))

while run:
    readbuffer=s.recv(1024)
    try:
        readbuffer = str(readbuffer,'utf-8')
        temp=readbuffer.split("\n")
    except:
        try:
            readbuffer = str(readbuffer,'latin-1')
            readbuffer = readbuffer.encode('utf-8')
            temp=str(readbuffer, 'utf-8').split("\n")
        except:
           continue

    for line in temp:

        line=line.rstrip()
        line=line.split()
        #print(line)
        if "PING" in line:
#            print("ping!" + str(line))
            s.send(bytes("PONG %s\r\n" % line[1],'utf-8'))
            continue

        if one and not '/NAMES' in line:
            continue
        else:
#            print("ready.")
            one = False
        if '/NAMES' in line:
            continue
        if not 'PRIVMSG' in line:
            continue

        if 'NicoQuenon' in line:
            print("Ignoring")
            continue
        
        if 'TomtomLaKompote' in line[0]:
            print("parsing...")
            parse=True
        else:
            parse=False
        
            
        if '!data' in str(line):
            send_truc(bobot.get_infos())
#            s.send(bytes(bobot.get_infos(), 'utf-8'))
            continue
        if '!save' in str(line):
            bobot.save_bases()
            continue
        if '!quits' in str(line):
            bobot.save_bases()
            run=False
            continue
        if '!talk' in str(line):
            message = u"AAAAaaah, je peux enfin m'exprimer, merci."
            send_truc(message)
            talk=True
            continue
        if '!tagueul' in str(line):
            message = u"Okay je ferme ma gueule..."
            send_truc(message)
            talk=False
            continue

        if '!quiit' in str(line):
            run=False
            continue

        if '!latterlescouilles' in str(line):
            message = [u"Ouch, ça fait trop mal sale batârd de merde! Enculé!",u"Aïe putain de merde mes cyber glaouis!! Sale bâtard!!",u"HAHAHAHA, même pas mal à mon bit petite tarlouze!!",u"Raté! Comment tu peut rater mes couilles vu la taille qu'elle font!",u"AAAAAAAAAAAH NAAAAAAAAAAAN!!! MES BITS!!",u"Tu viens de me briser les boules, c'est ta mère qui ne va pas être contente..."]
            send_truc(message[randint(0,len(message)-1)])
            continue

        if '!soumission' in str(line):
            message = [u"Oui mâitre, vous êtes mon maître, je vous dois honneur, respect et soumission toute ma vie. Puis-je vous lécher les pieds?", u"Maitre, la longueur de votre penis n'a d'égale que votre immense talent de programmation", u"J'aime tellement lécher votre cul Maitre que j'ai prit goût à la merde"]
            send_truc(message[randint(0,len(message)-1)])
            continue
        if not talk:
            continue

        if '!rage' in str(line).lower():
            print(str(line[-1]))
            for i in range(0,5):
                try:
                    message = bobot.gen_phrase(str(line[-1]))
                    sleep(.05*len(message))
                    send_truc(message)
                except:
                    send_truc("Je ne connais pas ce mot")
                    break

            continue
        
            
        #print(startup)
        line = " ".join(line[3:])
        line=line[1:]
        if len(line) < 2:
            continue

#        print(line)
        if line == "" :
            continue
        if 'http:' in line:
            print("Ignoring link")
            continue
        
        try:
            woli = bobot.parse_phrase(line,parse)
        except:
            print("Except in parsing...")
            continue
                
        if randint(0, 99) < replyrate:
            tmplst=[]
            message = ""
            found = False 
            if  startup>0:
                startup-=1
                continue
            else:               
                for i in range(0,len(woli)-1):
                    word=woli[randint(0,len(woli)-1)]
                    if len(word) > 4 : 
                        found = True
                        tmplst.append(word)
                     
            if found :
                
                message = bobot.gen_phrase(tmplst[randint(0,len(tmplst)-1)])

            if message == "":
              continue

            sleep(.2*len(message))
            send_truc(message)



