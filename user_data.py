import datetime
import os
import pickle
from contextlib import contextmanager

login_state = 0     # 0 is logged out, 1 is in
id_increment = 0


class User(object):
    def __init__(self, username, password):
        # self.Id = id
        self.Username = username
        self.Password = password
        self.Loginstate = True   # true or false
        self.Points = 0

    def get_loginstate(self):
        return self.Loginstate

    def get_username(self):
        return self.Username

    def get_points(self):
        return self.Points

    def login(self, password):
        if password == self.Password:
            self.Loginstate = True
            return 0
        else:
            return -1

    def logout(self):
        self.Loginstate = False
        return 0

    def increase_point(self):       # called when user updates a term
                                        # which requires loged in
        if Loginstate == True:
            self.Points += 1
            return 0
        else:
            return -1


@contextmanager
def load_users():
    folder_addr = "user_folder"
    txt_addr = "user_recent_file.txt"
    exact_txt_addr = os.path.join(folder_addr, txt_addr)

    database_file = None

    try:
        with open(exact_txt_addr, "r") as f:
            database_file = f.readline().strip()
            if not database_file:
                raise FileNotFoundError("No top line in user_recent_file is found")
        try:
            with open(database_file, "rb") as f1:
                userbase = pickle.load(f1)
                print("loaded users database from {}".format(database_file))
        except FileNotFoundError:
            raise RuntimeError("Most recently saved file {} could not be found".format(repr(database_file)))
    except FileNotFoundError:
        print("Database for USER is not found - new database is created")
        userbase = {}
    try:
        yield userbase
    finally:
        try:
            formated_date_and_time = datetime.datetime.now().strftime("%H_%M_%S_%b_%d_%Y")
        except Exception:
            print("Failed to get date time")
            formated_date_and_time = "Unknown time"
        user_save_file_addr = os.path.join(folder_addr, "db_user_sv_" + formated_date_and_time + ".pkl")
        with open(user_save_file_addr, "wb+") as f2:
            pickle.dump(userbase, f2)

        with open(exact_txt_addr, "w") as f3:
            f3.write(user_save_file_addr)
        print("Userbase saved at: {}".format(repr(user_save_file_addr)))


def login(userbase, username, password):
    try:
        user_obj = userbase[username]
        if (user_obj.login(password) == 0):
            print("LOGGED IN as : {}".format(repr(username)))
            return user_obj
        else:
            raise RuntimeError("Login unsuccessful")
    except KeyError:
        raise RuntimeError("Username does not exist")


def register(userbase, username, password):
    try:
        user_obj = userbase[username]
        raise RuntimeError("Username taken")
    except KeyError:
        userbase[username] = User(username, password)
        print("REGISTERRED and LOGGED IN as: {}".format(repr(username)))


def logout(userbase, username):
    try:
        user_obj = userbase[username]
        user_obj.logout()
        print("LOGGED OUT")
    except KeyError:
        raise RuntimeError("No such user, weird, check code")


def get_user_info(user_obj):
    user_description = "Username: {}, Points: {}".format(user_obj.get_username(), user_obj.get_points())
    return(user_description)


if __name__ == "__main__":
    with load_users() as db:
        # register(db, "aaa", "bbb")
        login(db, "aaa", "bbb")
        get_user_info(db["aaa"])
        logout(db, "aaa")
        # register(db, "aaa", "cc")
        # print(db)
