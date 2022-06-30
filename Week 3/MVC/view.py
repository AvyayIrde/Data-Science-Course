

def ask_file():
    file_name = input('Hello user, enter the name of the file you want to create: ')
    return file_name

def write():
    content = input('hello user, type below the text you want to enter to the file created:\n')
    return content.lower()

def read():
    read = input('Enter yes to display the content or anything else to continue: ')
    return read.lower()

def display(content):
    print("This is the content from your file :\n",content)