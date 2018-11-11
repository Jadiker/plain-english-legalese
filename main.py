if __name__ == "__main__":
    from tui import display, prompt, choice
    from user_data import login, register, load_users, User, get_user_info
    from dict_data import load_dict
    from contextlib import contextmanager # TODO delete; just for testing
    
    # TODO update the placeholders to the correct format
    def placeholder_search_function(dictionary, term):
        try:
            return dictionary[term]
        except KeyError:
            return ([], [])
        
    @contextmanager
    def placeholder_term_database_loader():
        yield {"some term": (["a legal value"], ["a plain value"])}
        
        
    # takes a dictionary and a term to search for in the dictionary
    search_function = placeholder_search_function

    with load_users() as user_database:
        with load_dict() as term_database:
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
                        print("User successfully registered!")
                        user = login(user_database, username, password)
                        print("User successfully logged in!")
                        continue
                    elif user_choice == "Login":
                        try:
                            username = prompt("Username: ")
                            password = prompt("Password: ")
                            user = login(user_database, username, password)
                            display("User successfully logged in!")
                        except Exception:
                            display("Unsuccessful login")
                        continue
                    elif user_choice == "Logout":
                        user = None
                        display("Successfully logged out!")
                        continue
                    elif user_choice == "Search":
                        term = prompt("What term would you like to search for? ").strip()
                        plain_responses, legal_responses = search_function(term_database, term)
                        
                        if plain_responses:
                            display("Here are the plain English definitions of '{}':\n\n{}\n".format(term, "\n".join(plain_responses)))
                        else:
                            display("No plain definitions of that term were found\n\n")
                        if legal_responses:
                            display("Here are some legal definitions of '{}':\n\n{}\n\n".format(term, "\n".join(legal_responses)))
                        else:
                            display("No legal definitions of that term were found\n")
                        continue
                    elif user_choice == "See User Info":
                        display("\n" + get_user_info(user) + "\n")
                        continue
                    elif user_choice == "Quit":
                        display("Goodbye!")
                        break
                    else:
                        print("Something went wrong in the program. Option {} was not recognized".format(user_choice))
                        continue
