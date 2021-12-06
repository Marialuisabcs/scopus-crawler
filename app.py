from views import CLI
from models import create_tables

def main():
    cli = CLI()
    cli.start()


if __name__ == '__main__':
    create_tables()
    main()
