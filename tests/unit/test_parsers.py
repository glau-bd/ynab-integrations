from src.index import parse_message
from src.utils.models import Transaction


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

    assert parse_message(email_body) == Transaction(
        account_id="091cf36a-e101-4c64-9622-51dd02c7c3c5",
        amount=1234,
        timestamp=1688457305.775607,
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


A transaction of SGD .99 was made with your UOB Card ending 5290 on
11/06/23 at BUS/MRT. If unauthorised, call 24/7 Fraud Hotline now
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
    assert parse_message(email_body) == Transaction(
        account_id="7571454c-6306-4ec2-99b6-37780a7811f6",
        amount=99,
        timestamp=1688400000.0,
        payee_id=None,
        payee_name="BUS/MRT",
        category_id=None,
        cleared=None,
        flag_color=None,
        approved=False,
    )
