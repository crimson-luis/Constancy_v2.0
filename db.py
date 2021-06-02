# import Fernet
users = []

class User:
    def __init__(self, name: str, password: str, email: str):
        self.name = name
        self.password = password
        # self.password = blake2b(password.encode('UTF-8')).hexdigest()
        self.email = email
        self.plan = 'basic'
        self.reset_code = ''

    def __repr__(self):
        return f'Name: {self.name}, email {self.email}, password: {self.password}'

    def reset_password(self, code: str, new_password: str):
        if code != self.reset_code:
            raise Exception('Invalid code.')
        self.password = new_password

# def create_user(name: str, password: str, email: str)
