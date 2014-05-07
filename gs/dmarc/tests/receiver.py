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
from mock import MagicMock
import gs.dmarc.lookup
from gs.dmarc.lookup import (ReceiverPolicy, receiver_policy,
    PublicSuffixList as psl)


class TestReceiverPolicy(TestCase):
    '''Test the receiver policy'''

    def test_receiver_policy_none(self):
        gs.dmarc.lookup.lookup_receiver_policy = \
            MagicMock(return_value=ReceiverPolicy.none)
        psl.get_public_suffix = MagicMock(return_value='example.com')
        r = receiver_policy('example.com')
        self.assertEqual(1, gs.dmarc.lookup.lookup_receiver_policy.call_count)
        self.assertEqual(0, psl.get_public_suffix.call_count)
        self.assertEqual(r, ReceiverPolicy.none)

    def test_reciver_policy_noDmarc(self):
        gs.dmarc.lookup.lookup_receiver_policy = \
            MagicMock(return_value=ReceiverPolicy.noDmarc)
        psl.get_public_suffix = MagicMock(return_value='example.com')
        r = receiver_policy('may.example.com')
        self.assertEqual(2, gs.dmarc.lookup.lookup_receiver_policy.call_count)
        self.assertEqual(1, psl.get_public_suffix.call_count)
        self.assertEqual(r, ReceiverPolicy.noDmarc)
