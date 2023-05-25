
import os
import smtplib
import ssl
import time
from datetime import datetime
from email.message import EmailMessage
from operator import truediv

ct = "Wireless" #Change To Ethernet Or Wireless
room = "L512" #Change To Room ID/Number
lap = 1

while True:
    # Ping 8.8.8.8 100 times
    TIME = datetime.now()
    resp = os.popen("ping -c 100 8.8.8.8")
    with open(f"ping_report_{lap}.txt", "w") as file:
        file.write(f'Ping Time: {TIME}\n')
        for x in resp:
            file.write(f'Ping Response: {x}')
    with open(f"ping_report_{lap}.txt", "r") as fp:
        for l_no, line in enumerate(fp):
            if "% packet loss" in line:
                indx = line.index("%")
                loss = float(line[indx-3: indx].replace(",", ""))
                if loss >= 3:
                    time.sleep(5)
                    print(f"wifi is failing. Room '{room}'. Connection Type is '{ct}', packet loss is at: {loss}, in File 'Ping_Report_{lap}'")
                    email_sender = 'fhspimail@gmail.com'
                    email_password = 'oczikaguxdkdfozy'
                    email_receiver = '1089227@lcps.org', '911657@lcps.org', '1067652@lcps.org', 'john.cunningham@lcps.org', 'Patrick.A.McNanley@lcps.org'
                    subject = "WIFI Fail _'LCPS'_Ethernet_"
                    body = f"wifi is failing. Room '{room}'. Connection Type is '{ct}', packet loss is at: {loss}, in File 'Ping_Report_{lap}'\n"
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em['Subject'] = subject
                    em.set_content(body)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())
                else:
                    print(f"Wifi Is Online. Current packet loss is at: {loss}, File Is 'Ping_Report_{lap}'\n")
                    if loss < 3:
                        file_path = f"ping_report_{lap}.txt"
                        os.remove(file_path)
                        print(f"{file_path}-Deleted")
    lap += 1

    # Delete any files older than 14 days
    folder_path = "."
    days_to_keep = 14

    current_time = time.time()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            modification_time = os.path.getmtime(file_path)
            if current_time - modification_time > days_to_keep * 24 * 60 * 60:
                os.remove(file_path)
                print(f"{filename}-Deleted")

    time.sleep(60)
