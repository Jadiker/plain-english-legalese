import datetime
import os
import pickle
from contextlib import contextmanager
import subprocess
from logger import Logger
logger = Logger(output_file=os.path.join("dict_folder", "log.txt"))
logger.log("Log started at {}".format(datetime.datetime.now().strftime("%H:%M:%S on %b %d, %Y")))


@contextmanager
def load_dict():
    folder_addr = "dict_folder"
    txt_addr = "dict_recent_file.txt"
    exact_txt_addr = os.path.join(folder_addr, txt_addr)

    database_file = None

    try:
        with open(exact_txt_addr, "r") as f:
            database_file = f.readline().strip()
            if not database_file:
                raise FileNotFoundError("No top line in dict_recent_file is found")
        try:
            with open(database_file, "rb") as f1:
                dictbase = pickle.load(f1)
                logger.log("loaded dict database from {}".format(database_file))
        except FileNotFoundError:
            raise RuntimeError("Most recently saved file {} could not be found".format(repr(database_file)))
    except FileNotFoundError:
        logger.log("Database for DICT is not found - new database is created")
        dictbase = {}
    try:
        yield dictbase
    finally:
        try:
            formated_date_and_time = datetime.datetime.now().strftime("%H_%M_%S_%b_%d_%Y")
        except Exception:
            logger.log("Failed to get date time")
            formated_date_and_time = "Unknown time"
        dict_save_file_addr = os.path.join(folder_addr, "db_dict_sv_" + formated_date_and_time + ".pkl")
        with open(dict_save_file_addr, "wb+") as f2:
            pickle.dump(dictbase, f2)

        with open(exact_txt_addr, "w") as f3:
            f3.write(dict_save_file_addr)
        logger.log("Dictbase saved at: {}".format(repr(dict_save_file_addr)))


# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    if os.name == "nt":
        subprocess.run("msg * {}".format(message))
    else:
        os.system('terminal-notifier {}'.format(' '.join([m, t, s])))


def index_in(something):
    return something[1][0]


def add_term(dictbase, term):
    try:
        term_obj = dictbase[term]
        raise RuntimeError("This term is already taken")
    except Exception:
        dictbase[term] = ([], [])
        print("term {} added".format(repr(term)))


if __name__ == "__main__":
    with load_dict() as db:
        add_term(db, "UnitedStates")
        print(db["UnitedStates"])
