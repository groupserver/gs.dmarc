:mod:`gs.dmarc` Documentation
=============================

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-06-25
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

.. currentmodule:: gs.dmarc

This product allows systems look up and report on the DMARC
(:rfc:`7489`: Domain-based Message Authentication, Reporting and
Conformance) status of a domain. DMARC allows the owner
of a domain to publish a key that is used to verify if an email
message actually originated from the domain, and to publish what
to do if the verification fails. It is an extension of DKIM
(DomainKeys Identified Mail, :rfc:`6376`) and SPF (Sender Policy
Framework, :rfc:`4408`).

Specifically this product supplies :class:`ReceiverPolicy` for
enumerating the different DMARC policies, and the
:func:`receiver_policy` function for querying the policy for a
given domain.

Contents:

.. toctree::
   :maxdepth: 2

   api
   HISTORY

Resources
=========

- Documentation: http://gsdmarc.readthedocs.io/
- Code repository: https://github.com/groupserver/gs.dmarc
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
