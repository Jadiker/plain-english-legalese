import datetime
import os
import pickle
from contextlib import contextmanager

@contextmanager
def load():
    # things we can define
    save_folder = "database"
    most_recent_save_file = "_most_recent_save.txt"
    
    # the rest of the code
    exact_most_recent_save_file = os.path.join(save_folder, most_recent_save_file)
    database_file = None
    try:
        with open(exact_most_recent_save_file, "r") as f:
            database_file = f.readline().strip()
            if not database_file:
                raise FileNotFoundError("No file was found in the most recent save file")
            try:
                database_file = database_file
                with open(database_file, "rb") as f2:
                    database = pickle.load(f2)
                    print("Loaded database from {}".format(database_file))
            except FileNotFoundError:
                raise RuntimeError("Most recent save file {} could not be found".format(repr(database_file)))
    except FileNotFoundError:
        # the most recent save file was not found, or there was no file listed inside that file
        # so, we make an empty database
        print("Database not loaded - blank database created")
        database = {}
    try:
        yield database
    finally:
        try:
            formatted_date_and_time = datetime.datetime.now().strftime("%H_%M_%S_%b_%d_%Y")
        except Exception:
            print("Failed to obtain formatted date and time!")
            formatted_date_and_time = "Unknown Time"
        
        save_file = os.path.join(save_folder, "db_sv_" + formatted_date_and_time + ".pkl")
        with open(save_file, "wb+") as f:
            pickle.dump(database, f)
        
        with open(exact_most_recent_save_file, "w") as f:
            f.write(save_file)
            
        print("Database saved at: {}".format(save_file))


if __name__ == "__main__":
    with load() as db:
        # do whatever you want with the database
        print(db)
