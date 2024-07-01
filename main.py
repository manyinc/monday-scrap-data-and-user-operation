from datasetgetter import *
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import requests
import os
import phonenumbers
from phonenumbers import PhoneNumberFormat
from smsapi.client import SmsApiPlClient


def find_user(login):
    global row
    for row in data_set:
        if login in row["New e-mail adress"]:
            return row
        
def time_info(start_time,end_time):
    print("#####################################################################################################\n")
    duration = end_time - start_time
    print("Process end in : {:.2f} sec".format(duration))
    print("\n#####################################################################################################\n")
            
class Person:
    def __init__(self, row):
        self.fname = row['Name']
        self.lname = row['Surname']
        self.position = row['Position']
        self.mail = row['New e-mail adress']
        self.mail_old = row['Old e-mail adress']
        self.phone_sim = row['Phone']
        self.mail_status = row['New e-mail status']
        self.monday_status = row['Account status']
        self.passwd = row['New e-mail password']
        self.fname_nu = ""
        self.lname_nu = ""
        self.user_pass = ""
        self.msg = ""

    def transform_non_unicode(self):
        self.fname_nu = ""
        self.lname_nu = ""        
        for letter_in_fname in self.fname :
            if letter_in_fname == "Ł":
                self.fname_nu = self.fname_nu + "L"
            elif letter_in_fname == "ł":
                self.fname_nu = self.fname_nu + "l"
            else:
                self.fname_nu = self.fname_nu + letter_in_fname
        self.fname_nu = unicodedata.normalize('NFKD', self.fname_nu).encode('ascii', 'ignore')
        self.fname_nu = self.fname_nu.decode('UTF-8')
        

        for letter_in_lname in self.lname :
            if letter_in_lname == "Ł":
                self.lname_nu = self.lname_nu + "L"
            elif letter_in_lname == "ł":
                self.lname_nu = self.lname_nu + "l"
            else:
                self.lname_nu = self.lname_nu + letter_in_lname
        self.lname_nu = unicodedata.normalize('NFKD', self.lname_nu).encode('ascii', 'ignore')
        self.lname_nu = self.lname_nu.decode('UTF-8')
        return self.fname_nu,self.lname_nu


    def transform_german_poland_phone_number(self):
        if not self.phone_sim.startswith('+'):
            self.phone_sim = '+' + self.phone_sim
        
        phone_number = phonenumbers.parse(self.phone_sim, "DE")
        
        if phonenumbers.is_valid_number(phone_number):
            formatted_number = phonenumbers.format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
            return formatted_number
            
        else:
            phone_number = phonenumbers.parse(self.phone_sim, "PL")
        
            if phonenumbers.is_valid_number(phone_number):
                formatted_number = phonenumbers.format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
                return formatted_number
            else:
                print(">>> Wrong  - Invalid number format for Germany and Poland")

    def footer_generate(self):
        self.transform_non_unicode()
        with open("template/footer_template.html", 'r',encoding='utf-8') as temp_footer:
            with open("footer\%s%s_example_com (%s).htm"%(self.fname_nu.lower(),self.lname_nu.lower(),self.mail), 'w',encoding='utf-8') as new_footer:
                for line in temp_footer:
                    if line.strip() == '{uname}':
                        new_footer.writelines(f"{self.fname} {self.lname}")

                    elif line.strip() == '{num}':
                        if self.phone_sim == '' or self.phone_sim == '-' or self.phone_sim == 'NULL':
                            new_footer.writelines('')
                        else:
                            new_footer.writelines(f'<tr><td nowrap="nowrap"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASxSURBVFhHpZd5qFVVFIevBlY0J1YmWQSWSqiNBvUa7KWZpBgW/RFqpiklZCmBmYpNpNmEIgo5gWMY+ocW0uCMrwlStKBHg6WFRQ6U5Vzft+85h3Puuffd+977we+t/dZee+119rD2um0KrcTM1V0uQmyFv0VyzYTBjV8ja0LZAHB6BqIdjv4taioD2/aIL+FVQVHETvgWXIyP/4KmAnIB4HAK4ll4LvwYjsLJL8gmwbgrEPfAR2A/deBb6PhtxX/zyASAk4WI4fAA/Bn2imQfnHyPrAn4uRbxEnwoKGgz3g/LIQmAQe8iHoeN0An3onuDtquxB96F7idkzWB8f8Ri2AEugcPwcRqZoK1/MJyNiCe/28nVI8cjDOJKuAG79D4nQN8R5raT8R8iboC74aPQYDJow8D7kBp+B/1KT3MG2MQr4Qpo44oE0DcIsQY6bi18h34nTIDNhYhNsAd8mf7J6oUrMKrYLIwsN7lA70q8Dl2BVepS+AZ+AD20+trFhHPh2bQDGH8I4Yfugy/Q10e9MIDr4T+wQUUl4OQ5xEfwJhw4JgB9IxxA0312G51kNPwcu8uQAdj4cY8V/ysYYDsbBmDjBDylogrifc7dbSY4BhfQ7ApXw+vgJ0zkygTQ7weshF3gCHUG4N5fAC9RUQk4ehtRDxtwVDHT0fc3fJDme7A7nKk+heehH/y0/xhA7Kx3JHNg8lkIB/wA47tdDX7hj3A049Nbpg/PTFf0txvAejtAWccYTUeMhZ78ehyEK1oN2B1BTCr+VxgXyRjLIjnAADbA/XAgk3ldSnFvJIfg1C9qDjwLZtUH8H1m0BSxEZqQ7miL0+M0TMHnwSdhKeJoXYVmAd9HEb6Qvpid1Qn0vyN2wQ6ugHCPNR5HpB7INOZAE9Aw+u4PmubB6zuGSc2yabiydem3wCD8ykymEvTVITZDI7+F/iQTthbxCghfL/drAhNeEzQRmHALwgPlVV1Pf5NXtjlIAoj2xeU6Cy5hEouSBPS/ivDF9Kk1wZj5KoL+ntDc3yTSK+Ak8xHr4M3wNXUleAKaYMxyW5ngapVpoOsMrZDMLztoN8DLQ2cZZAKIMBL+Ct0Kq5sEBGgKVrcIuk2fYZMcTNpWRZ/CG6Fp1+tmgvMpLxtE7g0XGN+K8NCdhHVM/JX6NLCZiHBbhMWGqdrVcVXeZIwvqHauqlnRlG+t4cclKBuAYOBQhAXEn9AawHubATa3IcwhPi4xksljYBdXW7mao2IAgoGmUKvbg7AvA93bDLDxsI6BT8EV2LyovhTYzUX4TGeCaDIAwUBvhu+BNcPDDPSQtgj4irfjffwMUVfuEGaA4QyEy2cuX4uTaepbCFfAM1CPnzB31QAEQVho3Al9tKYw2KuV3vdaYYVkgWLNEKrjmgIQDPDHhb8T/LHi1dpNEK/Ac2hXBXZeQ8eeD31fAqqegXLAmcWnW+Pz/Qc0ac0jSGuAHLA3dXutzaILsQvlmGhRAAKnFyOmQm+AdeVfcDm0BtjOJIeR2lkNLYXdoEFqn6DFAcRggksRz0DTtO++cH+tjt3iTirAIiaPq+IErQ4gBoG4Cr7x/hzzq03V+v8Czmfy0t8ToFD4HxsXqj8iwVaTAAAAAElFTkSuQmCC" alt="Mobile:" style="vertical-align:middle;" width="13" height="13">&nbsp;&nbsp;</td><td nowrap="nowrap"><a href="tel:{self.phone_sim}" style=" color:#434343;text-decoration:none;">{self.phone_sim}</a></td></tr>')
                       
                    elif line.strip() == '{mail}':
                            new_footer.writelines(f'<tr><td nowrap="nowrap"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJlSURBVFhH7ZVNSFRRFMefqVQgupBC2hUoEoigmC0GtUhoo6AUrSq3RqELP3YmCCLqUq0WUdQuFyJKizAkwYVEiGgLRwgJgtwICn7h5+9/35vpzTjofL1pM3/4zbn3vjvnnHfuffdaaf1vZehncKywENMDtZADx+CFFG8bpqGrrWFlKcMJPgtXIJXaAJ8S+ETjISzBM/gNF8ALqbIFMATl8EUJrNG4CrWUZArruYh5CzMHG3rTPA2iXcemQjuOveQu9QSZPXHanokYjZivdo9dyYDe/KLdNZqBpyzHqt1NjohzDfMW7psBW3vuCozAIVTBMn9oA/OZJir8NGNWQMG1EV/DEYRUoAy24CNok0iL8JhqLNjd2ITvIswHqDQDjj/YhF8QUgGLQH7Q5BegjVIC8zjqh2zaUYm5mfCS5k+Qv33ohNLwl4n4vTNJ36my/wxahnbQstzBninmKKDOlG7Igm9QjM9+OHXChiwBE+bNqEs81yH1CvLNgGW9hxbmqoxBMe+yDOgwk/S8lXnv7O4/Mfc65vQSRBIORjGqhgJLTeDHySO7axzWYfwQCK7TtShS8HCdWwG3mHsP8wZumAHLUnLaK4Hz4w8042fC7kZWTBVwC8c6qrUxB0DrqeUJBB+Gm+cFD1dMCUgE2IYOmtpsP0A7vZqx5xCyL6JRzAkERLDvmAoooa3TMy7FnYBE4GPhdONSQgkkQ+kE3Akk5eaLUsG4auialO46NhWqcexfnYS6pfpAu3kS1sGraihGLtRDJvSaQCShO1v3dCo1Dg+Cb0oStzE+iPrej1MHMJfI4ZVWEmVZJ4CmxwBbK6z2AAAAAElFTkSuQmCC" alt="Email:" style="vertical-align:middle;" width="13" height="13">&nbsp;&nbsp;</td><td nowrap="nowrap"><a href="mailto:{self.mail}" style=" color:#434343;text-decoration:none;">{self.mail}</a></td></tr>')
                    
                    else:
                        new_footer.write(line)
            new_footer.close()
        temp_footer.close()
        print("\n#####################################################################################################")
        print("\nSoft >> Footer succesfully generated")

    def send_sms(self, sender: str, msg_content: str, recipient_number: str):

        access_token = 'j357sVqDXirTeHN4exqD9LN81ArAuRfI6l91YvJM'

        client = SmsApiPlClient(access_token=access_token)

        # send single sms
        result = client.sms.send(to=recipient_number, message=msg_content)

    def config_mail_and_footer(self, user_pass):
        self.transform_non_unicode()
        self.user_pass = user_pass
        self.fname = self.fname.strip()
        self.lname = self.lname.strip()
        self.mail = self.mail.strip()
        siganture_name = f"{self.fname.lower()}{self.lname.lower()}_example_com ({self.mail.lower()})"
        mail_name = f"footer\{self.fname_nu.lower()}{self.lname_nu.lower()}_example_com ({self.mail.lower()}).htm"

        #browser open
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://mail.netart.com")
        save_all_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-box__buttons--save-all")))
        save_all_button.click()

        #login
        try:
            username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inlineFormInputGroupUsername")))
            password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inlineFormInputGroupPassword")))
            login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))

            username_input.send_keys(self.mail)
            password_input.send_keys(self.user_pass)
            login_button.click()

            print(f">>> Succes - login : {self.mail}")
        except:
            print(f">>> Wrong  - login or password : {self.mail}")

        #preferences
        try:
            settings_url = "https://mail.netart.com/?_task=settings&_action=preferences"
            driver.get(settings_url)

            iframe_xpath = "/html/body/div[2]/div[4]/div[3]/div[2]/iframe"
            iframe_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
            driver.switch_to.frame(iframe_element)

            language_dropdown = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "rcmfd_lang")))
            language_dropdown.click()
            option_de = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='de_DE']")))
            option_de.click()
            save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "rcmbtn100")))
            save_button.click()

            driver.switch_to.default_content()
            mail_view = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div[2]/div[2]/table/tbody/tr[3]/td")))
            mail_view.click()
            driver.switch_to.frame(iframe_element)

            view_dropdown = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/fieldset[1]/table/tbody/tr[4]/td[2]/select")))
            view_dropdown.click()
            option_de = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/fieldset[1]/table/tbody/tr[4]/td[2]/select/option[3]")))
            option_de.click()
            save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "rcmbtn100")))
            save_button.click()

            print(f">>> Succes - preferences config : {self.mail}")
        except:
            print(f">>> Wrong  - preferences config : {self.mail}")

        #account name
        try:
            account_settings_url = "https://mail.netart.com/?_task=settings&_action=identities"
            driver.get(account_settings_url)

            account_iframe_xpath = "/html/body/div[2]/div[4]/div[3]/div[2]/iframe"
            account_iframe_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, account_iframe_xpath)))
            driver.switch_to.frame(account_iframe_element)

            account_username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "rcmfd_name")))
            account_username_input.send_keys(f"{self.fname} {self.lname} - PLAN [B] ENERGY")

            account_submit_button = "return rcmail.command('save','',this,event)"
            driver.execute_script(account_submit_button)

            sleep(1)

            print(f">>> Succes - identities config : {self.mail}")
        except:
            print(f">>> Wrong  - identities config : {self.mail}")

        #signatures
        try:
            signatures_url = "https://mail.netart.com/?_task=settings&_action=plugin.signatures"
            driver.get(signatures_url)

            script = "return rcmail.command('create-signature','',this,event)"
            driver.execute_script(script)

            driver.switch_to.default_content()
            signature_view = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "signatures-frame")))
            driver.switch_to.frame(signature_view)

            add_signature = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mce-i-html")))
            add_signature.click()  

            edit_signature = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[1]/fieldset/table/tbody/tr[4]/td/div/div/div[1]/div/div[1]/div/div/div/div/div/div[3]/div/div[8]/button")))
            edit_signature.click()

            footer_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mce-textbox")))
            
            with open(mail_name, 'r',encoding='utf-8') as temp_footer:
                    copy_file = temp_footer.read()    
            temp_footer.close()

            load_data = "arguments[0].value = arguments[1];"
            driver.execute_script(load_data, footer_input, copy_file)
            sleep(3)
            ok_signature = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Ok")]')))
            ok_signature.click()
            
            s_name = siganture_name
            signature_name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[1]/fieldset/table/tbody/tr[1]/td[2]/input")))
            signature_name_input.send_keys(s_name)

            option_sign_pos = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='below']")))
            option_sign_pos.click()

            def_signature = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'custom-control-label')))
            def_signature.click()

            submit_button = "return rcmail.command('save-signature','',this,event)"
            driver.execute_script(submit_button)
            
            print(f">>> Succes - add signature: {self.mail}\n")
        except:
            print(f">>> Wrong  - signature not found : {self.mail}\n")
        
        sleep(1)
        driver.quit()

    def get_user_list_contact_vcf(self):
        with open("contact/contact.vcf", 'w', encoding='utf-8') as kontakt:
            for row in data_set:

                sim_num = row['Phone']
                position = row['Position']

                if sim_num != "" and sim_num != "-" and sim_num != "NULL":
                    fname = row['Name']
                    lname = row['Surname']
                    mail = row['New e-mail adress']

                    kontakt.writelines("BEGIN:VCARD\n")
                    kontakt.write("VERSION:2.1\n")
                    kontakt.write("N:%s;%s;;Example |;\n" %(fname,lname))
                    kontakt.write("FN:Example | %s %s\n" %(lname,fname))
                    kontakt.write("EMAIL:%s\n" %(mail))
                    kontakt.write("TEL;CELL:%s\n" %(sim_num))
                    kontakt.write("ORG:Example;%s\n" %(position))
                    kontakt.write("END:VCARD\n")
        kontakt.close()
        print(">>> Succes - contact generated succesfully\n")

##########################################################################################################################################################################################################
if __name__ == "__main__":
    print("\n################################# © Copyright Mateusz Zarzycki 2024 #################################\n")
    print("#####################################################################################################\n")
    while True:
        
        print("########################################### Select option ###########################################\n")
        print("Soft>>> 1 - Create signature for single user and config mail\n")
        print("Soft>>> 2 - Create signature and config all accounts\n")
        print("Soft>>> 3 - Create contact file vcf\n")
        print("Soft>>> 4 - Messeges to users about change mail\n")
        print("Soft>>> 5 - Test phone format, signature\n")
        print("#####################################################################################################\n")
        select = input("User>>> ")
##########################################################################################################################################################################################################
        if select == "1":
            try:
                while True:
                    login = input("\nUser >>> Login : ")
                    find_user(login)
                    user = Person(row)
                    user_pass = input(f"User >> Enter {user.mail} password : ")
                    start_time = time.time()
                    user.phone_sim = user.transform_german_poland_phone_number()
                    user.footer_generate()
                    user.config_mail_and_footer(user_pass)
                    end_time = time.time()
                    time_info(start_time,end_time)
                    print("Soft >>> If you want to back to menu press Ctrl+Z")
            except:
                print("Soft>>> Succesfuly back to menu !")
##########################################################################################################################################################################################################
        elif select == "2":
            try:
                for row in data_set:
                    user = Person(row)
                    user_pass = user.passwd
                    start_time = time.time()
                    user.phone_sim = user.transform_german_poland_phone_number()
                    user.footer_generate()
                    user.config_mail_and_footer(user_pass)
                end_time = time.time()
                time_info(start_time,end_time)
            except:
                print("Soft>>> Succesfuly back to menu !")
##########################################################################################################################################################################################################
        elif select == "3":
            try:
                user = Person(data_set[1])
                start_time = time.time()
                user.get_user_list_contact_vcf()
                end_time = time.time()
                time_info(start_time,end_time)
            except:
                print("Soft>>> Succesfuly back to menu !")
##########################################################################################################################################################################################################
        elif select == "4":
            start_time = time.time()
            msgs_to_users = []
            


            for row in data_set:
                user = Person(row)
                if user.monday_status == "Active" and user.phone_sim != "0":
                    try:
                        phone_num = user.phone_sim
                        user.msg = f"""
Hallo,
Normalerweise kannst du dein E-Mail-Postfach ueber die Webseite www.mail.example.com verwalten.
"""
                        user.send_sms("Example IT", user.msg, phone_num)
                        print(f"Succes ---> message sent to -> {phone_num}")
                    except:
                        print(f"Error  ---> wrong number    -> {phone_num}")
                sleep(3)



            for row in data_set:
                user = Person(row)
                if user.monday_status == "Active" and user.phone_sim != "0":
                    try:
                        phone_num = user.phone_sim
                        user.msg = f"""
Einige von uns bevorzugen die Nutzung zusaetzlicher E-Mail-Programme. Wir haben fuer dich Anleitungen zur Konfiguration solcher Programme vorbereitet.Diese findest du in unserem CRM-System: https://crmsystem.monday.com, auf der Verkaeufer-Plattform, im Abschnitt "Konfiguration von E-Mail-Programmen".

Wir wuenschen dir einen schoenen Tag,
dein IT-Team von PLAN [B] ENERGY
"""
                        user.send_sms("Example IT", user.msg, phone_num)
                        print(f"Succes ---> message sent to -> {phone_num}")
                    except:
                        print(f"Error  ---> wrong number    -> {phone_num}")
                sleep(3)



            end_time = time.time()
            time_info(start_time,end_time)

##########################################################################################################################################################################################################
        elif select == "5":
            try:
                for row in data_set:
                    user = Person(row)
                    user_pass = user.passwd
                    start_time = time.time()
                    user.phone_sim = user.transform_german_poland_phone_number()
                    user.footer_generate()
                end_time = time.time()
                time_info(start_time,end_time)
            except:
                print("Soft>>> Succesfuly back to menu !")
##########################################################################################################################################################################################################