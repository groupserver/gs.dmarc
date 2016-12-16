# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015, 2016 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from unittest import TestCase
import dns.resolver
from mock import patch
import gs.dmarc.lookup


class TestLookup(TestCase):
    '''Test the lookup of DMARC policies'''

    @staticmethod
    def create_response(policy):
        'Create a fake DMARC response, with the specified ``policy``'
        r = '"v=DMARC1; p={0}; sp=none; pct=100; '\
            'rua=mailto:dmarc-example-rua@example.com, '\
            'mailto:dmarc_e_rua@example.com;"'
        retval = [r.format(policy)]
        return retval

    def lookup_receiver_policy(self, policy):
        'Perform a fake lookup of the DMARC reciever policy'
        queryResp = self.create_response(policy)
        with patch('gs.dmarc.lookup.dns_query') as faux_query:
            faux_query.return_value = queryResp
            retval = gs.dmarc.lookup.lookup_receiver_policy('example.com')
        return retval

    def assertPolicy(self, expected, val):
        m = 'Expected the policy {0}, got {1}'
        msg = m.format(expected, val)

        self.assertEqual(expected, val, msg)

    def test_lookup_none(self):
        'Test the reciever-policy "none"'
        r = self.lookup_receiver_policy('none')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.none, r)

    def test_lookup_reject(self):
        'Test the reciever-policy "reject"'
        r = self.lookup_receiver_policy('reject')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.reject, r)

    def test_lookup_quarantine(self):
        'Test the reciever policy "quarantine".'
        r = self.lookup_receiver_policy('quarantine')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.quarantine, r)

    def test_lookup_monitor(self):
        'Test the reciever-policy "monitor", which is not a reciever policy'
        r = self.lookup_receiver_policy('monitor')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.noDmarc, r)

    @patch('gs.dmarc.lookup.dns_query')
    def test_lookup_nxdomain(self, faux_query):
        'Test a failed lookup of a domain (non-existant domain).'
        faux_query.side_effect = dns.resolver.NXDOMAIN
        r = gs.dmarc.lookup.lookup_receiver_policy('example.com')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.noDmarc, r)

    @patch('gs.dmarc.lookup.dns_query')
    def test_lookup_noanswer(self, faux_query):
        'Test a failed lookup of a domain (no answer).'
        faux_query.side_effect = dns.resolver.NoAnswer
        r = gs.dmarc.lookup.lookup_receiver_policy('example.com')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.noDmarc, r)

    @patch('gs.dmarc.lookup.dns_query')
    def test_lookup_nonameservers(self, faux_query):
        'Test a failed lookup of a domain (no name servers).'
        faux_query.side_effect = dns.resolver.NoNameservers
        r = gs.dmarc.lookup.lookup_receiver_policy('example.com')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.noDmarc, r)

    @patch('gs.dmarc.lookup.dns_query')
    def test_lookup_malformed(self, faux_query):
        '''Test that a response that does not start with "v= is interpreted
        as no DMARC.'''
        # A 'q' is not a '"'.
        a = self.create_response('reject')
        answer = 'q' + a[0]
        queryResp = [answer]
        faux_query.return_value = queryResp
        r = gs.dmarc.lookup.lookup_receiver_policy('example.com')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.noDmarc, r)

    def test_lookup_invalid_policy(self):
        '''Test that an invalid policy-tag raises an error'''
        with self.assertRaises(ValueError):
            gs.dmarc.lookup_receiver_policy('example.com', policyTag='Piranha')

    @patch('gs.dmarc.lookup.dns_query')
    def test_lookup_policy_tag(self, faux_query):
        '''Test that explicitly using the ``p``policy tag is fine.'''
        queryResp = self.create_response('reject')
        faux_query.return_value = queryResp
        r  = gs.dmarc.lookup.lookup_receiver_policy('example.com', policyTag='p')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.reject, r)

    @patch('gs.dmarc.lookup.dns_query')
    def test_lookup_subdomain_policy_tag(self, faux_query):
        '''Test that explicitly using the ``sp``policy tag is fine.'''
        queryResp = self.create_response('reject')
        faux_query.return_value = queryResp
        r  = gs.dmarc.lookup.lookup_receiver_policy('example.com', policyTag='sp')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.none, r)

    @patch('gs.dmarc.lookup.dns_query')
    def test_lookup_policy_fallback(self, faux_query):
        '''Test that the value of the ``p`` tag is returned if the ``sp``policy is absent.'''
        q = self.create_response('reject')[0]
        # Remove the subdomain policy from the DNS return
        faux_query.return_value = [q.replace('sp=none; ', ''), ]
        r  = gs.dmarc.lookup.lookup_receiver_policy('example.com', policyTag='sp')

        self.assertPolicy(gs.dmarc.lookup.ReceiverPolicy.reject, r)
