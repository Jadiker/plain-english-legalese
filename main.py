if __name__ == "__main__":
    from tui import display, prompt, choice
    from user_data import login, register, load_users, User, get_user_info
    from dict_data import load_dict
    from search import search_term, TermNotFound
    from contextlib import contextmanager # TODO delete; just for testing

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
                    display("\n" + ("*" * 26))
                    user_choice = options[choice(options)]
                    
                    if user_choice == "Register":
                        username = prompt("Username: ")
                        password = prompt("Password: ")
                        display("") # display a new line
                        try:
                            register(user_database, username, password)
                        except Exception:
                            display("Username already taken")
                            continue
                        display("User successfully registered!")
                        user = login(user_database, username, password)
                        display("User successfully logged in!")
                        continue
                    elif user_choice == "Login":
                        try:
                            username = prompt("Username: ")
                            password = prompt("Password: ")
                            user = login(user_database, username, password)
                            display("User successfully logged in!")
                        except Exception:
                            display("Login unsuccessful")
                        continue
                    elif user_choice == "Logout":
                        user = None
                        display("Successfully logged out!")
                        continue
                    elif user_choice == "Search":
                        term = prompt("What term would you like to search for? ").strip()
                        try:
                            found_term, responses = search_term(term, term_database)
                            plain_responses, legal_responses = responses
                        except TermNotFound as e:
                            display("That term could not be found in database.")
                            if e.close_terms:
                                display("Did you mean any of the following words?\n{}".format(", ".join(e.close_terms)))
                            continue
                        
                        display("The term '{}' was found in the database.".format(found_term))
                            
                        if plain_responses:
                            display("Here are the plain English definitions of '{}':\n\n{}\n".format(found_term, "\n".join(plain_responses)))
                        else:
                            display("No plain definitions of that term were found\n\n")
                        if legal_responses:
                            display("Here are some legal definitions of '{}':\n\n{}\n\n".format(found_term, "\n".join(legal_responses)))
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
