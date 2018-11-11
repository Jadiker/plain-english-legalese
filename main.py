if __name__ == "__main__":
    from tui import display, prompt, choice
    from user_data import login, register, load_users, User
    from contextlib import contextmanager # TODO delete; just for testing
    
    class PlaceholderUser:
        def __init__(self, username, password, display_name):
            self.username = username
            self.password = password
            self.display_name = display_name
    
    def placeholder_search_function(dictionary, term):
        print("(Searching {} for term {})".format(dictionary, term))
        try:
            return [dictionary[term]]
        except KeyError:
            return []
        
    @contextmanager
    def placeholder_legal_term_database_loader():
        yield {"a legal term": "a legal value"}
        
    @contextmanager
    def placeholder_plain_term_database_loader():
        yield {"a plain term": "a plain value"}
        
    @contextmanager
    def placeholder_user_database_loader():
        yield {"user": PlaceholderUser("user", "password", "Top Notch")}
        
    def placeholder_login(user_database, username, password):
        print("Using placeholder login")
        user = user_database[username]
        if user.password != password:
            raise RuntimeError("Bad password")
        else:
            return user
            
    def placeholder_get_user_info(user):
        '''Returns a string with information about the user'''
        return "User '{}' with username '{}' and password {}".format(user.display_name, user.username, "*"*len(user.password)) 


    # takes a dictionary and a term to search for in the dictionary
    search_function = placeholder_search_function

    # load term database (context manager)
    legal_term_database_loader = placeholder_legal_term_database_loader
    
    # load plain term database (context manager)
    plain_term_database_loader = placeholder_plain_term_database_loader

    get_user_info = placeholder_get_user_info
    
    with load_users() as user_database:
        with legal_term_database_loader() as legal_term_database:
            with plain_term_database_loader() as plain_term_database:
                user = None
                
                while True:
                    # ["Register", "Login (Logout)", "Search", "(See User Info)", Quit]
                    options = ["Register"]
                    if user:
                        login_or_logout = "Logout"
                    else:
                        login_or_logout = "Login"
                        
                    options.extend([login_or_logout, "Search"])
                    if user:
                        options.append("See User Info")
                    options.append("Quit")
                    user_choice = options[choice(options)]
                    if user_choice == "Register":
                        username = prompt("Username: ")
                        password = prompt("Password: ")
                        register(user_database, username, password)
                    elif user_choice == "Login":
                        try:
                            username = prompt("Username: ")
                            password = prompt("Password: ")
                            user = login(user_database, username, password)
                            display("User successfully logged in!")
                        except Exception:
                            display("Unsuccessful login")
                    elif user_choice == "Logout":
                        user = None
                        display("Successfully logged out!")
                    elif user_choice == "Search":
                        term = prompt("What term would you like to search for? ").strip()
                        legal_response = search_function(legal_term_database, term)
                        plain_response = search_function(plain_term_database, term)
                        
                        display("Here are some legal definitions of {}:\n{}".format("\n".join(term, legal_response)))
                        display("Here are the plain English definitions of {}:\n{}".format("\n".join(term, plain_response)))
                    elif user_choice == "See User Info":
                        display(get_user_info(user))
                    elif user_choice == "Quit":
                        display("Goodbye!")
                        break
                    else:
                        print("Something went wrong in the program. Option {} was not recognized".format(user_choice))
                            
                
