class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def authenticate(self, email, password):
        return self.email == email and self.password == password

    @staticmethod
    def register(name, email, password, users_list):
        if any(user.email == email for user in users_list):
            return None

        new_user = User(name, email, password)
        users_list.append(new_user)
        return new_user