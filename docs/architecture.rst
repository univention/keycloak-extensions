.. _app-architecture:

************
Architecture
************

The *Keycloak Extension App* architecture consists of the following elements:

* The operating environment |UCS| with the App Center and the Docker engine
  running the *Proxy* and *Handler* container.

* The *Keycloak Identity Access Management*, which is either running as part 
  of |UCS| via the *Keycloak App* or externally.

* The *Handler*-container retrieving events from the Keycloak event-api,
  checking conditions and running actions based on this information.

* The *Rule*-configuration configuring conditions and actions.

* The *Proxy* which enforces actions that can't be enforced by *Keycloak*
  itself and blocks suspicious requests or marks them with a HTTP-header.

* A reverse proxy terminating HTTPS-connection and setting
  a *X-FORWARDED-FOR* header to retain the original source IP-address.

.. _app-design-decisions:

Design decisions
================

Keycloak enables some brute force protection internally. This App is intended
to provide fine-granular decision making based on information available in
and outside of Keycloak itself.

Overview
========

.. _figure-bfa-overview:

.. figure:: /images/bfa-docs-version.*
   :alt: Keycloak extension overview.

   Interactions architectural components in and around this app.
   Containers of the app are marked pink.

.. raw:: latex

    \clearpage

Terms
=====

The document uses the terms that may not be clear to the reader. The following
list provides context and explanation.

.. glossary::

   SPI
      *Service Provider Interfaces* allow custom code that integrates with :program:`Keycloak`
      to allow the extension of the default behavior.

