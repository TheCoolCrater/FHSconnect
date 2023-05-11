from operator import truediv
import os 
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
from selenium import webdriver

lap = 1

while lap <= 5:
    TIME = datetime.now()
    resp = os.popen("ping -n 100 8.8.8.8") # ping Google's DNS server
    with open(f"ping_report_{lap}.txt", "w") as file:
        file.write(f'Ping Time: {TIME}\n')
        for x in resp:
            file.write(f'Ping Response: {x}')
        lap += 1

    with open(f"ping_report_{lap-1}.txt", "r") as fp:
        for l_no, line in enumerate(fp):
            if "% loss" in line:
                indx = line.index("%")
                loss = float(line[indx-3: indx].replace("(",""))

                if loss >= 15:
                    print(f"Wifi Is Failing. Packet Loss is At: {loss}")

                    # Navigate to Google sign-in page using Chrome
                    driver = webdriver.Chrome()
                    driver.get("https://accounts.google.com/signin")

                    # Enter test email and password
                    email_input = driver.find_element_by_id("identifierId")
                    email_input.send_keys("test@gmail.com")
                    next_button = driver.find_element_by_id("identifierNext")
                    next_button.click()
                    password_input = driver.find_element_by_xpath("//input[@type='password']")
                    password_input.send_keys("test_password")
                    sign_in_button = driver.find_element_by_id("passwordNext")
                    sign_in_button.click()

                    # Check if sign-in was successful or not
                    try:
                        driver.find_element_by_xpath("//div[text()='Compose']")
                        sign_in_status = "Success"
                        sign_out_button = driver.find_element_by_css_selector(".gb_Ia.gbii")
                        sign_out_button.click()
                        sign_out = driver.find_element_by_id("gb_71")
                        sign_out.click()
                    except:
                        sign_in_status = "Failure"

                    driver.close()

                    # Send email with sign-in status
                    email_sender = 'EMAIL'
                    email_password = "EMAIL PASS"
                    email_receiver = 'EMAIL-PHONE'

                    subject = "WIFI Fail"
                    body = f"""
                    wifi is failing. packet loss is at: {loss}
                    Sign-in status: {sign_in_status}
                    """

                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em[' subject'] = subject
                    em.set_content(body)


                    context = ssl.create_default_context()

                    with smtplib.SMTP_SSL( 'smtp.gmail.com' , 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())


                else:
                    print(f"Wifi Is Online. Current packet loss is at: {loss} ")
