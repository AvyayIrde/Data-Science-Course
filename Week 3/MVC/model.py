# create a file by accepting input from view
# write to file by accepting input from view
# Display contents back to the view

class file:

    def create(self, filename):
        try:
            self.filename = filename
            with open(f'{filename}.txt','x'):
                return
        except:
            print('File seems to already exist')

    def write_content(self,content):
        try:
            with open(f'{self.filename}.txt','a') as file:
                file.write(content)
                file.close()
                return
        except:
            print('File seems to already exist')

    def read(self):
        try:
            with open(f'{self.filename}.txt','r') as file:
                return file.read()
        except:
            print('File seems to already exist')