.. _app-limitations:

****************************
Requirements and limitations
****************************

To ensure a smooth operation of the app *Keycloak Extensions*
on |UCS|, administrators need to know the following requirements
and limitations.

.. _limitation-security-issues:

Considerations on rule structuring
==================================

When defining rules, always consider that a malicious actor may exploit
**any** anti brute force measures, to lock out legitimate users from the system.

Considerations
--------------

- A legitimate user will always be assigned the same fingerprint, but normal actions,
  such as clearing browser cache or certain add-ons may cause new *AUTH_SESSION_ID*'s.

- An illegitimate user/attacker may fake his fingerprint or *AUTH_SESSION_ID*, but 
  - unless he already has privileged access to your network - will not be able to fake his IP.

- A attacker with low privileged access to a user computer may retrieve existing IDs
  or fingerprints and spoof them.

- Multiple legitimate users may originate from the same IP (for example a cooperate network), but
  attackers are unlikely to originate from the same network as legitimate users.

Example scenario 1
------------------

.. admonition:: Description

   A user repeatedly fails his authentication, because he is trying to remember his password.
   As he is not trying to conceal his identity his IP and fingerprint will constant.

This *legitimate* user should be blocked or CAPTCHA-ed via his fingerprint, before action for his IP is taken, otherwise other user behind the same IP maybe unjustly impaired as well.

Example scenario 2
------------------

.. tab:: Description

   A user repeatably sends bad authentication requests without any fingerprint.

Fingerprinting may be be blocked by some browser extensions. While the fingerprint-ID
is the preferred identifier, a lack of fingerprint is not necessarily an indicator
of a bad actor, rules should fall back on *AUTH_SESSION_ID* first.

Example scenario 3
------------------

.. tab:: Description

   A user repeatably sends bad authentication requests without any fingerprint or device ID.

This scenario is not possible without deliberate effort by an attacker. Repeated, requests like this
should be blocked via the originating IP. If this IP has legitimate users, then the organization
to which the origin IP belongs to should be notified of a potential bad actor in their system.
