.. _app-troubleshooting:

***************
Troubleshooting
***************

.. highlight:: console

When you encounter problems with the operation of the app *Keycloak Extensions*, this section
provides information where you can look closer into and to get an impression
about what's going wrong.

.. _app-log-files:

Log files
=========

The app *Keycloak Extensions* produces different logging information in different places.

:file:`/var/log/univention/appcenter.log`
   Contains log information around activities in the App Center.

   The App Center writes *Keycloak Extensions* relevant information to this file, when you run
   app lifecycle tasks like install, update and uninstall or when you change the
   app settings.

:file:`/var/log/univention/join.log`
   Contains log information from join processes. When the App Center installs
   *Keycloak Extensions*, the app also joins the domain.

*Docker containers*
   The app uses two custom built Python images. The App Center runs the container.
   You can view log information from the *Keycloak Extensions* Docker container with the
   following command:

   .. code-block:: console

      $ univention-app logs keycloak-extensions

:file:`/var/log/apache2/*.log`
    Reverse proxy logs may contain relevant information for queried URLs by
    *Keycloak Extensions*, for example the status of login requests to :program:`Keycloak`.

