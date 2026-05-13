import os
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from smolagents import tool

# Load your dedicated Gmail credentials
load_dotenv()

@tool
def fetch_unread_newsletters(max_emails: int = 2) -> str:
    """
    Connects to the dedicated email inbox, fetches unread newsletters, 
    strips out HTML formatting, and returns the clean text.
    
    Args:
        max_emails: The maximum number of unread emails to process at once to avoid context overflow.
    """
    username = os.getenv("EMAIL_ACCOUNT")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not username or not password:
        return "Error: Email credentials not found in .env file."

    try:
        # Connect to Gmail's IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")
        
        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK" or not messages[0]:
            return "No unread newsletters found in the inbox."
            
        email_ids = messages[0].split()[:max_emails]
        digests = []
        
        for eid in email_ids:
            res, msg_data = mail.fetch(eid, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Safely decode the subject line
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    body = ""
                    # Parse the email payload to find the actual text/html
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/html":
                                html_content = part.get_payload(decode=True).decode(errors='ignore')
                                soup = BeautifulSoup(html_content, "lxml")
                                body = soup.get_text(separator="\n", strip=True)
                                break
                            elif content_type == "text/plain":
                                body = part.get_payload(decode=True).decode(errors='ignore')
                    else:
                        payload = msg.get_payload(decode=True).decode(errors='ignore')
                        if msg.get_content_type() == "text/html":
                            soup = BeautifulSoup(payload, "lxml")
                            body = soup.get_text(separator="\n", strip=True)
                        else:
                            body = payload
                            
                    # Truncate extremely long emails to protect the context window
                    body_truncated = body[:3000] + "\n...[TRUNCATED]" if len(body) > 3000 else body
                    digests.append(f"--- SUBJECT: {subject} ---\n{body_truncated}")
                    
        mail.logout()
        return "\n\n".join(digests)
        
    except Exception as e:
        return f"IMAP Connection Error: {str(e)}"