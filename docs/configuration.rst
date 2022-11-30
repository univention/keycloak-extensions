.. _app-configuration:

*************
Configuration
*************

To change settings after installation, sign in to the UCS management system with
a username with administration rights and go to :menuselection:`App Center -->
UCS Keycloak Extensions --> Manage Installation --> App Settings`. On the appearing
*Configure UCS Keycloak Extensions* page, you can change the settings and apply them to
the app by clicking :guilabel:`Apply Changes`.

The App Center then *re-initializes* the Docker container for the app
*Keycloak Extensions*. *Reinitialize* means the App Center throws away the
running *Keycloak Extensions* Docker container and creates a fresh *Keycloak Extensions*
Docker container with the just changed settings.

.. _basic:

Configuration to use the proxy container
========================================

.. warning::

   This app doesn't (yet) configure public facing proxies. To use the functionality
   of this app, in the case of UCS, the Apache needs to be configured to forward requests
   to the proxy container, instead of Keycloak directly. 

When using the Keycloak App with Apache2, this means adding:

.. tab:: Apache ProxyPass

   .. code-block::
      
      ProxyPass /login-actions/ http://127.0.0.1:5000

into the Keycloak vServer.

For HA-Proxy, assuming a backend *Keycloak* already exists, add:

.. tab:: HA-Proxy ACL

   .. code-block::
      
      backend keycloak-proxy:
          mode http
          http-request add-header X-Forwarded-For
          
   
      acl keycloak-subdomain.domain.tld hdr(host) -i keycloak_sub_domain
      use_backend keycloak-proxy if keycloak_sub_domain && { path_beg /login-actions/ }

.. _app-secrets:

Secrets
=======

The app *Keycloak Extensions* requires an API secret, which is automatically
generated. This secret is stored in:

:file:`/etc/keycloak-extension-api.secret`
    The shared secret used by the handler-container to authenticate with the proxy-container-api.

.. _app-settings:

Settings
========

The following references show the available settings within the app
*Keycloak Extensions*. Univention recommends to keep the default values.

.. envvar:: keycloak-bfa/handler/keycloak/admin-auth-url

     Defines the *Keycloak* admin authentication URL. This URL is
     required for retrieving global events from the Keycloak API.

     .. list-table::                                                                                 
         :header-rows: 1
         :widths: 2 5 5

         * - Required
           - Default value
           - Set

         * - Yes
           - 
           - Only before installation

.. envvar:: keycloak-bfa/handler/keycloak/admin-user

    Defines a *Keycloak* admin user. A privileged user is
    required for retrieving global events from the Keycloak API.

    .. list-table::
        :header-rows: 1
        :widths: 2 5 5

        * - Required
          - Default value
          - Set

        * - Yes
          -
          - Only before installation

.. envvar:: keycloak-bfa/handler/keycloak/admin-password

    Defines the password for the configured admin user.

    .. list-table::
        :header-rows: 1
        :widths: 2 5 5

        * - Required
          - Default value
          - Set

        * - Yes
          -
          - Only before installation

.. envvar:: keycloak-bfa/notifications/mail-server

   Defines the mail server (SMTP) to use for sending out notifications mails.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - Yes
         -
         - Only before installation

.. envvar:: keycloak-bfa/notifications/mail-user

   Defines the user, or *FROM* to use when sending out notification mails.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - Yes
         - ``keycloak``
         - Only before installation

.. envvar:: keycloak-bfa/notifications/mail-password

   Defines the password to authenticate with the configured user on the
   target mail server. Leave empty if no authentication is required.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - No
         -
         - Only before installation

.. envvar:: keycloak-bfa/handler/debug-target-proxy-overwrite

   Overwrite the default target proxy (the proxy container in this app)
   and target an external address instead. This setting is only intended
   for debugging outgoing handler HTTP-requests.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - No
         -
         - Only before installation

.. envvar:: keycloak-bfa/handler/udm-rest-base-url

   Defines the UDM REST URL to send request to. This is needed for
   disabling users and retrieving user mails. Not setting this
   will cause any *Actions* requiring a UDM connection to fail.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - No
         -
         - Only before installation

.. envvar:: keycloak-bfa/handler/udm-rest-user

   Defines the UDM REST user.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - No
         -
         - Only before installation

.. envvar:: keycloak-bfa/handler/udm-rest-password

   Defines the password for the UDM REST user.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - No
         -
         - Only before installation

.. envvar:: keycloak-bfa/proxy/keycloak-server

   Defines the target Keycloak server to forward requests to.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - Yes
         - ``https://id.@%@domainname@%@``
         - Only before installation

.. envvar:: keycloak-bfa/proxy/keycloak-protocol

   Defines the protocol to use when forwarding requests. On a
   standard setup this will be *http*. Setting this variable 
   is only required if you run with an external Keycloak.

   Possible values: ``http``, ``https``.

   .. list-table::
       :header-rows: 1
       :widths: 2 5 5

       * - Required
         - Default value
         - Set

       * - No
         - ``http``
         - Only before installation


.. _app-rule-configuration:

Rule Configuration
==================

By default the following rules are configured (fails per hour):

.. note::

   Keycloak's internal so called "code_id", which it uses to identify devices
   is based on the "AUTH_SESSION_ID" cookie.

* **CAPTCHA** for **fingerprint** after 5 failed logins
* **CAPTCHA** for **AUTH_SESSION_ID** after 5 failed logins
* Block **fingerprint** after 10 failed login attempts per user
* Block **AUTH_SESSION_ID** after 10 failed login attempts per user
* Block **fingerprint** after 15 failed login attempts (regardless of user)
* Block **AUTH_SESSION_ID** after 15 failed login attempts (regardless of user)
* Block **IP** after 20 failed attempts per user

CAPTCHAs are done by the included Keycloak |SPI|, based on *X-SUSPICIOUS-REQUEST*
headers set in the proxy.

.. tab:: Rule configuration

   Rules are configured via the rules.json file.
   All values are case-insensitive.

   .. code-block::
    
      { 
          "condition" : "fingerprint",
          "condition-value" : "value-of-fingerprint",
          "user"      : "username", # or empty
          "limit"     : "10",
          "action"    : "add_header",
          "expiry"    : "1h"
      }

   Possible **conditions** are:

    * IP
    * fingerprint
    * AUTH_SESSION_ID
    * device

   The special **condition** *"device"* is a composite condition. It first tries
   to use fingerprinting to identify a device, with *AUTH_SESSION_ID* as an
   automatic fallback.

   Possible **actions** are:
    
    * add_header (add a *X-SUSPICIOUS-REQUEST* header)
    * block_ip (block an IP)
    * udm_lock (lock user in UCS via UDM)

.. warning::

   Be careful when setting IP restrictions, especially setting when setting limits
   below the limits of device restrictions like *fingerprint* or *code_id*, because
   legitimate users may often share the same IP, if they work from withing a
   cooperate network or VPN.

.. warning::

   UDM can only lock LDAP users. User authenticated via Keycloak from other sources
   (for example Keycloak internal users), can't be affected by this.
