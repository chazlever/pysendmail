#! /usr/bin/env python
#
# Author: Chaz Lever
# Created:  11/17/2010

import argparse
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

if __name__ == '__main__':

    # PARSE COMMAND LINE PARAMETERS
    parser = argparse.ArgumentParser(description="""
    Script to send e-mails from the command line. Useful for sending automated
    messages within shell scripts.""")

    parser.add_argument('ACTION',
        action='store',
        help='Script action to perform {config,send}')

    # E-MAIL SEND PARAMETERS
    group = parser.add_argument_group("send options")
    group.add_argument('-t',
        action='append',
        dest='TOLIST',
        default=[],
        help='Email addresses in the TO: field')
    group.add_argument('-s',
        action='store',
        dest='SUBJECT',
        default='',
        help='E-mail subject')
    group.add_argument('-m',
        action='store',
        dest='MESSAGE',
        default='',
        help='E-mail message')
    group.add_argument('-a',
        action='append',
        dest='ATTACHMENTS',
        default=[],
        help='Email attachments')

     # E-MAIL CONFIG PARAMETERS
    group = parser.add_argument_group("config options")
    group.add_argument('--user',
        action='store',
        dest='USER',
        default=None,
        help='E-mail login for mail server')
    group.add_argument('--pass',
        action='store',
        dest='PASS',
        default=None,
        help='E-mail password for mail server')
    group.add_argument('--server',
        action='store',
        dest='SMTP_SERVER',
        default='smtp.gmail.com',
        help='Specify e-mail SMTP server')
    group.add_argument('--port',
        action='store',
        dest='SMTP_PORT',
        default=587,
        type=int,
        help='Specify e-mail SMTP port')
    group.add_argument('--nossl',
        action='store_false',
        dest='SSL',
        default=True,
        help='Use SSL to connect to SMTP server')

    results = parser.parse_args()

    if 'config' == results.ACTION:
        sendMail = SendMail()
        sendMail.User = results.USER
        sendMail.Pass = results.PASS
        sendMail.SmtpServer = results.SMTP_SERVER
        sendMail.SmtpPort = results.SMTP_PORT
        sendMail.Ssl = results.SSL
        sendMail.writeConfig()
    elif 'send' == results.ACTION:
        sendMail = SendMail()
        sendMail.readConfig()
        sendMail.send(results.TOLIST, results.SUBJECT, results.MESSAGE,
            results.ATTACHMENTS)
    else:
        parser.print_help()
