from model import file as fl
import view as v

# FYI, we will be executing this file only

if __name__=="__main__":
    file = fl()
    ask_filename = v.ask_file()
    file.create(ask_filename)
    content = v.write()
    file.write_content(content)
    read = v.read()
    if read == 'yes':
        content = file.read()
        v.display(content)
    else:
        print('Thank you for working with my firt MVC code')


