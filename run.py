import os
import argparse
from datetime import datetime
from helpers.watchdog import dog
from helpers.parsers.portals.nehnutelnosti import NehnutelnostiPropertyOffersParser
from helpers.utils.common import ensure_path
from helpers.senders.email_sender import send_email, prepare_email
from helpers.senders.email_builder import get_email_message_html, get_email_message_plain


# Prepare the base paths
THIS_PATH = os.path.realpath(__file__)
BASE_PATH = os.path.dirname(THIS_PATH)

# Prepare the analytical timestamp
TODAY = datetime.now()
today = f'{TODAY.day}. {TODAY.month}. {TODAY.year}'

# Prepare the settings path/presence
ensure_path(os.path.join(BASE_PATH, "settings"))
ensure_path(os.path.join(BASE_PATH, "helpers", "watchdog", "settings"))

# Prepare the database path/presence
ensure_path(os.path.join(BASE_PATH, "helpers", "watchdog", "database"))


if __name__ == '__main__':

    # -------------------------
    # Parse the input arguments
    # -------------------------

    arg_parser = argparse.ArgumentParser(description='Property offers parser')
    arg_parser.add_argument('-n', '--new', type=bool, help='new watchdog (delete the cache of the visited ids)')
    arg_parser.add_argument('-e', '--email', type=str, help='email of the recipient')
    args = arg_parser.parse_args()

    # ---------------------
    # Prepare the machinery
    # ---------------------

    # Prepare e-mail sending
    u_name, d_name = prepare_email(args.email)

    # ---------------------------
    # Prepare the property parser
    # ---------------------------

    # Prepare the parser
    parser = NehnutelnostiPropertyOffersParser()

    # -------------------------
    # Parse the property offers
    # -------------------------

    # Clear the cache with the visited offers if the new run is desired
    if args.new:
        dog.clear_visited_offers()

    # Get the new offers to be checked
    offers = dog.watch(parser)

    if offers:

        # Prepare the message
        message_text = get_email_message_plain(offers, parser.weburl)
        message_html = get_email_message_html(offers, parser.weburl)

        # Send the offers
        #
        # Needs the less secure access to be turned on: https://myaccount.google.com/u/2/lesssecureapps?pageId=none
        # More info: https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp
        send_email(from_address='property.finder.helpers@gmail.com',
                   to_address={'username': u_name, 'domain': d_name},
                   subject=f'nehnutelnosti.sk {today}',
                   plaintext=message_text,
                   html=message_html)
