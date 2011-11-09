# PySendmail

## What is it?

PySendmail is a simple Python script that allows you to send e-mail alerts from
the command line. Additionally, it can be imported as a module and incorporated
into existing Python scripts.

## How do I install it?

Install using *pip*:

    pip install -e git://github.com/chazlever/pysendmail.git#egg=pysendmail

Install using *setup.py*:
   
   git clone git://github.com/chazlever/pysendmail.git
   cd pysendmail
   python setup.py install

## How do I use it?

The script reads server settings from a config file which can be created using
the `config` option as follows:
   
    pysendmail --user 'username' --pass 'password' --server 'smtp.gmail.com' --port 587 config

To send e-mail, you can use the `send` option in a script or on the command
line as follows:

    pysendmail -t 'some@email.com' -s 'Your Subject' -m 'Your Message' -a 'filename' send 

For help using the application, use the `--help` flag on the command line:

    pysendmail --help

# Who are you?

My name is [Chaz Lever][chazlever]. I'm a graduate student pursuing a PhD in
computer science with a focus in computer networking and security.

[chazlever]:http://www.chazlever.com
