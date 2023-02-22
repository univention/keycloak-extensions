# Developing Keycloak Extensions

There are two ways of running Keycloak:

1. Standalone
2. Embedded

*Standalone* means, that the built package is run, normally via `bin/kc.sh` or similar.
*Embedded*, means to add a package dependency to a Java project and bootstrapping the server class.

## Debugging

Both approaches have their way of being debugged and both can be used with this project.

> Please note, that - for convenience - the sample extension is a clone of a java implementation of the reCaptcha extension (deprecated). Hence, if you want to familiarize yourself with this development environment, you'll find traces of that at various locations.

### Standalone

#### Build the extension docker container

```sh
docker compose build keycloak-dev [--build-arg KEYCLOAK_VERSION=a.b.c]
```

Optionally you can set the `KEYCLOAK_VERSION` that you want to test against. This will affect the Maven libraries being used for the extension and also the keycloak server being started.

#### Run the docker container with remote debugging enabled

```sh
docker compose up keycloak-dev
```

#### Start remote debugging in IDE

Depending on your IDE of choice, create a remote debugging connection, having the sources for the extension available.
The debug client config should point to `0.0.0.0:8787`.
Now you can set a breakpoint and attach to the debug server.
It can happen, that the debug connection is detached automatically once after the start.
You can then attach again and should be able to hit breakpoints inside the extension code.

### Embedded

#### Preface

This setup is inspired by the Keycloak Extension Playground project here: https://github.com/thomasdarimont/keycloak-extension-playground

Since this project contains many example extensions, that are not needed in this context, the dev setup for the sample extension is a structural clone of the playground project, stripped down to the bare minimum, to be able to run an `org.keycloak.testsuite.KeycloakServer`. Have a look at [EmbeddedServer.java](keycloak/embedded-server/src/main/java/de/univention/keycloak/server/EmbeddedServer.java).

#### Preparation

Please make sure to have enough disk space available before attempting to build Keycloak. The built packages and maven dependencies will require multiple GB of local storage, depending on the build configuration.

> Note, that you can specify the location of the local maven repository (default `~/.m2/repository`) in `~/.m2/settings.xml`, in case you are short of storage space in your home drive.

##### Build Keycloak

This is necessary to build the Keycloak server packages and install them into the local maven repository to make them available to the debug project.

```sh
git clone https://github.com/keycloak/keycloak.git
cd keycloak
git fetch origin --tags
git checkout <keycloak.version>
mvn -Dmaven.test.skip clean install
```
`<keycloak.version>` in this [pom.xml](keycloak/pom.xml)

For further info, see https://github.com/keycloak/keycloak/blob/main/docs/building.md

#### Build the Test and Debug Environment

First, be sure to set the environment variable `DEV_KEYCLOAK_VERSION=19.0.3` or another suitable value, since this is used in the maven pom files!

> This is also necessary, when working with the project inside your IDE.

```sh
cd keycloak
mvn clean install
```

#### Running and Debugging in IDEs


##### Eclipse

1. inside `keycloak`, do `mvn eclipse:eclipse` to create the eclipse project files
2. Open eclipse and navigate:
    - File 
    - Import ...
    - select 'Existing Maven Projects'
    - provide Root Directory (`keycloak`)
    - select all projects that appear now
    - Finish
3. Create a *Debug Configuration*:
    - In the *Main* tab (open by default):
        - Give it a meaningful name, like 'Keycloak Test Server'
        - select the *Project*: `embedded-server`
        - select the *Main class*: `de.univention.keycloak.server.EmbeddedServer`
    - In the *Arguments* tab:
        - Enter following *VM arguments*:
            ```
            -Dkeycloak.bind.address=0.0.0.0
            -Djava.net.preferIPv4Stack=true
            -Dkeycloak.connectionsJpa.url=jdbc:h2:file:./data/keycloak_17_0_0_0000_master;DB_CLOSE_ON_EXIT=FALSE
            -Dkeycloak.connectionsJpa.driver=org.h2.Driver
            -Dkeycloak.connectionsJpa.driverDialect=org.hibernate.dialect.H2Dialect
            -Dkeycloak.connectionsJpa.user=sa
            -Dkeycloak.connectionsJpa.password=
            -Dkeycloak.connectionsJpa.showSql=false
            -Dkeycloak.connectionsJpa.formatSql=true
            -Dprofile=COMMUNITY
            -Dproduct.default-profile=COMMUNITY
            -Dkeycloak.password.blacklists.path=./data/blacklists/
            -Dcom.sun.net.ssl.checkRevocation=false
            -Dkeycloak.truststore.disabled=true
            -Dkeycloak.profile=COMMUNITY
            -Dkeycloak.product.name=keycloak
            -Dproduct.name=keycloak
            -Dkeycloak.profile=preview
            -Dkeycloak.hostname.frontendUrl=http://localhost:8081/auth
            -Dkeycloak.profile.feature.account2=enabled
            -Dkeycloak.profile.feature.account_api=enabled
            -Dkeycloak.profile.feature.scripts=enabled
            -Dkeycloak.profile.feature.device_activity=enabled
            -Dkeycloak.profile.feature.tokenexchange=enabled
            -Dkeycloak.profile.feature.ciba=enabled
            -Dkeycloak.profile.feature.client_policies=enabled
            -Dkeycloak.profile.feature.map_storage=disabled
            -Dkeycloak.ciba-auth-channel.ciba-http-auth-channel.httpAuthenticationChannelUri=http://localhost:7777/ciba/auth
            -Dkeycloak.theme.welcomeTheme=keycloak
            -Dkeycloak.theme.dir=/src/main/resources/themes
            ```
            This is taken from the keycloak-extension-playground project and has only the `keycloak.theme.dir` updated. For simplicity, it is using the H2 database.
            > To be clarified in the future: Possibly all the parameters except the theme directory can be omitted.
    - Apply
3. Run or Debug

##### VS Code

> This is currently incomplete, as the Theme config and setting the VM parameters needs to be tested first, still it is possible to start the server and get breakpoints in the extension like follows.

1. In the *file explorer*:
    - right-click on `keycloak/keycloak-testinstance-server/src/main/java/de/univention/keycloak/server/KeycloakTestServer.java`
    - Select *Run Java* or *Debug Java*
