"""Enter the following code in the destination file to import the confirmation function.

customs = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))
sys.path.insert(0, customs)

"""

def confirmation(message):
    confirm = input (message + " (y/n): ").lower()
    #Ensure valid input
    while confirm not in ["yes", "no", "y", "n"]:
        confirm = input("Invalid input! Please enter 'y' or 'n': ")
    #Return boolean based on confirmation
    if confirm in ["yes", "y"]:
        return True
    else:
        return False