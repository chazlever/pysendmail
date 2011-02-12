PySendmail
==========

What is it?
-----------
PySendmail is a simple Python script that allows you to send e-mail alerts from 
the command line.

How do I use it?
----------------
The script reads server settings from a configuration file. You can write that 
configuration as follows
   
   pysendmail --user 'username' --pass 'password' --server 'smtp.gmail.com' --port 587 config

To send e-mail, you can use the following in a script or on the command line

   pysendmail -t 'some@email.com' -s 'Your Subject' -m 'Your Message' -a 'filename' send 

For help using the application, you can type the following on the command line

   pysendmail --help

Who are you?
============
My name is [Chaz Lever][chazlever]. I'm a computer science graduate student 
currenty doing computer networking and security research.

[chazlever]:http://twitter.com/chazlever

