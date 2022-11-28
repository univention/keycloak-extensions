# KeyCloak Brute-Force Protection Add-On

## Introduction

This is the repository for the KeyCloak Brute-Force Protection add-on.

## Deployments

This project offers a pipeline for deploying to a Hetzner VM.

The first stage (`infrastructure`) in which the setup of the infrastructure takes place sets up a Hetzner VM.
This stage also creates an *AWS Route53* DNS record pointing to the server IP via a DNS A record. 

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
the only thing necessary is pushing a *semantic version number* tag (e.g. `v0.1.2`).
The branch detection regex looks like this:

```regexp
/^v[0-9]+\.[0-9]+\.[0-9]+/
```

For more information on semantic versioning, see: https://semver.org

### Updating the Maven project version

It makes sense to have the internal Maven project under `./reCaptcha-auth-flow`
versioned using the same version number from your tag.
To achieve this, you can update the version in the Maven project,
and then version-tag your commit.

Updating the version of a Maven project is done using the following command:

```shell
mvn versions:set -DnewVersion=0.3.0
```