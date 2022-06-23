import email, imaplib, time
from email.header import decode_header

"""
email-manager.py contain all the function that manage the email. 
Setted mail is an amps-llc domain.
"""

#Return a dictionary that contain a dictionary (from, subject, body) that contain all emails
def get_emails (username: str, password: str):

    """
    get_emails read all email from the mial domain and return a dictionary with information.
    :param username: string with username
    :param password: string with password
    :return: Dictionary with 3 list: from, subject, body
    """
    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4("seth49.seeweb.it")
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    # total number of emails
    messages = int(messages[0])

    mails= {"from":[], "subject":[], "body":[]}

    for i in range(messages, 0, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)

                mails["from"].append(From)
                mails["subject"].append(subject)

                # if the email message is multipart
                charset = msg.get_content_charset()
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode(charset, 'ignore')
                            mails["body"].append(body)
                        except:
                            pass
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode(charset, 'ignore')
                    mails["body"].append(body)

    return mails


def get_tmp_pwd_from_emails (mails: dict):

    """
    This function read email and search the temporary password send from cardiocalm.
     In case the text mail change, subject_target must be changed
    :param mails: dictionary wit 3 list: from, subject, body
    :return: string wit temp password
    """

    subject_target="credenziali telecardiologia 2/2: password"

    for i in range(len(mails["subject"])):
        if subject_target == mails["subject"][i]:
            mail_body = str(mails["body"][i]).replace("\n","")
            mail_body=mail_body.replace("\r", "")
            mail_body = mail_body.replace(" ", "")
            i = mail_body.find("eseguireleistruzioni.")
            if i > 0:
                password_tmp = mail_body[i - 8:i]

    return password_tmp


def await_receipt_of_email (username, password):

    """
    This functio wait until a mail is receved.
    :param username: str
    :param password: str
    """
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4("seth49.seeweb.it")
    # authenticate
    imap.login(username, password)
    messages=0
    while messages<1:
        status, messages = imap.select("INBOX")
        # total number of emails
        messages = int(messages[0])
        if messages<1:
            time.sleep(10)


def delete_all_emails (username: str, password: str):
    """
    This function simply delete all email in mail domain
    :param username: str
    :param password: str
    :return:
    """

    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4("seth49.seeweb.it")
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")

    typ, data = imap.search(None, 'ALL')
    for num in data[0].split():
        imap.store(num, '+FLAGS', '\\Deleted')
    imap.expunge()
    imap.close()
    imap.logout()