import requests, time, smtplib

trigger = 1
sender = 'almaz@super_company.com'
receivers = 'cool@company.com'
message = """From: almaz@super_company.com
To: cool@company.com
Subject: Site availability

Site is unavailable.
"""

while True:
    try:
        requests.get('https://www.googleccczzz.com')
        trigger = 1
    except:
        if trigger == 1:
            smtpObj = smtplib.SMTP('localhost:1025')
            smtpObj.sendmail(sender, receivers, message)
            avail = 0
    time.sleep(60)