import requests
import pycountry
from urllib.parse import urlencode

from ..service import Service

service = Service(__name__)


@service.command(r"(?:translate) (?P<term>.+?)(?: from (?P<from_lang>.+?))? to (?P<to_lang>.+)$", mention=True, background=True)
def search(client, target, origin, term, to_lang, from_lang=None):
    if from_lang is None:
        sl = None
    else:
        try:
            sl = pycountry.languages.get(name=from_lang.title())
        except KeyError:
            client.message(target, "{origin}: Sorry, I don't understand \"{lang}\".".format(
                origin=origin,
                lang=from_lang
            ))
            return

    try:
        tl = pycountry.languages.get(name=to_lang.title())
    except KeyError:
        client.message(target, "{origin}: Sorry, I don't understand \"{lang}\".".format(
            origin=origin,
            lang=to_lang
        ))
        return

    r = requests.get("http://translate.google.com/translate_a/t?" + urlencode({
        "client": "p",
        "sl": "auto" if sl is None else sl.alpha2,
        "tl": tl.alpha2,
        "text": term,
        "ie": "UTF-8",
        "oe": "UTF-8"
    })).json()

    client.message(target, "{origin}: {sentences}".format(
        origin=origin,
        sentences=" ".join(x["trans"] for x in r["sentences"])
    ))