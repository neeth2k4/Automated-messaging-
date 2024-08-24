import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables from a .env file (if used)
load_dotenv()

# Email configuration using environment variables for security
sender_email = os.getenv('SENDER_EMAIL')  # Your email address
receiver_email = os.getenv('RECEIVER_EMAIL')  # Recipient's email address
password = os.getenv('EMAIL_PASSWORD')  # Your email password or app-specific password
smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')  # SMTP server (default to Gmail's)
smtp_port = int(os.getenv('SMTP_PORT', 587))  # SMTP port (default to 587 for TLS)

# Email content configuration
subject = "Automated Notification"  # Email subject
body = "<h2>This is an automated email notification</h2> <p>This email is sent from a Python script.</p>"  # HTML content of the email
attachment_path = "path/to/your/attachment.pdf"  # File path to an attachment (optional)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the email content
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

# Attach the HTML body to the email
message.attach(MIMEText(body, 'html'))  # Use 'plain' for plain-text emails

# Attach a file (optional)
if attachment_path:
    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )
        message.attach(part)
        logging.info(f"Attached file: {attachment_path}")
    except Exception as e:
        logging.error(f"Failed to attach file: {e}")

# Send the email
try:
    # Establish a secure session with the SMTP server using your credentials
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())
    logging.info(f"Email sent to {receiver_email}!")

except Exception as e:
    logging.error(f"Failed to send email. Error: {e}")
finally:
    # Terminate the SMTP session and close the connection
    server.quit()
    logging.info("SMTP session terminated.")
