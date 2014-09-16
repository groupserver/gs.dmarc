Changelog
=========

2.1.1 (2014-07-09)
------------------

* Cope when the host-name passed to ``lookup_receiver_policy``
  for hosts that start with ``_dmarc`` already.
* Reject all answers that do not start with ``v=DMARC1``, as per
  `Section 7.1`_ (number 5) of the DMARC specification.

.. _Section 7.1: http://tools.ietf.org/html/draft-kucherawy-dmarc-base-04#section-7.1

2.1.0 (2014-05-07)
------------------

* Added ``gs.dmarc.receiver_policy``, which looks up the
  organisational domain.
* Updated the Sphinx documentation.

2.0.0 (2014-04-29)
------------------

* Added ``gs.dmarc.ReceiverPolicy.noDmarc``, and returning it from 
  ``gs.dmarc.lookup_receiver_policy``. Bumped the version number
  because of this.
* Added Sphinx documentation

1.0.0 (2014-04-24)
------------------

* Initial release
