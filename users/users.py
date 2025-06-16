import json
import codecs
import re
import base64
import shutil
import os

class Users():
    def __init__(self):
        f = open("users/accounts.txt", "r")
        value = f.read()
        try:
            self.users = json.loads(value)
        except:
            self.users = {}
        f.close()

    def add_user(self, email, password):
        self.users[email] = {"password": password}
        f = open("users/accounts.txt", "w")
        f.write(json.dumps(self.users))
        f.close()
    

    def add_phone(self, email, phone):
        if email not in self.users:
            return
            
        self.users[email].update({"phone": phone})
        f = open("users/accounts.txt", "w")
        f.write(json.dumps(self.users))
        f.close()

    def add_resume(self, email, resume_file_path):
        if email not in self.users:
            return
        
        resume_name = re.search(r'(?<=\/)[ A-z]+\.[A-z]+', resume_file_path).group()
        self.users[email].update({"resume_name": resume_name})
        f = open("users/accounts.txt", "w")
        f.write(json.dumps(self.users))
        f.close()


        source = resume_file_path
        destination = os.getcwd()+ "/users/resumes/" + resume_name
        dest = shutil.copyfile(source, destination)

    def get_information(self, email):
        return self.users[email]

    def get_password(self, email):
        return self.users[email]["password"]

if __name__ == "__main__":
    users = Users()
    # users.add_user("rileyjthompson5@gmail.com", "test")
    # users.add_phone("rileyjthompson5@gmail.com", "6507874705")
    users.add_resume("rileyjthompson5@gmail.com", "../../../Desktop/resume/Riley Thompson Resume.pdf")