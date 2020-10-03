import os
import json
from helpers.parsers.portals.nehnutelnosti import NehnutelnostiPropertyOffersParser


base_path = os.path.dirname(os.path.realpath(__file__))
sett_path = os.path.join(base_path, 'settings')
uids_path = os.path.join(base_path, 'database')


def load_settings():
    with open(os.path.join(sett_path, 'watchdog.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def load_visited_offers():
    if not os.path.exists(os.path.join(uids_path, 'visited.json')):
        clear_visited_offers()
    with open(os.path.join(uids_path, 'visited.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def save_visited_offers(offers):
    with open(os.path.join(uids_path, 'visited.json'), 'w', encoding='utf-8') as f:
        return json.dump({"offers": offers}, f)


def clear_visited_offers():
    with open(os.path.join(uids_path, 'visited.json'), 'w', encoding='utf-8') as f:
        json.dump({"offers": []}, f)


def watch():

    # Parse the offers
    offers = NehnutelnostiPropertyOffersParser().parse(load_settings()["url"])
    to_see = []

    # get the cache with the already visited offers
    visited = load_visited_offers()
    visited = visited.get("offers", []) if visited else []

    # Get the new offers and update the cache
    for offer in offers:
        if offer["uid"] not in visited:
            visited.append(offer["uid"])
            to_see.append(offer)

    # Save the cache
    save_visited_offers(visited)

    # Return the new offers
    return to_see
