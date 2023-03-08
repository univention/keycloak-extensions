# KeyCloak Brute-Force Protection Add-On

## Introduction

This is the repository for the KeyCloak Brute-Force Protection add-on.

## Deployments

This project offers a pipeline for deploying to a Hetzner VM.

The first stage (`infrastructure`) in which the setup of the infrastructure takes place sets up a Hetzner VM.
This stage also creates an _AWS Route53_ DNS record pointing to the server IP via a DNS A record.

The second stage (`provision`), runs an Ansible playbook which joins the newly created server to the designated domain.

### Triggered Automated Deployments

Automated deployments to the `staging` and `production` environments are
triggered by commits to `staging` and `main` branches respectively.

All other branches require a manual action for their deployments to work.

### Teardown of environments

To remove an environment from GitLab, we have a CI job available.
To trigger this job, and have Terraform remove both the Hetzner VM and the DNS record from Route53,
you can use the GitLab web UI: Within the project, navigate to:
**Deployments** > **Environments** and click the **Stop** button for the selected environment.

## Releases and Packages

To release a package into the GitLab package registry,
the only thing necessary is pushing a _semantic version number_ tag (e.g. `v0.1.2`).
The branch detection regex looks like this:

```regexp
/^v[0-9]+\.[0-9]+\.[0-9]+/
```

For more information on semantic versioning, see: https://semver.org

# Setup

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

#### Keycloak <= 18

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

### Configure reCaptcha

In order for reCaptcha to work, we need to tweak two things on Keycloak:

1. Go to `Realm settings > Security Defenses` and set:
2. `X-Frame-Options` to `ALLOW-FROM https://www.google.com`
3. `Content-Security-Policy` to `frame-src 'self' https://www.google.com; frame-ancestors 'self'; object-src 'none';`
4. Save.

Now you need to check that your proxy gets the environment variable `CAPTCHA_SITE_KEY`.
For localhost, I lend you this one: `6LcUyZkiAAAAAHo98CowhZFoc-E-3yeo38Hs1HSB`, but you
may want to grab one from [here](https://www.google.com/recaptcha/admin/).

Currently only Google reCaptcha is supported, but Cloudflare and others are easy to integrate.

## Local setup

`docker compose -f develop.docker-compose.yaml up -d keycloak database`  
`docker compose -f develop.docker-compose.yaml up -d proxy handler`

You can access:

- Keycloak at `http://localhost:5050` (only for configuration).
- Proxied Keycloak at `http://localhost:8181` (protected by proxy).
- Handler will be polling Keycloak directly (without the proxy).

# Architecture

![Architecture](images/architecture.png)

### Proxy

- [x] Fingerprint requests to track devices.
- [x] Block requests based on IP (read from database).
- [x] Block requests based on device (read from database).
- [x] Injects the reCaptcha into the login form if needed (read action from database).

### Handler

- [x] Polls events from Keycloak every second.
- [x] Check Keycloak events against rules.
- [x] Saves the decided actions on the database, which the proxy will use.
- [x] Sets expiration time of actions to 5 minutes (configurable) automatically.
- [x] Deletes expired actions from the database.
- [x] TODO: Notifies the administrator if failed login attempts rate is exceeded.
- [x] New Device Login.

## Future lines of work

1. Keycloak event monitoring on Grafana (sucessful logins, failed login attempts...)
2. UDM integration
3. Whitelists
4. Blacklists
