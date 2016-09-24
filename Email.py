import email
import imaplib
import getpass
import smtplib

#setting the max size of the buffer value to read an email account with large number of emails.
imaplib._MAXLINE = 1000000
mail = imaplib.IMAP4_SSL('imap.gmail.com')
emailid = input("Please Enter your Gmail ID :\n")
password = getpass.getpass("Please Enter your Password :\n")
mail.login(emailid, password)
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select('Inbox') 
# connect to inbox.
print("Connected to inbox of", emailid)
result, data = mail.uid('search', None, "ALL")
list_email = data[0].split()
listlen = len(list_email)
listlen -= 1
a = listlen - 10
i=1
while ((a) < listlen) :
	result, data = mail.uid('fetch', list_email[listlen], '(RFC822)')
	raw_email = data[0][1]
	email_message = email.message_from_bytes(raw_email)
	print("[", i , "]",  email_message['From'])
	#print(email.utils.parseaddr(email_message['From']))
	#print(email_message.items())
	listlen -= 1
	i += 1

inputChoice = (input("Choose the email to read or enter [C] to compose an email:\n"))
if (inputChoice == 'c' or inputChoice == 'C') :
	reciever = input("Please enter the email address of the reciepent :\n")
	subject = input("Enter the subject of the email :\n")
	text = input("Enter the message to be sent :\n")
	txt = "From : " + emailid + "\nTo : " + reciever + "\nSubject : " + subject + "\n" + text
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(emailid, password)
	server.sendmail(emailid, reciever, txt)
	server.quit()
	mail.close()
	mail.logout()
	exit()
else :
	mailid = int(inputChoice) - 1

chosenID = listlen + 10 - mailid
print("Chosen email ID : ", chosenID)
result1, data1 = mail.uid('fetch', list_email[chosenID], '(RFC822)')

print("\n\n***** FETCHING EMAIL *****\n\n")

raw_email1 = data1[0][1]
email_message_chosen = email.message_from_string(raw_email1.decode('utf-8'))
print("FROM : ", email_message_chosen['From'])
print("TO : ", email_message_chosen['To'])
print("SUBJECT : ", email_message_chosen['Subject'])
for part in email_message_chosen.walk() :
	body = part.get_payload(decode=True)
	if body != None :
		message = body.decode('utf-8')
		message = message.replace("<BR>", "\n")
		print("MESSAGE : ", message)
print("ID of email : ", chosenID)
print("\n\n***** END OF EMAIL *****\n")
choice = input("Enter [R] to reply [D] to Delete or [X] to log out and exit :\n")

if (choice == "x" or choice == "X") :
	mail.logout()
	print("Logged out of email.")
elif (choice == "d" or choice == "D") :
	print("Deleting Email...")
	newchosenID = listlen + 11 - mailid
	mail.store(str(newchosenID), '-X-GM-LABELS', '\\Inbox')
	mail.store(str(newchosenID), '+X-GM-LABELS', '\\Trash')
	mail.store(str(newchosenID), '+FLAGS', '\\Deleted')
	print("Email Deleted")
	print(mail.expunge())
	print("All fnctions complete...")
elif (choice == "r" or choice == "R") :
	reciever = email_message_chosen['From']
	subject = "Re: " + email_message_chosen['Subject']
	text = input("Enter the message to be sent :\n")
	txt = "From : " + emailid + "\nTo : " + reciever + "\nSubject : " + subject + "\n" + text
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(emailid, password)
	server.sendmail(emailid, reciever, txt)
	server.quit()
	mail.close()
	mail.logout()
	exit()

