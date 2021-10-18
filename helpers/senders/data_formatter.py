def get_pride_per_square_str(record):
    return f' ({record["price_per_square"]}) ' if "price_per_square" in record else ''


def get_price_str(record):
    return record["price"]


def as_html(r):

    # Prepare the content
    content = [
        f'<a href="{p["url"]}">{p["label"]}</a> '
        f'adresa: {p["address"]}, '
        f'rozloha: {p["area"]}, '
        f'cena: {get_price_str(p)}{get_pride_per_square_str(p)}'
        for p in r
    ]

    # Format the content
    return '<ol>' + ' '.join(f'<li>{m}</li>' for m in content) + '</ol>'


def as_plain(r):

    # Prepare the content
    content = [
        f'<a href="{p["url"]}">{p["label"]}</a> '
        f'adresa: {p["address"]}, '
        f'rozloha: {p["area"]}, '
        f'cena: {get_price_str(p)}{get_pride_per_square_str(p)}'
        for p in r
    ]

    # Format the content
    return '\r\n'.join(content)
