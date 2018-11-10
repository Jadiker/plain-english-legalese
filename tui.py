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
        print("{}. {}".format(human_index, option))
    
    # ask the user for choices
    number = None
    while number is None:
        try:
            number = int(input("Type the number of the option: "))
            # turn the number into an index
            number -= 1
            if number < 0 or len(options) <= number:
                raise ValueError("Invalid number")
        except Exception: # TODO should this be a ValueError or a general Exception?
            print("Sorry, please enter a number between 1 and {}".format(len(options)))
            number = None
    return number
    
if __name__ == "__main__":
    display("Hello world!")
    user_response = prompt("Testing user input: ")
    print("Got back: {}".format(user_response))
    my_options = ["The first option", "The second option"]
    user_choice = choice(my_options)
    print("The user chose to do the following: {}".format(my_options[user_choice]))
    
    
    
            
    
    
    
    

    
