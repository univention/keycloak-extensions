# POC Helm Chart for Keycloak with BFA protection

Allows to install Keycloak with brute force protection into a kubernetes cluster.

## Prerequisites

- The images are available

## SetUp

There is currently no access to the public registry, thus the images need to be pushed manually if not present
see also the [](push_images.sh)

As of now the images are present. There is only one registry, therefore images are differentiated by tags

### run locally

- Assure you have KIND (kubernetes in docker) installed
- adjust the `values.yml` so that it contains username and password for the registry
  for POC you can e.g. create a gitlab user token that can access the registry.
- Connect to the intranet (otherwise the images cannot be pulled)
- ./run_local.sh
- create a port-forward for the proxy pod
- When up, follow the instructions here:

https://git.knut.univention.de/univention/customers/dataport/upx/pocs/keycloak-bfa-and-security-poc



# Caveats

**THIS IS JUST A POC, DO NOT USE IN PRODUCTION**

## Considerations on the aproach

The overall aproach seems inappropriate:

- standards are being violated (produces invalid HTML - might break inexplicably)
- Very error prone (3 additional components to keycloak that need to be configured and up-to-date)
- Hard to maintain (see above)
- Hardly adds any security:
  - The browser fignerprinting can be easily bypassed
  - The protection by IP can be added with a lot less effort in cluster (LB / ingress rate limiting)
- Introduces potential vulnerabilities (3 additional components with potential security flaws;
  facilitates DOS attacks)
  
### Improvements Proposal

- Let the infrastructure handle BFP (Rate limiting / BFP by Loadbalancer / Ingress)
- Mandatory 2nd Factor effectively protects from guessing passwords.

## Missing implementations

Even if one would decide to use this aproacht (don't, see above), there is a lot missing:

- There is no way to lift the BFP for users (frontend required)
- The manual keycloak configuration steps should be automated within a realm
- A way to monitor multiple realms is missing
- meaningful log messages (errors very hard to detect)
- checker for required parameters / misconfiguration
- E2E tests / unit tests
- as of now the implementation has race conditions

