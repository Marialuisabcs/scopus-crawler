import csv
import os.path
import sys
import glob

from furl import furl
from pathlib import Path

from crawler import main
from models import Study


class CLI:
    def __init__(self):
        self.folder = None
        self.options = {
            'help': self.help,
            'run-bot': self.run_bot,
            'set-folder': self.set_folder,
            'save-csv': self.save_csv(),
            'exit': lambda: sys.exit(1)
        }

    def request_option(self):
        option = input('>> ')
        while option not in self.options:
            print('Invalid option, try again.')
            option = input('>> Option: ')

        self.options[option]()

    def help(self):
        for option in self.options:
            print(option)

        self.request_option()

    def run_bot(self):
        print('Starting bot...\n')
        main.start_bot()

        self.request_option()

    def set_folder(self):
        folder_name = input('>> Folder name: ')

        while not folder_name:
            print('Folder name can not be empty')
            folder_name = input('>> Folder name: ')

        if os.path.isdir(Path.cwd() / 'outputs' / folder_name):
            self.folder = folder_name

        print('Folder selected succesfully!')
        print('Current folder: ' + str(self.folder))

        self.request_option()

    def save_csv(self):
        path = (Path.cwd() / 'outputs' / self.folder)
        extension = 'csv'
        os.chdir(path)
        files = glob.glob('*.{}'.format(extension))
        studies_added_count = 0
        total_studies_count = 0
        for file in files:
            with open(path / file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_studies_count += 1
                    eid = furl(row['Link']).args['eid']
                    if check_eid(eid):
                        Study.create(
                            title=row['Title'],
                            abstract=row['Abstract'],
                            eid=eid,
                        )
                        studies_added_count += 1

        print(f'{studies_added_count} from {total_studies_count} sutudies added')

    def start(self):
        print('Type `help` for help')
        self.request_option()


def check_eid(eid):
    query = Study.select().where(Study.eid == eid)

    if query:
        return True

    return False


if __name__ == '__main__':
    cli = CLI()
    cli.start()
