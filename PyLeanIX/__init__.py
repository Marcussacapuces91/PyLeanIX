#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests


class LeanIX:

    def __init__(self, instance: str, api_token: str, proxies=None):
        """Constructor"""
        self._logger = logging.getLogger(__name__)
        self._session = requests.session()
        if proxies:
            self._session.proxies.update(proxies)
        self._instance = instance
        self._access_token = self._get_api_token(api_token)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def _get_api_token(self, api_token: str) -> str:
        """Return access token found using API_TOKEN"""
        response = self._session.post(
            self._instance + '/services/mtm/v1/oauth2/token',
            auth=('apitoken', api_token),
            data={'grant_type': 'client_credentials'}
        )
        response.raise_for_status()
        return response.json()['access_token']

    def request(self, _class: str, params: dict, cur: str = None) -> (str, object):
        params['cursor'] = cur
        response = self._session.get(
            self._instance + '/services/pathfinder/v1/' + _class,
            headers={
                'authorization': 'Bearer ' + self._access_token,
                'accept': 'application/json',
                'cursor': cur
            },
            params=params
        )
        return response.json()['cursor'], response.json()['data']
