from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash 
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient(config['Database']['MONGO_URI'])
db = client.dandelion

def get_users():
    # get list of usernames with no other info
    users = db.users.find({
        # if username key exists
        "username": { "$exists": True }
    }, {
        "username": 1, "_id": 0
    })
    user_list = []
    for user in users: 
        username = user['username']
        user_list.append(username)
    return user_list

def get_user_emails():
    # get list of emails with no other info
    emails = db.users.find({
        # if email key exists
        "email": { "$exists": True }
    }, {"email": 1, "_id": 0})
    email_list = []
    for email in emails: 
        email_address = email['email']
        email_list.append(email_address)
    return email_list

def log_users():
    db.user_log.insert_many(db.users.find({}, {"username": 1, "_id": 0}))

def get_new_users():
    present_users = db.users.find({}, {"username": 1, "_id": 0})
    previous_users = db.user_log.find({}, {"username": 1, "_id": 0})
    new_users = []
    for user in present_users:
        if user["username"] not in previous_users:
            new_users.append(user["username"])
            db.user_log.insert_one(user)
    return new_users

def email_new_users():
    # run every two minutes
    users = get_new_users()
    for user in users:
        # get email address from username
        email = db.users.find_one({"username": user})["email"]
        # send email confirmation
        msg = Message("Thanks for joining our app",                 sender=config['Mail']['MAIL_USERNAME'], recipients=[email])
        msg.body = "testing"
        mail.send(msg) 