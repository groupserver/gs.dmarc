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
from dns.resolver import query as dns_query, NXDOMAIN, NoAnswer


class ReceiverPolicy(Enum):
    '''An enumeration of the different receiver policies in DMARC.'''
    __order__ = 'none quarantine reject'  # only needed in 2.x

    #: No DMARC policy. Should be interpreted the same way as
    #: :attr:`gs.dmarc.ReceiverPolicy.none`.
    noDmarc = 0

    #: The published policy is ``none``. Recieving parties are supposed to
    #: skip the verification of the DMARC signature.
    none = 1

    #: Generally causes the message to be marked as *spam* if verification
    #: fails.
    quarantine = 2

    #: Causes the system that is receiving the message to reject the message if
    #: the verification fails.
    reject = 3


def answer_to_dict(answer):
    '''Turn the DNS DMARC answer into a dict of tag:value pairs.'''
    a = answer.strip('"').strip(' ')
    rawTags = [t.split('=') for t in a.split(';') if t]
    tags = [(t[0].strip(), t[1].strip()) for t in rawTags]
    retval = dict(tags)
    return retval


def lookup_receiver_policy(host):
    '''Lookup the reciever policy for a host. Returns a ReceiverPolicy.

    :param str host: The host to query. The *actual* host that is queried has
                     ``_dmarc.`` prepended to it.
    :return: The DMARC receiver policy for the host. If there is no published
             then :attr:`gs.dmarc.ReceiverPolicy.noDmarc` is returned.
    :rtype: A member of the :class:`gs.dmarc.ReceiverPolicy` enumeration.


    The :func:`lookup_receiver_policy` function is intended to determine if
    a DMARC receiver policy will cause issues for a particular host.

    Example:
        Get the host from an email address, and get the receiver policy::

            addr = email.utils.parseaddr('mpj17@onlinegroups.net')
            host = addr[1].split('@')[1]
            policy = lookup_receiver_policy(host)

            if (policy in (ReceiverPolicy.quarintine, ReceiverPolicy.reject)):
                # Rewrite the From header
'''
    dmarcHost = '_dmarc.{0}'.format(host)
    try:
        dnsAnswer = dns_query(dmarcHost, 'TXT')
    except (NXDOMAIN, NoAnswer):
        retval = ReceiverPolicy.noDmarc
    else:
        answer = str(dnsAnswer[0])
        tags = answer_to_dict(answer)
        policy = tags.get('p', 'none')
        retval = ReceiverPolicy[policy]

    assert isinstance(retval, ReceiverPolicy)
    return retval
