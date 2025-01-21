from datetime import datetime
from src.index import parse_message
from src.utils.models import Transaction, Message


def test_parse_uob_paynow_message():
    email_body = """
---------- Forwarded message ---------
From: <unialerts@uobgroup.com>
Date: Wed, Jun 7, 2023 at 12:06 PM
Subject: UOB Personal Internet Banking Notification Alerts
To: <test_email@gmail.com>


You made a PayNow transfer of SGD 12.34 to PayNow ID ending with TEST_RECIPIENT at
11:48AM, 07-Jun-2023 SG Time. If unauthorised, call 24/7 Fraud Hotline.
UOB EMAIL DISCLAIMER
Any person receiving this email and any attachment(s) contained,
shall treat the information as confidential and not misuse, copy,
disclose, distribute or retain the information in any way that
amounts to a breach of confidentiality. If you are not the intended
recipient, please delete all copies of this email from your computer
system. As the integrity of this message cannot be guaranteed,
neither UOB nor any entity in the UOB Group shall be responsible for
the contents. Any opinion in this email may not necessarily represent
the opinion of UOB or any entity in the UOB Group.
"""
    message = Message(
        email_body, datetime(2024, 1, 1)
    )
    assert parse_message(message) == Transaction(
        account_id="8ad9c9a8-8b94-433d-b86e-ec3237e1f2cc",
        amount=-12340,
        timestamp=1704038400.0,
        memo="Paynow transaction to TEST_RECIPIENT",
        payee_id=None,
        payee_name="TEST_RECIPIENT",
        category_id=None,
        cleared=None,
        flag_color=None,
        approved=False,
    )


def test_parse_uob_card_message():
    email_body = """
---------- Forwarded message ---------
From: <unialerts@uobgroup.com>
Date: Sun, Jun 11, 2023 at 7:32 AM
Subject: UOB - Transaction Alert
To: <GERALD.LAU.95@gmail.com>


A transaction of SGD 16.35 was made with your UOB Card ending 8446 on 10/12/24 at MCDONALD'S (PNS). If unauthorised, call 24/7 Fraud Hotline now
UOB EMAIL DISCLAIMER
Any person receiving this email and any attachment(s) contained,
shall treat the information as confidential and not misuse, copy,
disclose, distribute or retain the information in any way that
amounts to a breach of confidentiality. If you are not the intended
recipient, please delete all copies of this email from your computer
system. As the integrity of this message cannot be guaranteed,
neither UOB nor any entity in the UOB Group shall be responsible for
the contents. Any opinion in this email may not necessarily represent
the opinion of UOB or any entity in the UOB Group.
"""
    message = Message(
        email_body, datetime(2024, 1, 1)
    )
    assert parse_message(message) == Transaction(
        account_id="fbe75e9b-2845-4b02-ac46-52350b01c3e3",
        amount=-16350,
        timestamp=1704038400.0,
        payee_id=None,
        payee_name="MCDONALD'S (PNS)",
        category_id=None,
        cleared=None,
        flag_color=None,
        approved=False,
    )


def test_parse_citi_card_message():
    email_body = """
---------- Forwarded message ---------
From: Citibank Singapore <alerts@citibank.com.sg>
Date: Mon, Jan 6, 2025 at 2:54 PM
Subject: Citi Alerts - Credit Card/Ready Credit Transaction
To: <GERALD.LAU.95@gmail.com>


Dear Customer,
We would like to inform you that there is a charge made on your Citi PremierMiles Card:


Account Number           : XXXX-XXXX-XXXX-7354
Transaction date         : 06/01/25
Transaction time         : 14:54:02
Transaction amount       : SGD5502.60
Transaction  details     : KKH PTE LTD            SINGAPORE     SGP


Thank you for using Citi Alerts.

Citibank Online
Citibank Singapore Ltd
Co.Reg. No. 200309485K

Please do not reply to this email. To view or amend your Citi Alerts Profile, simply login to Citibank Online with your username and password. Alternatively, you may call our 24-Hour CitiPhone hotline available on our Citibank website for assistance or any other enquiries.
"""
    message = Message(
        email_body, datetime(2024, 1, 1)
    )
    assert parse_message(message) == Transaction(
        account_id="59e55c96-cda8-4dba-be30-4ff2059ddbbb",
        amount=-5502600,
        timestamp=1704038400.0,
        payee_id=None,
        payee_name="KKH PTE LTD SINGAPORE SGP",
        category_id=None,
        cleared=None,
        flag_color=None,
        approved=False,
    )
