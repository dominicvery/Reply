import pandas as pd

def analysis(users, payments):

    print("\nSummary:\n")

    users_with_credit_card(users)

    madepayment_over25(users, payments)

    average_purchase(payments)

    most_orders(payments)

    summary_table(users, payments)

#number of users registers with credit card
def users_with_credit_card(users):
    users_with_credit_card = len(users[users["has_credit_card"]==True])
    print(f"Number of users registered with a credit card: {users_with_credit_card} \n" )

#percentage of users over 25 who have made a payment
def madepayment_over25(users, payments):
    join = users[(users.username.isin(payments.username))]
    over25 = users[users["age"]>=25]
    madepayment_over25 = join[join["age"]>=25]
    try:
        percentage = len(madepayment_over25)/len(over25) *100
        print(f"Percentage of users over age 25 who made a payment: {round(percentage, 2)}% \n")
    except ZeroDivisionError:
        print("No users over 25")

#Average purchase amount
def average_purchase(payments):
    average_purchase = payments.loc[:, 'amount'].mean()
    print(f"Average payment amount: £{round(average_purchase, 2)} \n")

#top 3 users by total payements
def most_orders(payments):
    most_orders = payments.groupby("username")["amount"].sum().sort_values(ascending=[False]).reset_index()
    print("Top 3 users by total payment:")
    print(most_orders.head(3),"\n")

#summary table of users
def summary_table(users, payments):
    print("Summary Table:")
    df = pd.merge(users, payments.groupby("username").sum(), on="username", how="outer")
    df = df.drop(['transaction_date','age','email'], axis=1)
    df= df.replace({True: "Y", False: "N"})
    df['amount'] = df['amount'].fillna(0)
    df=df.rename(columns={'amount':'total'})
    df["made_payment"]=df.apply(lambda row: "N" if row["total"] == 0 else "Y", axis = 1)
            
    print(df)