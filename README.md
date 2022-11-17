# KeyCloak Brute-Force Protection Add-On

## Introduction

This is the repository for the KeyCloak Brute-Force Protection add-on.

## Releases and Packages

To release a package into the GitLab package registry,
the only thing necessary is pushing a semantic version tag (e.g. `v0.1.2`).
The branch detection regex looks like this:

```regexp
/^v[0-9]+\.[0-9]+\.[0-9]+/
```

If you want to have the internal Maven project
under `./reCaptcha-auth-flow` versioned with the same version number,
you can update the Maven project and then tag your commit using the pattern above.

Updating the version of a Maven project is done using the following command:

```shell
mvn versions:set -DnewVersion=0.3.0
```