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
from enum import Enum


class ReceiverPolicy(Enum):
    '''The different receiver policies in DMARC.'''
    __order__ = 'none quarantine reject'  # only needed in 2.x
    none = 1
    quarantine = 2
    reject = 3


def lookup_receiver_policy(host):
    '''Lookup the reciever policy for a host. Returns a ReceiverPolicy'''
    retval = ReceiverPolicy.none
    assert isinstance(retval, ReceiverPolicy)
    return retval
