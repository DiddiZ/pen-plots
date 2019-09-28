from tempfile import gettempdir
import json
import logging
import time
from pathlib import Path
from pen_plots.util import download

cache_path = Path(gettempdir()) / 'scryfall_cache'
card_database = None
last_scryfall_api_call = 0
scryfall_api_call_delay = 0.05


def __init_cache():
    """
    Downloads card database from Scryfall and places it in a temp dir.
    """
    global card_database

    cache_path.mkdir(parents=True, exist_ok=True)
    card_database = download_cached('https://archive.scryfall.com/json/scryfall-oracle-cards.json')


def search_card_by_name(card_name):
    """
    Searches Scryfall database for all cards with a specific name.
    -------
    list
        of matching cards.
    """
    if card_database is None:
        __init_cache()

    card_name = card_name.lower()

    with open(card_database, "r", encoding="utf-8") as read_file:
        return [card_data for card_data in json.load(read_file) if card_data['name'].lower() == card_name]


def get_image(image_uri):
    return download_cached(image_uri, image_uri.split('/')[-1].split('?')[0])


def download_cached(url, file_name=None):
    """
    Downloads a file places it in the temp dir. Skips if file already cached.

    Returns
    -------
    path
        of downloaded file.
    """
    global last_scryfall_api_call

    if file_name is None:
        file_name = url.split('/')[-1]
    file_path = cache_path / file_name
    if not file_path.is_file():
        logging.info('Downloading %s' % file_name)

        # Sleep to ensure 50ms delay between Scryfall API calls.
        if time.time() < last_scryfall_api_call + scryfall_api_call_delay:
            time.sleep(last_scryfall_api_call + scryfall_api_call_delay - time.time())
        last_scryfall_api_call = time.time()

        download(url, file_path)
    else:
        logging.info('Found %s in cache' % file_name)

    return file_path
