#!/usr/bin/python3.4

import requests
import smtplib
import time
import imaplib
import email
import urllib
import logging
import os
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from_email = "user_email_address"
from_pwd = "password"
smtp_server = "imap.gmail.com"
smtp_port = 993


mail = imaplib.IMAP4_SSL(smtp_server, smtp_port) 
mail.login(from_email,from_pwd)
mail.select('inbox', readonly = True)


today_date = datetime.strftime(datetime.now() - timedelta(1), '%d-%b-%Y') # https://stackoverflow.com/questions/30483977/python-get-yesterdays-date-as-a-string-in-yyyy-mm-dd-format/30484112

today_date = datetime.today().strftime('%d-%b-%Y')


type, data = mail.search(None,  'FROM', '"target_email"', "ON " + today_date.format (time.strftime("%d-%b-%Y"))) # https://stackoverflow.com/questions/28597779/how-to-filter-gmail-imap-messages-for-date-in-python


mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]# converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)# downloading attachments
    body = email_message.get_payload()[0].get_payload(decode=True)# get the body of the email
    soup = BeautifulSoup(body, 'html.parser') # convert to html
    anchors = soup.find_all('a')
    for anchor in anchors:
        url = anchor['href']

myfile = requests.get(url, allow_redirects=True) # create requests to access the url
open('/home/ubuntu/ExternalData/moengage/' + today_date + '.zip', 'wb').write(myfile.content) # save the file in zip format