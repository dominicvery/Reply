import pytest
from Validation_functions import *
import pandas as pd


df = pd.DataFrame({
        "username":["test1", "test2"], "email":["test1@1.com", "test2@2.com"]
    })

def test_credit_card():

    assert check_card_number("1234567891234567") == True    #16 digits
    with pytest.raises(Exception):    #16 digits with letters
        check_card_number("ab34567891234567")
    with pytest.raises(Exception):    #Not 16 digits
        check_card_number("123")
    with pytest.raises(Exception):    #Null
        check_card_number(None)
    with pytest.raises(Exception):    #Empty
        check_card_number()

def test_email_format():

    assert check_email_format("test@google.com") == True
    with pytest.raises(Exception):
        check_email_format("")      #empty
    with pytest.raises(Exception):
        check_email_format(None)    #null
    with pytest.raises(Exception):      #incorrect
        check_email_format("google.com")

def test_email_unique():

    assert check_email_unique("test@google.com", df)
    with pytest.raises(Exception):
        check_email_unique("test1@1.com", df)

def test_username_format():
    
    assert check_username_format("test1") == True
    with pytest.raises(Exception):    #spaces
        check_username_format("Test 1")
    with pytest.raises(Exception):    #symbols
        check_username_format("Test1%")
    with pytest.raises(Exception):    #Empty
        check_username_format("")
    with pytest.raises(Exception):    #null
        check_username_format(None)

def test_username_unique():
    assert check_username_unique("unique", df)
    with pytest.raises(Exception):
        check_username_unique("test1", df)

def test_dob():
    assert check_dob("2007-05-18") #over 18
    with pytest.raises(Exception):
        assert check_dob("2009-05-18") #under 18
    with pytest.raises(Exception):
        assert check_dob("2009.05.18") #Incorrectly formatted
    

def test_amount():

    assert check_amount(123) == True    #3 digits
    with pytest.raises(Exception):      #string
        check_amount("12a")
    with pytest.raises(Exception):    #4 digits
        check_amount(1000)
    with pytest.raises(Exception):    #2 digits
        check_amount(99)
    with pytest.raises(Exception):    #None
        check_amount(None)

def test_card_match():

    user_data1=[{"username":"test1", "credit_card":"123456789123456"},
    {"username":"test2", "credit_card":"0000000000000000"}]

    assert check_card_match("123456789123456", user_data1) == "test1"    #match

    with pytest.raises(Exception):    #no match
        check_card_match("1111111111111111", user_data1)


def test_payment_date():
    assert check_payment_date("2025-05-18") #correct
    with pytest.raises(Exception):
        assert check_payment_date("2026-05-18") #In the future
    with pytest.raises(Exception):
        assert check_payment_date("2009-15-18") #Incorrectly formatted


