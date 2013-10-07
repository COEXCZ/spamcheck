# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__all__ = ('spamcheck',)
__author__ = u"Jan Češpivo, COEX CZ s.r.o (http://www.coex.cz)"

from urllib2 import Request, urlopen
from simplejson import dumps, loads

try:
    from django.conf import settings
    SPAM_CHECK_URL = getattr(settings, 'SPAM_CHECK_URL')
except (ImportError, AttributeError):
    SPAM_CHECK_URL = 'http://spamcheck.postmarkapp.com/filter'


def spamcheck(raw_email, url=SPAM_CHECK_URL):

    data = dict(email=raw_email, options='long')
    json = dumps(data)

    req = Request(url, json, {'Accept': 'application/json', 'Content-Type': 'application/json'})
    result = urlopen(req)
    for row in result:
        response = loads(row)
    result.close()

    success = response['success']
    spam_score = float(response['score'])
    spam_report = response['report']

    return success, spam_score, spam_report
