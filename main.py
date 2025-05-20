from Validation_functions import *
from analysis_functions import *
import pandas as pd

def main():

    payments_path= "Data/payments.json"
    users_path = "Data/users.json"

    #load json and df for users and payments
    user_data = get_json(users_path)
    payment_data = get_json(payments_path)
    users = pd.DataFrame(columns=["username", "email", "age", "has_credit_card"])
    payments = pd.DataFrame(columns=["username", "amount", "transaction_date"])

    #create valid_users array so credit card number can be checked without storing in the df
    valid_users=[]

    #iterate over users and add to df if no exceptions raised
    for user in user_data:
        #check json correctly formatted
        try:
            check_user_format(user)
        except Exception as e:
            print("invalid user format")
            continue
        try:
            user["age"], user["has_credit_card"] = user_validation(user, users)
            valid_users.append(user)
        except Exception as e:
            print(f"Invalid user:{user}:{e}")
            continue
        users.loc[len(users)] = user

    #iterate over payments, validate entries and match card number to valid_users
    for payment in payment_data:
        #check json correctly formatted
        try:
            check_payment_format(payment)
        except Exception as e:
            print("invalid payment format")
            continue
        try:
           payment_validation(payment)
           payment["username"] = check_card_match(payment["credit_card"], valid_users)
        except Exception as e:
            print(f"Invalid payment:{payment}:{e}")
            continue
        payments.loc[len(payments)] = payment

    #run analysis
    analysis(users, payments)

if __name__ == "__main__":
    main()



