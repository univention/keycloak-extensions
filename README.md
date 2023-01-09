## Configure Keycloak

### Events

We need user events to be enabled. In order to do so:

#### Keycloak > 18

1. Access `http://localhost:5050/admin`.
2. Click `Administration Console`.
3. Access with user `admin` and password `univention`.
4. Click `Realm settings` on the left menu.
5. Go to `Events` tab.
6. Under `User events settings` set `Save events` to `ON`.
7. You can set an expiration time for events, but it is not needed for local testing.
8. For now we only need `LOGIN_ERROR` and `LOGIN`, but no need to disable the other 111 event types.

#### Keycloak <= 18 (current local setup)

1. Access `http://localhost:5050/admin`.
2. Click `Administration Console`.
3. Access with user `admin` and password `univention`.
4. Click `Events` on the left menu, towards the bottom.
5. Go into `Config` tab.
6. Under `Login Events Settings`, set `Save Events` to `ON`.
7. Save
8. (Not needed) You can set an expiration time for events, but it is not needed for local testing.
9. (Not needed) For now we only need `LOGIN_ERROR` and `LOGIN`, but no need to disable the other 111 event types.

> Any changes to `docker-compose.yaml` will affect this steps.

### Configure reCaptcha extension (optional)

#### Theme

1. Go into `Realm settings > Themes`.
2. Choose `captcha` as `Login theme`.

> If the theme is not there, make sure you build the custom keycloak:
> `docker compose up -d keycloak --build`

#### Auth Flow

1. Go to `Authentication` on the left menu.
2. Select the `Browser` flow from the dropdown.
3. On the top right, do `Copy`.
4. Name: `Captcha` (can be changed).
5. Access the new created flow from the dropdown.
6. Under `Captcha forms` (or the name you gave it on step 4), go to `Actions > Add execution`
7. Select `Username Password Form With reCaptcha`.
8. Move it just below `Captcha forms` as a substep.
9. Set it as `Required` and remove the original step `Username Password Form`
10. Configure the new step:
    1. Click on `Actions > Config` for the new step.
    2. Set an alias, `myCaptcha` will do.
    3. (Optional, or copy my values from following steps) Go to `https://www.google.com/recaptcha/admin` and get the site key and secret key.
    4. Set site key to `6LcUyZkiAAAAAHo98CowhZFoc-E-3yeo38Hs1HSB`
    5. Set secret key to `6LcUyZkiAAAAAOM0G7kctpprpOtM6DWKagf8Ew88`
11. Go back to `Authentication` menu on the left and go to `Bindings`.
12. Set the `Browser Flow` to `Captcha` (or your name on step 4).
13. Save.
14. Go to `Realm settings > Security Defenses` and set:
    1. `X-Frame-Options` to `ALLOW-FROM https://www.google.com`
    2. `Content-Security-Policy` to `frame-src 'self' https://www.google.com; frame-ancestors 'self'; object-src 'none';`
    3. Save.

## Local setup

`docker compose up -d keycloak database`  
`docker compose up -d proxy handler`

You can access:

- Keycloak at `http://localhost:5050` (only for configuration).
- Proxied Keycloak at `http://localhost:8181` (protected by proxy).
- Handler will be polling Keycloak directly (without the proxy).

## Architecture

![Architecture](images/architecture.png)

### Proxy

- [x] Fingerprint requests to track devices.
- [x] Block requests based on IP (read from database).
- [ ] Block requests based on device (read from database). TODO: better device tracking.
- [x] Add header `X-SUSPICIOUS-REQUEST` to enable captcha on Keycloak if configured.

### Handler

- [x] Polls events from Keycloak every second.
- [x] Check Keycloak events against rules.
- [x] Saves the decided actions on the database, which the proxy will use.
- [x] Sets expiration time of actions to 5 minutes (configurable) automatically.
- [x] Deletes expired actions from the database.
- [ ] TODO: Notifies the administrator if failed login attempts rate is exceeded.
- [ ] TODO: New Device Login.

### Keycloak

- [x] Show reCaptcha if configured on `X-SUSPICIOUS-REQUEST`.
- [ ] TODO: currently reCaptcha fails with KC > 18 because of a new JSON mapping...

## Future lines of work

1. Keycloak event monitoring on Grafana (sucessful logins, failed login attempts...)
2. UDM integration
3. Whitelists
4. Blacklists
