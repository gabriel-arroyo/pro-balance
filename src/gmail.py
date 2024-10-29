import imaplib
import email
from email.header import decode_header


def get_product_orders():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("your_email@gmail.com", "your_password")
    mail.select("inbox")
    result, data = mail.search(None, "UNSEEN SUBJECT 'Order'")
    if data[0]:
        for num in data[0].split():
            _, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    # Extract order information from email
                    print(msg.get_payload(decode=True))
