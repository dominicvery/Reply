import re
from datetime import datetime
import json

def get_json(file):
    with open(file, "r") as readfile:
        json_data = json.loads(readfile.read())
        return json_data
    
#json user entries must include the following keys
def check_user_format(user):
    if not all(x in ["username", "email", "dob", "credit_card"] for x in user.keys()):
        raise Exception("invalid format")
    
#json payment entries must include the following keys
def check_payment_format(payment):
    if not all(x in ["credit_card", "transaction_date", "amount"] for x in payment.keys()):
        raise Exception("invalid format")

#payment validation
def payment_validation(payment):
    check_card_number(payment["credit_card"])
    check_payment_date(payment["transaction_date"])
    check_amount(payment["amount"])
    return True

#user validation
def user_validation(user, users):
    age = check_dob(user["dob"])
    check_email_format(user["email"])
    check_email_unique(user["email"], users)
    has_credit_card = check_usercard(user)
    check_username_format(user["username"])
    check_username_unique(user["username"], users)
    return age, has_credit_card

#amount must be 3 digit integer
def check_amount(amount):
    if not isinstance(amount, int) or amount not in range(100, 1000):
        raise Exception("Amount must be a 3 digit integer")
    return True

#payment date must be ISO 8601 and cannot be in the future
def check_payment_date(date):
    y,m,d = check_iso(date)
    age = get_age(y, m, d)
    if age < 0:
        raise Exception("Payment date cannot be in the future")
    return True

#Dob must be ISO 8601 and age must be over 18
def check_dob(dob):
    y,m,d = check_iso(dob)
    age = get_age(y,m,d)
    if age < 18:
        raise Exception("Must be 18 or over")
    return age

#check date is in form ISO 8601
def check_iso(date):
    try:
        y,m,d = date.split("-")
    except:
        raise Exception("Must be ISO 8601")
    if len(y) != 4:
        raise Exception("Must be ISO 8601")
    if len(m) not in [1,2] or int(m) not in range(1,13):
        raise Exception("Must be ISO 8601")
    if len(d) not in [1,2] or int(d) not in range(1,32):
        raise Exception("Must be ISO 8601")
    return y, m, d

def get_age(y,m,d):
    y_today, m_today, d_today = datetime.today().strftime('%Y-%m-%d').split("-")
    if int(m_today) - int(m) > 0:
        return int(y_today) - int(y)
    elif int(m_today) - int(m) == 0 and int(d_today) - int(d) >= 0:
        return int(y_today) - int(y)
    else:
        return int(y_today) - int(y) - 1

#email validation: regex in the form something@something.something
def check_email_format(email):
    x= re.findall(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
    if not x:
        raise Exception("incorrect email format")
    return True

def check_email_unique(email, users):
    if len(users[users["email"]==email]):
        raise Exception("Email already in use")
    return True

def check_username_format(username):
    if not username.isalnum():
        raise Exception("Username must be alphanumeric")
    return True

def check_username_unique(username, users):
    if len(users[users["username"]==username]):
        raise Exception("username already in use")
    return True

def check_usercard(user):
    if "credit_card" not in user or user["credit_card"]==None:
        return False
    check_card_number(user["credit_card"])
    return True

#card number must be 16 digits
def check_card_number(credit_card):
    if not credit_card.isdigit():
        raise Exception("Credit card must only include numbers")
    if len(credit_card)!=16:
        raise Exception("Credit card must have 16 digits")
    return True

#Find user with credit card number matching payment
def check_card_match(payment_card, users):
    for user in users:
        if "credit_card" not in user:
            continue
        elif user["credit_card"] == payment_card:
            return user["username"]
    raise Exception("No user with this payment card")
