import base64
import json
from django.test import TestCase

import arrow
from django.test import Client
from django.utils import timezone

from entries.models import Entry


class SetupTestCase(TestCase):
    def setup(self):
        self.entries = [{
            "created_at": "Fri May 19 18:20:34 +0000 2017",
            "id": 865633293131063300,
            "lang": "pt",
            "url": "http://spoti.fi/2pZ1NqR",
            "count": 5,
            "location": "RS",
            "text": "Crying in the Club - Camila Cabello"
        }, {

            "lang": "en",
            "count": 32,
            "id": 866775819888336896,
            "location": "rs",
            "text": [],
            "created_at": "Mon May 22 22:00:34 +0000 2017",
            "url": "http://spoti.fi/J7QR2b"
        }, {
            "lang": "en",
            "count": 14,
            "id": 866018919718338560,
            "location": "",
            "text": "Not Today - BTS\nI vote @BTS_twt for the #BTSBBMAs",
            "created_at": "Sat May 20 19:52:54 +0000 2017",
            "url": "http://spoti.fi/2kgImv3"
        }]


class EntriesTestCase(SetupTestCase):
    def test_get(self):
        c = self.get_authenticated_client(self.users[0])
        r = c.get("/api/")
        content = r.json()

        self.assertEqual(len(content), 3)
        c2 = self.get_authenticated_client(self.users[1])
        get_response = c2.get("/api/").json()
        self.assertEqual(len(get_response), 1)
