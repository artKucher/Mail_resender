from config import *
import imaplib

def checkMailbox(lastMessageId):
    mail_box = imaplib.IMAP4_SSL(imap_host)
    mail_box.login(user, passwd)





    foldersList = ["INBOX"]
    #for i in mail_box.list('""', 'INBOX/*')[1]:
        #foldersList.append(i.decode().split(' "/" ')[1])
    raw_datas = []
    maxId = -1
    for folder in foldersList:
        mail_box.select(folder, readonly=True)
        _, data = mail_box.uid('search', None, 'UID ' + str(lastMessageId +1) + ':*')
        messageIdsList = data[0].decode().split()

        if messageIdsList == []:
            continue

        if int(messageIdsList[-1]) > maxId:
            maxId = int(messageIdsList[-1])
        #indexLastKnownMessage = getFirstNewMsgIndex(messageIdsList,lastMessageId)
        #trim to choose only new messages
        #messageIdsListNew = messageIdsList[indexLastKnownMessage:]

        for mail_id in messageIdsList:
            _, data = mail_box.uid('fetch', mail_id, '(RFC822)')
            raw_datas.append(data)

    #return raw datas of new messages and last new message Id
    return raw_datas, maxId

def getFirstNewMsgIndex(messageIdsList, lastMessageId):
    counter = 0
    for id in messageIdsList:
        if int(id)>int(lastMessageId):
            return counter
        counter +=1
    return len(messageIdsList)
