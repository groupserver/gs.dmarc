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
from gs.dmarc.lookup import lookup_receiver_policy, ReceiverPolicy


class TestContentType(TestCase):
    '''Test the content-type guesser component of gs.form'''

    def test_lookup_none(self):
        host = 'example.com'
        r = lookup_receiver_policy(host)
        self.assertEqual(r, ReceiverPolicy.none)
