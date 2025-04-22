import json

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
        # self.users[email] = str(hash(password))
        self.users[email] = {"password": password}
        f = open("users/accounts.txt", "w")
        f.write(json.dumps(self.users))
        f.close()

    def get_information(self, email):
        return self.users[email]

    def get_password(self, email):
        return self.users[email]["password"]
