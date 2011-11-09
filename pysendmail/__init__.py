#!/usr/bin/env python

"""
Send e-mails from Python scripts or the command line.

A standalone program to send or receive applications from the command line. Can
also be imported as a module into other Python scripts to facilitate sending
e-mail.
"""

__author__ = 'Chaz Lever'
__date__ = '11/17/2010'

import base64
import email
from email.Utils import COMMASPACE, formatdate
import os
import smtplib
import stat
import sys


class SendMail:
    """SendMail provides methods for sending e-mail."""

    def __init__(self):
        self.User = None
        self.Pass = None
        self.SmtpServer = None
        self.SmtpPort = None
        self.Ssl = True
        self.ConfigFile = os.path.expanduser('~/.pysendmail')

    def writeConfig(self):
        """Write the configuration file containing server credentials."""
        try:
            with open(self.ConfigFile, 'w') as f:
                config = (self.User, self.Pass, self.SmtpServer,
                        str(self.SmtpPort), str(self.Ssl))
                f.write(base64.b64encode(':'.join(config)))
                os.chmod(self.ConfigFile, stat.S_IRUSR | stat.S_IWUSR)
        except IOError, e:
            sys.exit("ERROR: %s" % str(e))

    def readConfig(self):
        """Read the configuration file containing server credentials."""
        try:
            with open(self.ConfigFile, 'r') as f:
                config = base64.b64decode(f.readline().strip())
                config = config.split(':')
                self.User = config[0]
                self.Pass = config[1]
                self.SmtpServer = config[2]
                self.SmtpPort = int(config[3])
                self.Ssl = ('True' == config[4])
        except IOError, e:
            sys.exit("ERROR: %s" % str(e))

    def send(self, to, subject, message, attachments=None):
        """Send message to mail server over TLS connection"""

        # BUILD THE E-MAIL MESSAGE
        msg = email.MIMEMultipart.MIMEMultipart()
        msg['From'] = self.User
        msg['To'] = COMMASPACE.join(to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(email.MIMEText.MIMEText(message))

        # ATTACH ANY FILE ATTACHMENTS
        try:
            if attachments:
                for fname in attachments:
                    part = email.MIMEBase.MIMEBase('application',
                            'octet-stream')
                    with open(fname, 'rb') as f:
                        part.set_payload(f.read())
                    email.Encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment',
                        filename=os.path.basename(fname))
                    msg.attach(part)
        except Exception, e:
            sys.exit("ERROR: %s" % str(e))

        # CONNECT TO MAIL SERVER AND SEND MESSAGE
        try:
            server = smtplib.SMTP(self.SmtpServer, self.SmtpPort)
            #server.set_debuglevel(1)
            server.starttls()
            server.login(self.User, self.Pass)
            server.sendmail(self.User, to, msg.as_string())
            server.close()
        except smtplib.SMTPException, e:
            sys.exit("ERROR: %s" % str(e))
