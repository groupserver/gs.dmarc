Changelog
=========

2.1.8 (2016-10-18)
------------------

* Adding :pep:`484` type hints
* Updating the public-suffix list
* Using :mod:`setuptools` to return the public-suffix list

2.1.7 (2016-04-11)
------------------

* Testing with Python 3.5
* Switching to dictionary-comprehensions

2.1.6 (2016-03-24)
------------------

* Updating the suffix list from Mozilla, thanks to `Baran
  Kaynak`_

.. _Baran Kaynak: https://github.com/barankaynak

2.1.5 (2015-09-01)
------------------

* Catching ``dns.resolver.NoNameserver`` exceptions, thanks to
  `Alexy Mikhailichenko`_

.. _Alexy Mikhailichenko: https://github.com/alexymik

2.1.4 (2015-06-25)
------------------

* Fixing a spelling mistake in the README, thanks to `Stefano
  Brentegani`_
* Updating the documentation, as DMARC is now :rfc:`7489`

.. _Stefano Brentegani: https://github.com/brente

2.1.3 (2014-10-20)
------------------

* Handling domains with invalid DMARC policies, closing `Bug 4135`_

.. _Bug 4135: <https://redmine.iopen.net/issues/4135

2.1.2 (2014-09-26)
------------------

* Switching to GitHub_ as the primary code repository.

.. _GitHub: https://github.com/groupserver/gs.dmarc

2.1.1 (2014-07-09)
------------------

* Coping when the host-name passed to ``lookup_receiver_policy``
  for hosts that start with ``_dmarc`` already
* Rejecting all answers that do not start with ``v=DMARC1``, as
  per `Section 7.1`_ (number 5) of the draft DMARC specification

.. _Section 7.1:
   http://tools.ietf.org/html/draft-kucherawy-dmarc-base-04#section-7.1

2.1.0 (2014-05-07)
------------------

* Adding ``gs.dmarc.receiver_policy``, which looks up the
  organisational domain
* Updating the Sphinx documentation

2.0.0 (2014-04-29)
------------------

* Adding ``gs.dmarc.ReceiverPolicy.noDmarc``, and returning it
  from ``gs.dmarc.lookup_receiver_policy``
* Adding Sphinx documentation

1.0.0 (2014-04-24)
------------------

Initial release.

..  LocalWords:  Changelog GitHub README
