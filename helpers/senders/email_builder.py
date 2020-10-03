from helpers.parsers.websites.parser import get_domain
from helpers.senders.data_formatter import as_html, as_plain


DELIMITERS = {'html': '<br>', 'plain': '\r\n'}


def get_intro(link, return_type='html'):
    content = [f'Ahoj vole,<br>', f'toto sú nové šmaky na portáli {link}. Nezmeškaj svoju šancu!']
    as_type = DELIMITERS.get(return_type, ' ').join(content)
    return as_type


def get_outro(return_type='html'):
    content = f'Ideme!'
    as_type = DELIMITERS.get(return_type, ' ') + content
    return as_type


def get_email_message_html(body, link):
    intro = get_intro(f'<a href="{link}">{get_domain(link)}</a>', return_type='html')
    offer = as_html(body)
    outro = get_outro(return_type='html')
    return intro + offer + outro


def get_email_message_plain(body, link):
    intro = get_intro(get_domain(link), return_type='plain')
    offer = as_plain(body)
    outro = get_outro(return_type='plain')
    return intro + offer + outro
