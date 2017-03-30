#!/usr/bin/env python
import os
import smtplib
from email.mime.text import MIMEText



def sendMail(to, subject, content):
	try:
		sender = "crawler@bauman.is"

		msg = MIMEText(content)
		msg['Subject'] = subject
		msg['From'] = sender
		msg['To'] = to

		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login('script@dunb.lv',os.environ['DUNB_PASS'])
		mail.sendmail(sender, [to], msg.as_string())
	except:
		print ("Sending failed")
		return False
	else:
		print ("Mail to " + to + " sent.\nSubject: " + subject + "\nMessage: " + content)
	
	mail.quit()
	
	
#sendMail('testing')