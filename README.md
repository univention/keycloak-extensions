# KeyCloak Brute-Force Protection Add-On

## Introduction

This is the repository for the KeyCloak Brute-Force Protection add-on.

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