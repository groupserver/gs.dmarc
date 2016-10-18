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
from __future__ import absolute_import, unicode_literals
from enum import Enum
from pkg_resources import resource_filename  # Part of setuptools
try:
    # typing is needed by mypy, but is unused otherwise
    from typing import Dict, Text  # noqa: F401
except ImportError:
    pass
from dns.resolver import (query as dns_query, NXDOMAIN, NoAnswer,
                          NoNameservers)
from publicsuffix import PublicSuffixList


class ReceiverPolicy(Enum):
    '''An enumeration of the different receiver policies in DMARC.'''
    __order__ = 'noDmarc none quarantine reject'  # only needed in 2.x

    #: No published DMARC receiver-policy could be found. Often interpreted
    #: the same way as :attr:`gs.dmarc.ReceiverPolicy.none`.
    noDmarc = 0

    #: The published policy is ``none``. Recieving parties are supposed to
    #: skip the verification of the DMARC signature.
    none = 1

    #: Generally causes the message to be marked as *spam* if verification
    #: fails.
    quarantine = 2

    #: Causes the system that is receiving the message to reject the
    #: message if the verification fails.
    reject = 3


def answer_to_dict(answer):
    # type: (Text) -> Dict[unicode, unicode]
    '''Turn the DNS DMARC answer into a dict of tag:value pairs.'''
    a = answer.strip('"').strip(' ')
    rawTags = [t.split('=') for t in a.split(';') if t]
    retval = {t[0].strip(): t[1].strip() for t in rawTags}
    return retval


def lookup_receiver_policy(host):
    # type: (str) -> ReceiverPolicy
    '''Lookup the reciever policy for a host. Returns a ReceiverPolicy.

:param str host: The host to query. The *actual* host that is queried has
                 ``_dmarc.`` prepended to it.
:returns: The DMARC receiver policy for the host. If there is no published
          policy then :attr:`gs.dmarc.ReceiverPolicy.noDmarc` is returned.
:rtype: A member of the :class:`gs.dmarc.ReceiverPolicy` enumeration.'''
    dmarcHost = '_dmarc.{0}'.format(host)
    retval = ReceiverPolicy.noDmarc
    try:
        dnsAnswer = dns_query(dmarcHost, 'TXT')
    except (NXDOMAIN, NoAnswer, NoNameservers):
        pass  # retval = ReceiverPolicy.noDmarc
    else:
        answer = str(dnsAnswer[0])
        # Check that v= field is the first one in the answer (which is in
        # double quotes) as per Section 7.1 (5):
        #     In particular, the "v=DMARC1" tag is mandatory and MUST appear
        #     first in the list. Discard any that do not pass this test.
        # http://tools.ietf.org/html/draft-kucherawy-dmarc-base-04#section-7.1
        if answer[:9] == '"v=DMARC1':
            tags = answer_to_dict(answer)
            # TODO: check that 'none' is the right assumption?
            p = tags.get('p', 'none')
            policy = p if hasattr(ReceiverPolicy, p) else 'noDmarc'
            # https://github.com/python/mypy/issues/1381
            retval = ReceiverPolicy[policy]  # type: ignore
        # else: retval = ReceiverPolicy.noDmarc
    return retval


def receiver_policy(host):
    # type: (str) -> ReceiverPolicy
    '''Get the DMARC receiver policy for a host.

:param str host: The host to lookup.
:returns: The DMARC reciever policy for the host.
:rtype:  A member of the :class:`gs.dmarc.ReceiverPolicy` enumeration.

The :func:`receiver_policy` function looks up the DMARC reciever polciy
for ``host``. If the host does not have a pubished policy
`the organizational domain`_ is determined and the DMARC policy for this is
returned. Internally the :func:`gs.dmarc.lookup.lookup_receiver_policy` is
used to perform the query.

.. _the organizational domain:
   http://tools.ietf.org/html/draft-kucherawy-dmarc-base-04#section-3.2'''
    hostSansDmarc = host if host[:7] != '_dmarc.' else host[7:]

    retval = lookup_receiver_policy(hostSansDmarc)
    if retval == ReceiverPolicy.noDmarc:
        fn = get_suffix_list_file_name()
        with open(fn) as suffixList:
            psl = PublicSuffixList(suffixList)
            newHost = psl.get_public_suffix(hostSansDmarc)
        # TODO: Look up the subdomain policy
        retval = lookup_receiver_policy(newHost)
    return retval


def get_suffix_list_file_name():
    # type: () -> Text
    '''Get the file name for the public-suffix list data file

:returns: The filename for the datafile in this module.
:rtype: ``str``'''
    # TODO: automatically update the suffix list data file
    # <https://publicsuffix.org/list/effective_tld_names.dat>
    retval = resource_filename('gs.dmarc', 'suffixlist.txt')
    return retval
