#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint

import PyLeanIX
from PyLeanIX import LeanIX
from my_secrets import API_TOKEN, INSTANCE, PROXIES

from flask import Flask, escape, g, current_app


def get_leanix():
    with app.app_context() as ctx:
        try:
            return current_app.leanix
        except AttributeError:
            current_app.leanix = PyLeanIX.LeanIX(INSTANCE, API_TOKEN)
            print("create leanix")
            return current_app.leanix


app = Flask(__name__)
app.leanix = PyLeanIX.LeanIX(INSTANCE, API_TOKEN) #, PROXIES)
# print("Leanix")


@app.route('/')
def index():
    """Retourne la page d'accueil du site avec la liste générale des applications"""
    body: str = '<h1>Welcome to LeanIX interface app !</h1>'
    body += "<ul>"

    cursor = None
    while True:
        c, d = get_leanix().request('factSheets', {
            'type': 'Application',
            'archivedOnly': False,
            'names': False,
            'permissions': False,
            'completion': False,
            'documents': False,
            'tags': False,
            'fields': False,
            'constrainingRelations': True,
            'subscriptions': False
            #            'constrainingRelations': False
        }, cursor)
        if d:
            # print(f"Taille de la réponse : {len(d)}")
            for line in d:
                body += "<li>\n"
                body += f"  <h2><a href=\'{INSTANCE + '/itmlive/factsheet/Application/' + line['id']}\'>" \
                        f"{line.get('display_name', line['name'])}" \
                        "</a></h2>\n"
                body += f"  <p>{line.get('description', '<i>Pas de description</i>')}</p>\n".replace('\n', '<br/>')

                if line.get('fields'):
                    body += "  <h3>Champs</h3>\n"
                    body += "  <ul>\n"
                    for f in line['fields']:
                        if f['name'] == 'externalId':
                            body += f"    <li>Code Application : {f['data']['externalId']}</li>\n"
                    body += "  </ul>\n"

                body += f'<pre>{pprint.pformat(line, indent=1, width=132, sort_dicts=False)}</pre>\n'
                body += "</li>\n"
            cursor = c
        else:
            break

    body += "</ul>"
    return body


if __name__ == '__main__' or __name__ == 'main':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
