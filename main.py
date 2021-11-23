from __future__ import annotations

import time
from pathlib import Path

import crawler


def start_bot():
    search_string = input('>> Enter your search string: ')

    download_dir = Path.cwd() / 'downloads'
    download_dir.mkdir(exist_ok=True)
    download_dir = str(download_dir)

    driver = crawler.Drivers.firefox(download_dir)
    bot = crawler.ScopusCitationBot(driver, download_dir, search_string)

    print('Start a session in scopus.')
    input('>> Press enter when you are done...')

    bot.start_session()

    run_bot(bot)


def run_bot(bot: crawler.ScopusCitationBot):
    year = 1990
    while year <= 2022:
        bot.get_url(year)
        bot.export_csv_with_abstracts(1)
        year += 1
        # time.sleep(5)

    bot.end_session()


if __name__ == '__main__':
    start_bot()
