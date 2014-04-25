# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
import dns.resolver
from mock import MagicMock
import gs.dmarc.lookup


class TestLookup(TestCase):
    '''Test the lookup of DMARC policies'''

    @staticmethod
    def create_response(policy):
        r = '"v=DMARC1; p={0}; sp=none; pct=100; '\
            'rua=mailto:dmarc-example-rua@example.com, '\
            'mailto:dmarc_e_rua@example.com;"'
        retval = [r.format(policy)]
        return retval

    def lookup_receiver_policy(self, policy):
        queryResp = self.create_response(policy)
        gs.dmarc.lookup.dns_query = MagicMock(return_value=queryResp)
        host = 'example.com'
        retval = gs.dmarc.lookup.lookup_receiver_policy(host)
        return retval

    def test_lookup_none(self):
        r = self.lookup_receiver_policy('none')
        self.assertEqual(r, gs.dmarc.lookup.ReceiverPolicy.none)

    def test_lookup_reject(self):
        r = self.lookup_receiver_policy('reject')
        self.assertEqual(r, gs.dmarc.lookup.ReceiverPolicy.reject)

    def test_lookup_quarantine(self):
        r = self.lookup_receiver_policy('quarantine')
        self.assertEqual(r, gs.dmarc.lookup.ReceiverPolicy.quarantine)

    def test_lookup_nxdomain(self):
        gs.dmarc.lookup.dns_query = MagicMock(side_effect=dns.resolver.NXDOMAIN)
        host = 'example.com'
        r = gs.dmarc.lookup.lookup_receiver_policy(host)
        self.assertEqual(r, gs.dmarc.lookup.ReceiverPolicy.none)

    def test_lookup_noanswer(self):
        gs.dmarc.lookup.dns_query = MagicMock(side_effect=dns.resolver.NoAnswer)
        host = 'example.com'
        r = gs.dmarc.lookup.lookup_receiver_policy(host)
        self.assertEqual(r, gs.dmarc.lookup.ReceiverPolicy.none)
