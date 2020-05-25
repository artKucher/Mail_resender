from config import *
import email
import smtplib
import re

def sendMessages(raw_datas):
    smtp = smtplib.SMTP(smtp_host, smtp_port)
    smtp.starttls()
    smtp.login(user, passwd)
    for raw_data in raw_datas:
        email_data = raw_data[0][1]
        #parse message
        message = email.message_from_bytes(email_data)
        if (checkFrom(str(message["From"])[1:-1])):
            #sendMessage
            for to_addr in to_addresses:
                ToAddrLast = message["To"]
                CcAddrLast = message["Cc"]
                # replace headers
                message.replace_header("From", from_addr)
                message.replace_header("To", to_addr)
                message.replace_header("Cc", "")
                message.replace_header("Return-Path", "")
                #add To and Cc fields in message text.
                stringMessage = message.as_string()
                endBody = stringMessage.find("</body>")
                stringMessage = stringMessage[:endBody]+\
                                "\r\n"+"_"*24+"TO"+"_"*24+"<br>"+"\r\n"+\
                                " ".join(getEmails(ToAddrLast))+"\r\n"+ \
                                "<br>"+"_"*24+"CC"+"_"*24 + "<br>"+"\r\n" +\
                                " ".join(getEmails(CcAddrLast)) + "\r\n" + \
                                "<br>" + "_" * 50 + "\r\n" + \
                                stringMessage[endBody:]
                #send mail
                #smtp.sendmail(from_addr, to_addr, stringMessage)
    smtp.quit()

#check if "from" email address is contained in list of should-be-forwarded addresses
def checkFrom(mfrom):
	for addr in addresses_to_forward:
		if mfrom.lower().find(addr)!= -1:
			return True
	return False

#parse trash string and get e-mails
def getEmails(msg):
    res = re.findall(r'(?<=<).*?(?=>)',msg)
    return res