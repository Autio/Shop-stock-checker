# Check if Prisma.fi has Playstation 5 is in stock and send an email if this is so
import os
import smtplib
import urllib.request
from email.message import EmailMessage
from bs4 import BeautifulSoup


def check_availability():
    target_page = 'https://www.prisma.fi/fi/prisma/prisma-gaming-playstation-5'
    target_phrase = 'Playstation 5-pelikonsolit tilapäisesti loppu'
    page = urllib.request.urlopen(target_page)
    soup = BeautifulSoup(page)

    if target_phrase in soup.text:
        return False
    return True
    

def main():
    available = True
    #available = check_availability()
    from_address = "petri.mikael.autio@gmail.com"
    to_address = "anssi.ekmark@gmail.com"

    if(available):
        msg = EmailMessage()
        msg['Subject'] = "PS5 hälytys"
        msg['From'] = from_address
        msg['To'] = from_address
        msg.set_content("No nyt sitä pleikkaa o.\n Kato vaikka: https://www.prisma.fi/fi/prisma/prisma-gaming-playstation-5")

        with open('credentials') as file:
            lines = file.readlines()
            username = lines[0].rstrip('\n')
            password = lines[1].rstrip('\n')
        x = 5
        
        #try: 
        server = smtplib.SMTP('mail.upbeam.net', 23)
        server.login(username, password)
        server.ehlo()
        server.starttls()
        
        server.send_message(msg)
        server.quit()
    #except: 
        print('Sending the email failed.')


main()
