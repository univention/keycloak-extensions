.. _app-installation:

************
Installation
************

.. highlight:: console

You can install the app *Keycloak Extensions* like any other app with Univention App Center.

UCS offers two different ways for app installation:

* With the web browser in the UCS management system

* With the command-line

For general information about Univention App Center and how to use it for
software installation, see :ref:`uv-manual:software-appcenter` in
:cite:t:`ucs-manual`.

.. _app-prerequisites:

Prerequisites
=============

Installing this app has various prerequisites:

#. *Keycloak Extensions* requires a configured *Keycloak* (>=18.0).

TODO: any other prerequisites above and additional detailed steps below this TODO

.. _installation-browser:

Installation with the web browser
=================================

To install *Keycloak Extensions* from the UCS management system, use the following steps:

#. Use a web browser and sign in to the UCS management system.

#. Open the *App Center*.

#. Select or search for *Keycloak Extensions* and open the app with a click.

#. To install *Keycloak Extensions*, click :guilabel:`Install`.

#. Leave the *App settings* in their defaults or adjust them to your
   preferences. For a reference, see :ref:`app-settings`.

#. To start the installation, click :guilabel:`Start Installation`.

.. note::

   To install apps, the user account you choose for login to the UCS management
   system must have domain administration rights, for example the username
   ``Administrator``. User accounts with domain administration rights belong to
   the user group ``Domain Admins``.

   For more information, see :ref:`uv-manual:delegated-administration` in
   :cite:t:`ucs-manual`.

.. _installation-command-line:

Installation with command-line
==============================

To install the app *Keycloak Extensions* from the command-line, use the following steps:

#. Sign in to a terminal or remote shell with a username with administration
   rights, for example ``root``.

#. Choose between default and custom settings and run the appropriate
   installation command.

   .. tab:: Default settings

      For installation with default settings, run:

      .. code-block::

         $ univention-app install keycloak-extensions

   .. tab:: Custom settings

      To pass customized settings to the app during installation, run the
      following command:

      .. code-block::

         $ univention-app install --set $SETTING_KEY=$SETTING_VALUE keycloak-extensions