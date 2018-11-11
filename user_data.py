import datetime
import os
import pickle
from contextlib import contextmanager
import subprocess
from logger import Logger
logger = Logger(output_file=os.path.join("user_folder", "log.txt"))
logger.log("Log started at {}".format(datetime.datetime.now().strftime("%H:%M:%S on %b %d, %Y")))


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
        if self.Loginstate == True:
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
                logger.log("loaded users database from {}".format(database_file))
        except FileNotFoundError:
            raise RuntimeError("Most recently saved file {} could not be found".format(repr(database_file)))
    except FileNotFoundError:
        logger.log("Database for USER is not found - new database is created")
        userbase = {}
    try:
        yield userbase
    finally:
        try:
            formated_date_and_time = datetime.datetime.now().strftime("%H_%M_%S_%b_%d_%Y")
        except Exception:
            logger.log("Failed to get date time")
            formated_date_and_time = "Unknown time"
        user_save_file_addr = os.path.join(folder_addr, "db_user_sv_" + formated_date_and_time + ".pkl")
        with open(user_save_file_addr, "wb+") as f2:
            pickle.dump(userbase, f2)

        with open(exact_txt_addr, "w") as f3:
            f3.write(user_save_file_addr)
        logger.log("Userbase saved at: {}".format(repr(user_save_file_addr)))


def login(userbase, username, password):
    try:
        user_obj = userbase[username]
        if (user_obj.login(password) == 0):
            logger.log("LOGGED IN as : {}".format(repr(username)))
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
        logger.log("REGISTERED as: {}".format(repr(username)))


def logout(user_obj):
    user_obj.logout()
    logger.log("LOGGED OUT")


def get_user_info(user_obj):
    user_description = "Username: {}, Points: {}".format(user_obj.get_username(), user_obj.get_points())
    return(user_description)


def add_points(user_obj):
    user_obj.increase_point()
    logger.log("Added 1 point to user: {}".format(user_obj.get_username()))


# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    if os.name == "nt":
        subprocess.run("msg * {}".format(message))
    else:
        os.system('terminal-notifier {}'.format(' '.join([m, t, s])))


def admin_remove_user(userbase, username):
    try:
        del userbase[username]
        print("User {} removed".format(repr(username)))
    except KeyError:
        print("User {} does not exist".format(repr(username)))


if __name__ == "__main__":
    with load_users() as db:
        admin_remove_user(db, "aaa")
        register(db, "aaa", "bbb")
        login(db, "aaa", "bbb")
        add_points(db["aaa"])
        user_info_str = get_user_info(db["aaa"])
        # notify user info in top right
        notify(title='Legalese', subtitle='User info', message=user_info_str)
        logout(db["aaa"])

        # register(db, "aaa", "cc")
        # print(db)
