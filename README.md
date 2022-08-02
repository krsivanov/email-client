# email-client
Email Client Application

## Description

Simple email-client project. The application can send and read emails from gmail and yahoo. This app can send emails to multiple users by dividing the addresses with ', '.
You can attach and remove files in the email with the buttons 'Add Attachment' and 'Remove Attachment'.
You can choose the file you want to remove from the dropdown menu in the right. After you write the email and add the attachment by pressing the menu button you  get a message box asking you to confirm if you want to send it. By pressing yes the email is sent.
'Show Inbox' button let you read the messages in your email(You don't see the attachemnt in the emails just the written message).
'Show Contacts' feature is in development

## Getting Started

### Dependencies

* The project is made on Python 3.10.4
* used python libraries:
    - tkinter (GUI)
    - smtplib (send mails)
    - imaplib (read mails)
    - email (parse mails)


### Installing
#### For Windows
* Download and Install - python v.3.10.5 from :
    https://www.python.org/downloads/release/python-3105/

* Download and Install pip
    The PIP can be downloaded and installed using the command line by going through the following steps:

    Method 1: Using cURL in Python
    Curl is a UNIX command that is used to send the PUT, GET, and POST requests to a URL. This tool is utilized for downloading files, testing REST APIs, etc.

    Step 1: Open the cmd terminal 

    Step 2: In python, a curl is a tool for transferring data requests to and from a server. Use the following command to request:

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    https://bootstrap.pypa.io/get-pip.py

* Install Dependancies 
    Step 1: Open the cmd terminal
    step 2: Write in the cmd terminal the following comands:
     - pip install tkinter
     - pip install imaplib
     - pip install smtplib

### Executing program

* Opening the Project
    Step 1: Open the cmd terminal
    Step 2: Open the folder where the project is located
    Step 3: Write in the command line the following command:
     - python email-client.py
