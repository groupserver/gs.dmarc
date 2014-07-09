# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from mock import MagicMock
import gs.dmarc.lookup
from gs.dmarc.lookup import (ReceiverPolicy, receiver_policy,
                             PublicSuffixList as psl)


class TestReceiverPolicy(TestCase):
    '''Test the receiver policy'''

    def test_suffix_file(self):
        'Test that we can read the data file for the public suffix list'
        fn = gs.dmarc.lookup.get_suffix_list_file_name()
        self.assertEqual('txt', fn[-3:])
        with open(fn, 'r') as infile:
            l = infile.readline()
        self.assertEqual('// This Source Code Form', l[:24])

    def test_receiver_policy_none(self):
        'Test that we only look up the reciever policy once if it is "none"'
        gs.dmarc.lookup.lookup_receiver_policy = \
            MagicMock(return_value=ReceiverPolicy.none)
        psl.get_public_suffix = MagicMock(return_value='example.com')
        r = receiver_policy('example.com')

        cc = gs.dmarc.lookup.lookup_receiver_policy.call_count
        self.assertEqual(1, cc)
        self.assertEqual(0, psl.get_public_suffix.call_count)
        self.assertEqual(r, ReceiverPolicy.none)

    def test_reciver_policy_noDmarc(self):
        'Test that we look up the public suffix for the host for "no dmarc"'
        gs.dmarc.lookup.lookup_receiver_policy = \
            MagicMock(return_value=ReceiverPolicy.noDmarc)
        psl.get_public_suffix = MagicMock(return_value='example.com')
        r = receiver_policy('my.example.com')

        cc = gs.dmarc.lookup.lookup_receiver_policy.call_count
        self.assertEqual(2, cc)
        self.assertEqual(1, psl.get_public_suffix.call_count)
        self.assertEqual(r, ReceiverPolicy.noDmarc)

    def test_dmarc_host(self):
        'Test a host lookup when "_dmarc." something is given'
        gs.dmarc.lookup.lookup_receiver_policy = \
            MagicMock(return_value=ReceiverPolicy.none)
        psl.get_public_suffix = MagicMock(return_value='example.com')
        r = receiver_policy('_dmarc.example.com')

        cc = gs.dmarc.lookup.lookup_receiver_policy.call_count
        self.assertEqual(1, cc)
        self.assertEqual(0, psl.get_public_suffix.call_count)
        self.assertEqual(r, ReceiverPolicy.none)

        args, kw_args = gs.dmarc.lookup.lookup_receiver_policy.call_args
        self.assertEqual('example.com', args[0])