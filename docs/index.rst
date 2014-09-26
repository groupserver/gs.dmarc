:mod:`gs.dmarc` Documentation
=============================

This product allows systems look up and report on the DMARC
(Domain-based Message Authentication, Reporting and Conformance)
status of a domain [#dmarc]_. DMARC allows the owner of a domain
to publish a key that is used to verify if an email message
actually originated from the domain, and to publish what to do if
the verification fails. It is an extension of DKIM (DomainKeys
Identified Mail, :rfc:`6376`) and SPF (Sender Policy Framework,
:rfc:`4408`).

Specifically this product supplies
:class:`gs.dmarc.ReceiverPolicy` for enumerating the different
DMARC policies, and the :func:`gs.dmarc.receiver_policy` function
for querying the policy for a given domain.

Contents:

.. toctree::
   :maxdepth: 2

   api
   HISTORY

Resources
=========

- Documentation: http://gsdmarc.readthedocs.org/
- Code repository: https://github.com/groupserver/gs.dmarc
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#dmarc] See `the internet-draft`_ Domain-based Message
            Authentication, Reporting and Conformance (DMARC)
.. _the internet-draft: https://datatracker.ietf.org/doc/draft-kucherawy-dmarc-base/?include_text=1

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

