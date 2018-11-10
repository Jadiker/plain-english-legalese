
login_state = 0     # 0 is logged out, 1 is in
id_increment = 0


class User(object):
    def __init__(self, id, username, password):
        self.Id = id
        self.Username = username
        self.Password = password
        self.Loginstate = True   # true or false
        self.Points = 0

    def get_loginstate(self):
        return self.Loginstate

    def get_username(self):
        return self.Username

    def login(self, password):
        if password == self.Password:
            self.Loginstate = True

    def logout(self):
        self.Loginstate = False

    def increase_point(self):       # called when user updates a term
                                        # which requires loged in
        if Loginstate == True:
            self.Points += 1


def register(id_i, username, password):
    users[id_i] = User(id_i, username, password)


def main():
    global users = {}
