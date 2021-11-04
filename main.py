from __future__ import annotations

from pathlib import Path

import crawler


def download():
    download_dir = Path.cwd() / 'downloads'
    download_dir.mkdir(exist_ok=True)
    download_dir = str(download_dir)

    driver = crawler.Drivers.firefox(download_dir)

    search_string = input('>> Enter your search string: ')
    bot = crawler.ScopusCitationBot(driver, download_dir, search_string)

    print('Start a session in scopus.')
    input('>> Press enter when you are done...')

    bot.start_session()
    bot.export_csv_with_abstracts(1)
    bot.end_session()


if __name__ == '__main__':
    download()
