import sys
import smtplib
import easyimap
import imaplib,re
import speech_recognition as sr
import pyttsx3
from email.mime.text import MIMEText

r = sr.Recognizer()
r.energy_threshold=2500

smtp_ssl_host='smtp.gmail.com'
smtp_ssl_port=465

ch=0
op={'send':1,'read':2,'search':3,'logout':4}

def speakout(label):
    engine=pyttsx3.init()
    engine.say(label)
    engine.runAndWait()

def verify(text):
    try:
        with sr.Microphone() as source:
            speakout("you have entered")
            speakout(text)
            speakout("Say Yes to continue and No to reenter")
            audio = r.record(source,duration=4)
        text=r.recognize_google(audio)
        return text
    except:
        speakout('Sorry could not recognise Please Try again')
        text=verify(text)
    return text

def voice(label):
    with sr.Microphone() as source:
        speakout(label)
        audio = r.record(source,duration=5)
    text=r.recognize_google(audio)
    text=text.split(' ')
    for i in range(len(text)):
        if(text[i]=="at")or(text[i]=="attherate"):
            text[i]="@"
    text=''.join(text)
    msg=text
    print(msg)
    if(verify(text)=="yes"):
        return msg
    else:
        msg=voice(label)
    return msg

def voicesub(label):
    with sr.Microphone() as source:
        speakout(label)
        audio = r.record(source,duration=8)
    text=r.recognize_google(audio)
    print(text)
    return text

def voicebody(label):
    with sr.Microphone() as source:
        speakout(label)
        audio = r.record(source,duration=15)
    text=r.recognize_google(audio)
    print(text)
    return text

        
def voicemenu():
    try:
        with sr.Microphone() as source:
            audio = r.record(source,duration=6)
        text=r.recognize_google(audio)
    except:
        speakout('Sorry could not recognise Please try again')
        text=voicemenu()
    print(text)
    return text

def send(username,password):
    try:
        print('Sending Email')
        sender = username
        print('Enter recipient email address')
        targets = voice('Enter recipient email address')
        print('Enter subject')
        sub=voicesub('Enter subject')
        body=voicebody('Enter the Message to be sent')
        print('Enter the Message to be sent')
        msg = MIMEText(body)
        msg['Subject']=sub
        msg['From']= sender
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username,password)
        server.sendmail(sender, targets, msg.as_string())
        server.quit()
        speakout('Message successfully Sent')
    except:
        speakout('Message not Sent')

def read(username,password):
    print('Reading out all unread emails')
    i=imaplib.IMAP4_SSL('imap.gmail.com')
    i.login(username,password)
    x,y=i.status('INBOX','(MESSAGES UNSEEN)')
    k='MESSAGES\s+(\d+)'.encode()
    l='UNSEEN\s+(\d+)'.encode()
    mes=int(re.search(k,y[0]).group(1))
    uns=int(re.search(l,y[0]).group(1))
    speakout('you have')
    speakout(uns)
    speakout(' unread emails')
    print("Unread Emails are")
    imapper = easyimap.connect('imap.gmail.com',username, password)
    for mail_id in imapper.unseen(uns):
        speakout('Mail from')
        speakout(mail_id.from_addr)
        print("Mail from :",mail_id.from_addr)
        speakout('subject')
        speakout(mail_id.title)
        print('Subject :',mail_id.title)
        speakout('Message')
        speakout(mail_id.body)
        print("Message :",mail_id.body)
    if(uns!=0):
        speakout('All unread emails are read')

def search(username,password):
    print('enter a username to search mails')
    search=voice('enter a username to search mails')
    count=0
    imapper = easyimap.connect('imap.gmail.com',username, password)
    for mail_id in imapper.listids(limit=5):
        mail = imapper.mail(mail_id)
        if(mail.from_addr.find(search)!=-1):
            count=count+1
    print(count)
    speakout('You have')
    speakout(count)
    speakout('emails with given username')
    print("You have",count,"emails with given username")
    for mail_id in imapper.listids(limit=5):
        mail = imapper.mail(mail_id)
        if(mail.from_addr.find(search)!=-1):
            speakout('Mail Form')
            speakout(mail.from_addr)
            print("Mail from :",mail.from_addr)
            speakout('Subject')
            speakout(mail.title)
            print('Subject :',mail.title)
            speakout('Message ')
            speakout(mail.body)
            print("Message :",mail.body)

def menu():
    print("Menu :")
    print('say Send to send an email')
    print('say read to check for unread emails')
    print('say Search to search a recepient related email')
    print('say logout to logout and close')
    speakout('say Send to send an email')
    speakout('say read to check for unread emails')
    speakout('say Search to search a recepient related email')
    speakout('say logout to logout and close')
    print("Speakout an Instruction :")
    try:
        z=voicemenu()
        return op[z]
    except:
        speakout('Sorry could not recognise Please Try again')
        return menu()
    
#Login Credentials and validation
try:
    print("Say username")
    username=voice('enter a username')
    print("Say your password")
    password=voice('enter password')
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    z=server.login(username,password)
    server.quit()
except:
    print("Login Failed")
    print("Due to Wrong Credentails or Network Failure")
    print("Try Again Later")
    speakout('Login Failed please try again later')
    sys.exit()
speakout('Login Successful')
print('Login Successful')
while(ch<4):
    ch=menu()
    if(ch==1):
        send(username,password)
    elif(ch==2):
        read(username,password)
    elif(ch==3):
        search(username,password)
    else:
        speakout('Logout Successful')
        print('Logout Successful')
        break