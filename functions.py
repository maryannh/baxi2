from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash 
from flask_mail import Mail, Message

client = MongoClient("mongodb+srv://maryann:3j69q28gzRCbJxwo@cluster1-pdojm.mongodb.net/test?retryWrites=true")
db = client.dandelion

def get_users():
    # get list of usernames with no other info
    users = db.users.find({}, {"username": 1, "_id": 0})
    user_list = []
    for user in users: 
        username = user['username']
        user_list.append(username)
    return user_list

def get_user_emails():
    # get list of emails with no other info
    emails = db.users.find({}, {"email": 1, "_id": 0})
    email_list = []
    for email in emails: 
        email_address = email['email']
        email_list.append(email_address)
    return email_list

def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)
