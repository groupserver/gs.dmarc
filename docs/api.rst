:mod:`gs.dmarc` API Reference
=============================

.. currentmodule:: gs.dmarc

Currently only querying the DMARC `receiver policy`_ is
supported.

Receiver Policy
---------------

A DMARC receiver policy is published in a DNS ``TXT`` record, in
a domain that starts with ``_dmarc``. It is possible to use the
:program:`host` program to look up a DMARC record.

.. code-block:: bash

  $ host -t TXT _dmarc.yahoo.com
  _dmarc.yahoo.com descriptive text "v=DMARC1\; p=reject\; sp=none\; pct=100\; rua=mailto:dmarc-yahoo-rua@yahoo-inc.com, mailto:dmarc_y_rua@yahoo.com\;"

The :func:`receiver_policy` function performs the DNS query,
parses the results, and returns the policy for the host. The
different policies are listed by the :class:`ReceiverPolicy`
enumeration.

.. autofunction:: gs.dmarc.receiver_policy

.. autoclass:: gs.dmarc.ReceiverPolicy
   :members:

Example
~~~~~~~

Get the host from an email address, and get the receiver policy.

.. code-block:: python

    addr = email.utils.parseaddr('mpj17@onlinegroups.net')
    host = addr[1].split('@')[1]
    policy = receiver_policy(host)

    if (policy in (ReceiverPolicy.quarintine, ReceiverPolicy.reject)):
        # Rewrite the From header

.. seealso::

   :mod:`publicsuffixlist`
        The organizational domain is determined by the publicsuffixlist_
        product.

   :mod:`dnspython`
        The `dnspython`_ product is used to perform the DNS query.

   :mod:`enum34`
        The `enum34`_ product is used to provide enumeration
        support in versions of Python prior to 3.4.

.. _publicsuffixlist: https://pypi.python.org/pypi/publicsuffix
.. _dnspython: https://pypi.python.org/pypi/dnspython
.. _enum34: https://pypi.python.org/pypi/enum34

Internal
--------

Internally the :func:`lookup.lookup_receiver_policy`
function is used to make a DNS query, parse the arguments, and
return a member from the :class:`ReceiverPolicy`
enumeration.

.. autofunction:: gs.dmarc.lookup.lookup_receiver_policy
