def display(text):
    '''
    Display one line of text on the screen
    
    text is a string
    '''
    print(text)
    
def prompt(prompt):
    '''
    Prompts the user for a value
    
    prompt is a string
    '''
    return input(prompt)
    
def choice(options):
    '''
    Display a list of options of what the user can do and let the user pick one
    
    options is a list of strings (each one is an option the user can choose)
    '''
    print("What would you like to do?")
    for index, option in enumerate(options):
        human_index = index + 1
        print("    {}. {}".format(human_index, option))
    print()
    
    # ask the user for choices
    number = None
    while number is None:
        try:
            user_input = input("Type the number or the option: ")
            try:
                number = int(user_input)
            except ValueError:
                simple_user_input = user_input.strip().lower()
                for index, option in enumerate(options):
                    simple_option = option.strip().lower()
                    if simple_user_input == simple_option:
                        number = index + 1
            number -= 1
            if number < 0 or len(options) <= number:
                raise ValueError("Invalid number")
                
        except Exception: # TODO should this be a ValueError or a general Exception?
            print("Sorry, please enter a number between 1 and {} or the exact option".format(len(options)))
            number = None
    return number
    
if __name__ == "__main__":
    display("Hello world!")
    user_response = prompt("Testing user input: ")
    print("Got back: {}".format(user_response))
    # my_options = ["The first option", "The second option"]
    # user_choice = choice(my_options)
    # print("The user chose to do the following: {}".format(my_options[user_choice]))
    
    
    
            
    
    
    
    

    
