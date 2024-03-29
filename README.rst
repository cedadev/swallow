swallow
=======

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: http://swallow.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://badges.gitter.im/bird-house/birdhouse.svg
    :target: https://gitter.im/bird-house/birdhouse?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
    :alt: Join the chat at https://gitter.im/bird-house/birdhouse


swallow (the bird)
  *The swallow is a shy species, and therefore difficult to observe and study. It spends most of the day on top of high branches, above all during breeding season.
  [..].* ( `Wikipedia <https://en.wikipedia.org/wiki/swallow>`_ ).

A Web Processing Service - For running the Met Office NAME model
----------------------------------------------------------------

swallow is a WPS to run the Met Office NAME model.

It was initially developed by Teri Forey at Leicester University ( `namewps <https://github.com/TeriForey/namewps>`_ ).
It is now maintained by CEDA ( `swallow <https://github.com/cedadev/swallow>`_ ).

* Free software: Apache Software License 2.0
* Documentation: https://swallow.readthedocs.io.

Testing
-------

To test the WPS, run:

```
python -m pytest -W ignore tests
```

Development and maintenance
---------------------------

To keep up-to-date with the birdhouse cookicutter, just run:

```
cruft update
```

It will pull in changes from the latest cookiecutter commit and merge them 
in (maybe seamlessly).

Credits
-------

This package was created with Cookiecutter_ and the `bird-house/cookiecutter-birdhouse`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`bird-house/cookiecutter-birdhouse`: https://github.com/bird-house/cookiecutter-birdhouse

STFC Licence
------------

`LICENCE <https://github.com/cedadev/swallow/blob/master/LICENSE>`_

