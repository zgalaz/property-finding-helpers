def as_html(r):

    # Prepare the content
    content = [
        f'<a href="{p["url"]}">{p["label"]}</a> '
        f'adresa: {p["address"]}, '
        f'rozloha: {p["area"]}, '
        f'cena: {p["price"]} ({p["price_per_square"]})'
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
        f'cena: {p["price"]} ({p["price_per_square"]})'
        for p in r
    ]

    # Format the content
    return '\r\n'.join(content)
