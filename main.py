#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint

import PyLeanIX
from secrets import API_TOKEN, INSTANCE, PROXIES

if __name__ == '__main__':
    with PyLeanIX.LeanIX(INSTANCE, API_TOKEN, PROXIES) as app:
        cursor = None
        data = list()
        while True:
            c, d = app.request('factSheets', {
                'type': 'Application',
                'archivedOnly': False,
                'pageSize': 50,
                'permissions': False,
                'completion': True,
                'documents': True,
                'tags': True,
                'subscriptions': True,
                'constrainingRelations': True
            }, cursor)
            if d:
                data += d
                cursor = c
            else:
                break

        for line in data:
            pprint(line, indent=1, width=132, sort_dicts=False)
