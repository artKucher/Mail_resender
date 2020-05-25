import imap
import smtp

def main():
    f = open("lastLetterID.txt", "r")
    LLID = int(f.read())
    f.close()

    raw_datas, newLLID = imap.checkMailbox(LLID)
    if(raw_datas != []):
        smtp.sendMessages(raw_datas)

    f = open("lastLetterID.txt", "w")
    f.write(str(newLLID))
    f.close()

if __name__ == '__main__':
    main()