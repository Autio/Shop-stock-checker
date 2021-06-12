# Check if Prisma.fi has Playstation 5 is in stock and send an email if this is so
import json
import smtplib
import urllib.request
from datetime import datetime
from email.message import EmailMessage
from bs4 import BeautifulSoup

log = ""

def check_availability():
    global log
    try:
        target_page = 'https://www.prisma.fi/fi/prisma/prisma-gaming-playstation-5'
        target_phrase = 'Playstation 5-pelikonsolit tilapäisesti loppu'
        page = urllib.request.urlopen(target_page)
        soup = BeautifulSoup(page)

        if target_phrase in soup.text:
            return False
        return True
    except:
        log += "Error parsing website "
    
def main():
    global log
    available = check_availability()
    logfile = open('log.txt', 'r+')
    successmessage = "PS5 looks to be available! "

    # Check if the PS5 has already been spotted once
    # Note, the log needs resetting if you want this process to continue
    if successmessage in logfile.read():
        print("PS5 already found")
        return

    if(available):    
        log += successmessage
        try:
            with open('credentials') as file:
                config = json.load(file)
                username = config['username']
                password = config['password']
                from_address = config['fromAddress']
                to_address = config['toAddress']
        except: 
            log += "Error with credentials file "      
        
        msg = EmailMessage()
        msg['Subject'] = "PS5 hälytys"
        msg['From'] = from_address
        msg['To'] = to_address
        msg.set_content("No nyt sitä pleikkaa o.\nKato vaikka: https://www.prisma.fi/fi/prisma/prisma-gaming-playstation-5")

        try: 
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(username, password)

            server.send_message(msg)
            server.quit()

            log += "Message sent! "
        except: 
            log += "Error sending email "
    else:
        log += "No PS5 seems to be available "
    logfile.write(str(datetime.now()) + " " + log + "\n")
    logfile.close()

if __name__ == '__main__':
    main()