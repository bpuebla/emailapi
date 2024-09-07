import email.message
from imap_tools import MailBox, A
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import time
import re
import os
from bs4 import BeautifulSoup
import smtplib
from utils import readtxt

class EmailReply():
    def __init__(self):
        # Your email credentials
        self.username = os.environ.get("USERNAME")
        self.password = os.environ.get("PASSWORD")
        self.mail_url = os.environ.get("IMAP_URL")

        self.mailbox = MailBox(self.mail_url).login(self.username, self.password, 'INBOX')
        self.path_in_template = "in_template.txt"
        self.path_out_template = "out_template.txt"
    
    def reply(self, msg):
        """
        
        Main execution of reply to emails.
        
        """
        # Read templates
        in_template = readtxt(self.path_in_template)
        out_template = readtxt(self.path_out_template)
        
        # Extract variables from template
        data = self.parse_email(in_template, msg)
        
        # Return error if unable to parse
        if data.get('error'):
            print('Error', data['error'])
            body = data['error']
            
        # Replace sending template with data
        else:
            body = out_template.format(**data)
        
        # Send email
        self.send_reply(msg, body)
        
        
    def check_email(self):
        """
        
        Returns new emails in inbox.
        
        """
        return [msg for msg in self.mailbox.fetch(A(new=True))]    
        
    def parse_email(self,template, msg):
        
        """
        
        Parses email and extracts variables 
        
        """
        #Check if text or html
        if msg.text:
            string = msg.text
        elif msg.html:
            string = BeautifulSoup(msg.html).get_text()
        else:
            return {'error': 'No text found in the email'}
        
        # Convert the template into a regex pattern
        regex_pattern = re.sub(r'{(\w+)}', r'(?P<\1>.+?)', template)
        
        # Match the string with the regex pattern
        match = re.match(regex_pattern, string)
        
        if match:
            # Return the matched variables as a dictionary
            return match.groupdict()
        else:
            return {'error': 'Email does not follow pattern'}
        
    def do_things_with_data(self,data: dict):
        """
        
        Invokes functions related with data provided in email. Unused.
        
        """
        pass

    def send_reply(self, msg, body):
        # Create the reply email
        reply = MIMEMultipart()
        reply['From'] = self.username
        reply['To'] = msg.from_
        reply['Subject'] = 'Re: ' + msg.subject

        reply.attach(MIMEText(body, 'plain'))

        # Send the email
        smtp_host = 'smtp.example.com'
        smtp_port = 587  # Use 465 for SSL
        smtp_user = self.username
        smtp_pass = self.password

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(reply)




    def extract_variables(template, string):
        # Convert the template into a regex pattern
        regex_pattern = re.sub(r'{(\w+)}', r'(?P<\1>.+?)', template)
        
        # Match the string with the regex pattern
        match = re.match(regex_pattern, string)
        
        if match:
            # Return the matched variables as a dictionary
            return match.groupdict()
        else:
            return None

    def email_loop(self):
        """
        
        Executes checking loop, calls reply when new emails are found.
        
        """
        try:
            while True:
                print('Checking emails...')
                emails = self.check_email()
                if not emails:
                    time.sleep(30)
                else:
                    print('Emails found, replying...')
                    for msg in emails:
                        self.reply(msg)
        except KeyboardInterrupt:
            print("Stopped by user.")
        finally:
            MailBox.logout()

if __name__ == '__main__':
    EmailReply().email_loop()