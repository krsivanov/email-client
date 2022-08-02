from os.path import basename
import smtplib
import imaplib
import tkinter as tk
from tkinter import StringVar
from tkinter import filedialog
from tkinter import messagebox
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

root = tk.Tk()
root.title('Email Client')
root.geometry('560x520')
root.resizable(0, 0)


global att_list
att_list = []
global atts_to_show
atts_to_show= ''
global email_to
email_to = StringVar()
global subject
subject = StringVar()
global attachments
attachments = StringVar()

def login(username,password):
    '''
    Login function using smtplib to create a SMTP connection
    '''
    try:   
        servers = {
        'gmail.com':{'server': 'smtp.gmail.com','port': '587'},
        'yahoo.com': {'server': 'smtp.mail.yahoo.com','port': '587'},
        }
        provider = username.split('@')[1]
        print(servers[provider]['server'])
        print(servers[provider]['port'])

    #Create your SMTP session 
        smtp = smtplib.SMTP(servers[provider]['server'],servers[provider]['port']) 
    #Use TLS to add security 
        smtp.ehlo()
        smtp.starttls() 
        smtp.ehlo()
    #User Authentication 
        smtp.login(username,password)
        print('logged in')
        show_write_email_frame()
        return smtp
            
    except smtplib.SMTPAuthenticationError as ex:
        messagebox.showwarning(title='Error', message='Wrong email/password')
    except KeyError:
        messagebox.showwarning(title='Error', message='Email domain not provided')
    except IndexError:
        messagebox.showwarning(title='Error', message='Wrong email address') 
    except Exception as ex:
        messagebox.showwarning(title='Error', message=ex)
        print('exception:', ex)

def confirm_mail(mail_from,mail_to, mail_subject, text_mail, password,files=None):
    """
    Function creating messega box to confirm if you want to send the email
    """
    res = messagebox.askyesno('Send Mail', 'Are you sure you want to send the email?') 
    if res == True:
        send_mail(mail_from,mail_to, mail_subject, text_mail, password, files)

    elif res == False:
        pass
    else:
        messagebox.showerror('error', 'something went wrong!')

def send_mail(mail_from,mail_to, mail_subject, text_mail, password, files=None):
    '''
    
    '''
    global att_list
    
    send_to = mail_to.split(', ')
    try:
        assert isinstance(send_to, list)
        msg = MIMEMultipart()
        msg['From'] = mail_from
        msg['To'] = mail_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = mail_subject

        msg.attach(MIMEText(text_mail))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
            
        smtp = login(mail_from,password)

    #Sending the Email
        smtp.sendmail(mail_from, send_to ,msg.as_string())
    #Terminating the session 
        smtp.quit() 
        messagebox.showinfo('Show Info', 'Your email has been sent successfully!')

    #clear the frame and variables
        mail_content.delete("1.0","end")
        email_to.set('')
        subject.set('')
        attachments.set('')
        att_list =[]
        show_write_email_frame()

    except Exception as ex: 
        print("Something went wrong....",ex)

def add_attachment():
    global atts_to_show
    global collection_choice
    global att_list
    global write_email_frame

    collection_choice = StringVar(write_email_frame)

    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filenames = filedialog.askopenfilenames(
        title='Open files',
        filetypes=filetypes)


    if filenames[0] not in att_list:
            att_list.append(filenames[0])
            atts_to_show += filenames[0].split('/')[-1]
            atts_to_show += '  '
            attachments.set(atts_to_show)


    choose_collection = tk.Menubutton(write_email_frame,text="Choose attachment to delete", indicatoron=True, 
                                        borderwidth=1, relief="raised")
    choose_collection.grid(row=5,column=2, sticky='W')
    global menu
    menu = tk.Menu(choose_collection, tearoff=False)
    choose_collection.configure(menu=menu)
    for choice in att_list:
        menu.add_command(label=choice, command=lambda option=choice: collection_choice.set(option))

def remove_attachment(item_to_remove):
    global atts_to_show
    global att_list
    global collection_choice
    global write_email_frame

    if item_to_remove!='Choose attachment to delete':
        print(att_list)
        att_list.remove(item_to_remove)
        menu.delete(item_to_remove)

        atts_to_show=''
        for att in att_list:
            atts_to_show += att.split('/')[-1]
            atts_to_show += '  '
        attachments.set(atts_to_show)
        
    print(att_list)

def read_mail(username, app_password):
    try:
        global read_emails_frame
        servers = {
        'gmail.com':{'server': 'imap.gmail.com','port': '993'},
        'yahoo.com': {'server': 'imap.mail.yahoo.com', 'port': '587'},
        }

        provider = username.split('@')[1]
        print(servers[provider]['server'])
        print(servers[provider]['port'])

        #set connection
        mail = imaplib.IMAP4_SSL(servers[provider]['server'],servers[provider]['port'])
        #login
        mail.login(username, app_password)
        #select inbox
        mail.select("INBOX")
        #select specific mails
        _, selected_mails = mail.search(None, '(FROM "*")')
        #total number of mails from specific user
        print("Total Messages:" , len(selected_mails[0].split()))
    
        def message_fill(email_message):
            email_text = ''
            for part in email_message.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    message = part.get_payload(decode=True)
                    email_text += message.decode()
            return email_text

        feed = []
        index = 1
        for num in selected_mails[0].split():
            _, data = mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
            #convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)
            feed.append((index, email_message['from'], email_message['subject'],message_fill(email_message)))
            index += 1

        listbox_items = [f'{el[0]} || From: {el[1]} || Subject: {el[2]}' for el in feed]

        def fill_text_field(event):
            title_item = title_listbox.get(tk.ACTIVE)
            text_field.delete('1.0', tk.END)

            for element in feed:
                if f'{element[0]} || From: {element[1]} || Subject: {element[2]}' == title_item:
                    text_field.insert(tk.END, element[3])

        def populate_title_listbox(data):
            title_listbox.delete(0, tk.END)
            for element in data:
                title_listbox.insert(tk.END, element)

        scrollbar = tk.Scrollbar(read_emails_frame, orient=tk.VERTICAL)
        scrollbar.grid(row=0, column=1, sticky="NS")
        title_listbox = tk.Listbox(read_emails_frame, height=10, width=85, yscrollcommand=scrollbar.set)
        title_listbox.grid(row=0, column=0)
        title_listbox.bind('<<ListboxSelect>>', fill_text_field)
        title_listbox.bind('<KeyRelease>', populate_title_listbox(listbox_items))
        populate_title_listbox(listbox_items)
        text_field = tk.Text(read_emails_frame, width=64, height=13)
        text_field.grid(row=1, column=0,pady=20)
        scrollbar.config(command=title_listbox.yview)
   
    except IndexError as ex1:
        messagebox.showwarning(title='Error', message='Wrong email/password')

    except KeyError as ex2:
            messagebox.showwarning(title='Error', message='Wrong email/password')

    except imaplib.IMAP4.error as ex3:
        messagebox.showwarning(title='Error', message='Wrong email/password')

def hide_frame(frame):
    frame.destroy()

def show_write_email_frame():
    global atts_to_show
    global write_email_frame
    hide_frame(read_emails_frame)
    write_email_frame = tk.Frame(root, width=500)
    write_email_frame.grid(row=1, column=0,sticky='NSEW')

    atts_to_show=''

    write_email_frame.columnconfigure(1, weight=2)
    to_label = tk.Label(write_email_frame,text='To:', font=('Helvetica 10'))
    to_label.grid(row=0,column=0, padx=10,pady=5, sticky='W')
    to_entry = tk.Entry(write_email_frame,textvariable= email_to, font=('Helvetica 10'))
    to_entry.grid(row=0,column=1, padx=10,pady=5, sticky='WE')
    subject_label = tk.Label(write_email_frame,text='Subject:', font=('Helvetica 10'))
    subject_label.grid(row=1,column=0, padx=10,pady=5, sticky='W')
    subject_entry = tk.Entry(write_email_frame,textvariable= subject, font=('Helvetica 10'))
    subject_entry.grid(row=1,column=1, padx=10,pady=5, sticky='WE')
    mail_text_label = tk.Label(write_email_frame,text='Mail Text:', font=('Helvetica 10'))
    mail_text_label.grid(row=2,column=0, padx=10,pady=5, sticky='W')
    global mail_content
    mail_content = tk.Text(write_email_frame, height = 14, width = 66)
    mail_content.grid(row=3,column=0, padx=10, columnspan=3)
    att_label = tk.Label(write_email_frame, text='Attachments:',font=('Helvetica 10'))
    att_label.grid(row=4,column=0, padx=10,pady=10, sticky='W')
    show_att_label = tk.Label(write_email_frame, textvariable=attachments,font=('Helvetica 10'))
    show_att_label.grid(row=4,column=1, padx=10,pady=10, sticky='W', columnspan=10)
    add_att_btn = tk.Button(write_email_frame, text='Add Attachment', font='Helvetica 9 bold',command=lambda : add_attachment())
    add_att_btn.grid(row=5, column=0 ,sticky='W', pady=5, padx=10)
    remove_att_btn = tk.Button(write_email_frame, text='Remove Attachment', font='Helvetica 9 bold',command=lambda :remove_attachment(collection_choice.get()))
    remove_att_btn.grid(row=5, column=1 ,sticky='W', pady=5, padx=10)
    send_email_btn = tk.Button(write_email_frame, text='SEND', font='Helvetica 9 bold', command=lambda : confirm_mail(user_email.get(),email_to.get(),subject.get(), mail_content.get("1.0",'end-1c'), password_var.get(),att_list))
    send_email_btn.grid(row=6,columnspan=4,sticky= 'W', pady=5, padx=10)

    show_contacts_btn = tk.Button(main_frame, text='Show contacts', font='Helvetica 9 bold',command=lambda :show_contacts_frame(user_email.get()))
    show_contacts_btn.grid(row=1, column=3 ,sticky='W', pady=5, padx=10)

def show_read_emails_frame(username,password):
    hide_frame(write_email_frame)
    global read_emails_frame
    read_emails_frame = tk.Frame(root,padx=15, pady=15)
    read_emails_frame.grid(row=1, column=0,sticky='NSEW')
    read_mail(username,password)

#TODO
def show_contacts_frame(user_email):
    messagebox.showinfo(title='INFO', message='Coming Soon...')

    # hide_frame(write_email_frame)
    # s=StringVar()
    # name_label = tk.Label(contacts_frame,text='Name:', font=('Helvetica 10'))
    # name_label.grid(row=0,column=0, padx=10,pady=5, sticky='W')

    # name_entry = tk.Entry(contacts_frame,textvariable= s, font=('Helvetica 10'))
    # name_entry.grid(row=0,column=1, padx=10,pady=5, sticky='WE')
    # subject_label = tk.Label(contacts_frame,text='Subject:', font=('Helvetica 10'))
    # subject_label.grid(row=1,column=0, padx=10,pady=5, sticky='W')
    # subject_entry = tk.Entry(contacts_frame,textvariable= s, font=('Helvetica 10'))
    # subject_entry.grid(row=1,column=1, padx=10,pady=5, sticky='WE')



    def load_contacts(user_email):
        username = user_email.split('@')[0]
        print(username)
        try:
            f1 = open(f'contacts/{username}.txt')
            contact_list = f1.readlines()
            f1.close()
            return contact_list
        except FileNotFoundError:
            print('There is no file with such name')

    print(load_contacts(user_email))

#FRAMES
main_frame = tk.Frame(root)
main_frame.grid(row=0,column=0,sticky='NSEW')
read_emails_frame = tk.Frame(root,padx=15, pady=15)
read_emails_frame.grid(row=1, column=0,sticky='NSEW')
global write_email_frame
write_email_frame = tk.Frame(root)
write_email_frame.grid(row=2, column=0,sticky='NSEW')
contacts_frame = tk.Frame(root)
contacts_frame.grid(row=3, column=0,sticky='NSEW')

#main FRAME
user_email = StringVar()
password_var = StringVar()

email_label = tk.Label(main_frame,text='E-mail Address', font=('Helvetica 10'))
email_label.grid(row=0,column=0, padx=10,pady=5, sticky='W')
email_entry = tk.Entry(main_frame,textvariable= user_email, font=('Helvetica 10'))
email_entry.grid(row=0,column=1, padx=10,pady=5, sticky='W')
password_label = tk.Label(main_frame,text='Password', font=('Helvetica 10'))
password_label.grid(row=0,column=2, padx=10,pady=5, sticky='W')
password_entry = tk.Entry(main_frame,textvariable= password_var, font=('Helvetica 10'), show="*")
password_entry.grid(row=0,column=3, padx=10,pady=5, sticky='W', columnspan=2)
login_btn = tk.Button(main_frame, text='LOGIN', font='Helvetica 9 bold',command=lambda :login(user_email.get(),password_var.get()))
login_btn.grid(row=1, column=0 ,sticky= 'W',padx=10)
write_email_btn = tk.Button(main_frame, text='Write New Email', font='Helvetica 9 bold',command=lambda :show_write_email_frame())
write_email_btn.grid(row=1, column=1 ,sticky= 'W',padx=10  )
show_emails_btn = tk.Button(main_frame, text='Show Inbox', font='Helvetica 9 bold',command=lambda :show_read_emails_frame(user_email.get(),password_var.get()))
show_emails_btn.grid(row=1, column=2 ,sticky= 'W',padx=10)

root.mainloop()
