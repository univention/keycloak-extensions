# Changelog

## [0.15.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.14.0...v0.15.0) (2024-12-20)


### Features

* upgrade UCS base image to 2024-12-12 ([70f944e](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/70f944e6da482032fa8c2a434996edd184c9bea9))

## [0.14.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.13.1...v0.14.0) (2024-12-02)


### Features

* added ssl support to the database connection on the proxy ([62b4759](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/62b475986dd3eace0f3781e0b5ee29e3b620d1b6))

## [0.13.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.13.0...v0.13.1) (2024-11-27)


### Bug Fixes

* add if to ports ([977e274](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/977e27401c3923b06af113eea11689394d1dcd5a))
* disable probes by default ([804b5f4](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/804b5f492ff555b6edbdbf450971f9067e1321c2))
* Kyverno lint ([34e1a8b](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/34e1a8be48e51b94d069c1a86fdf954d46973a53))
* missing quote ([9b0972f](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/9b0972f092894b63e3eebce9c8b4c5e02dfa9fa8))

## [0.13.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.12.0...v0.13.0) (2024-11-20)


### Features

* migrate component secret ([6e7d230](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/6e7d23014418f34cbae7e466bcd68d087afcea4e))

## [0.12.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.11.0...v0.12.0) (2024-09-26)


### Features

* **ci:** enable malware scanning, disable sbom generation ([eb929cc](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/eb929cc1f1bdbf6e9f2f1f4aa7dcb7c781575e1c))
* **ci:** enable malware scanning, disable sbom generation ([2b763d4](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/2b763d46dc7f508d143b3a99a36166b46e749844))

## [0.11.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.10.0...v0.11.0) (2024-09-13)


### Features

* update UCS base image to 2024-09-09 ([ba59679](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/ba596790f7d1ea8f44c073ffd0e7d8cc9fc0560c))

## [0.10.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.9.4...v0.10.0) (2024-08-21)


### Features

* **keycloak-extensions:** Add certManager template for ingress ([21b69ae](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/21b69ae0da5a863dbac230bb13bc7e6c1e466981))


### Bug Fixes

* **keycloak-extensions:** Use proxy tls secretName when provided ([2ebe1f8](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/2ebe1f88ea6c3f29117225f67c95b07d98b62b79))

## [0.9.4](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.9.3...v0.9.4) (2024-08-05)


### Bug Fixes

* **proxy:** handle calls with no cookie ([adae1e8](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/adae1e865f1d7dff103caf102ac84f0be1a91f59))

## [0.9.3](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.9.2...v0.9.3) (2024-08-04)


### Bug Fixes

* **proxy:** use legacy identifier first ([95f5759](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/95f5759d0762e075dc8b2ca585ab46621e8f26d6))

## [0.9.2](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.9.1...v0.9.2) (2024-08-04)


### Bug Fixes

* **proxy:** use legacy identifier first ([e5e6f78](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/e5e6f7885f91dfe9382ea4d53e8d2eea5121b22b))

## [0.9.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.9.0...v0.9.1) (2024-07-31)


### Bug Fixes

* **handler:** Retry on get user email failed authentication ([e37ee92](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/e37ee920c14b88f58fc0322e13ae22ce16bf5861))

## [0.9.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.8.0...v0.9.0) (2024-07-31)


### Features

* update python-keycloak ([e088f1e](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/e088f1edd536b1041a80f5b2755ae9667f55f1dd))

## [0.8.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.7.0...v0.8.0) (2024-07-12)


### Features

* **smtp:** Add support for SSL/TLS more and no-auth environments ([78b736c](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/78b736c59fb616ed0f81f032188498ee517e5a9b))

## [0.7.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.6.1...v0.7.0) (2024-07-04)


### Features

* support global postgres ([6455891](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/6455891ce9d9e2ab736ccb903dba3a52fbf3ed48))

## [0.6.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.6.0...v0.6.1) (2024-06-24)


### Bug Fixes

* avoid failure if a user has no email ([69cc802](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/69cc802aa350981d40830f1c46c10f90cdecd8a1))
* default to 1 minute for event retention and expiry ([ce918ab](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/ce918ab7151b63f33af5cef1ad22d0ca833522c4))
* wrong env variable name EVENTS_RETENTION_MINUTES and allow disabling email notifications ([60eb62b](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/60eb62bb0d606c9ef2a13cfce1652c999cff9bec))

## [0.6.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.5.1...v0.6.0) (2024-05-28)


### Features

* Allow to customize all ingress annotations ([1eb011b](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/1eb011bf7fb63d2a6e34edeedb29bc51063f8458))

## [0.5.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.5.0...v0.5.1) (2024-05-23)


### Bug Fixes

* use global registry ([7bdc9a8](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/7bdc9a84853b6e668ea5151e9237faddc08412c6))

## [0.5.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.4.1...v0.5.0) (2024-05-23)


### Features

* push to harbor ([bcf633b](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/bcf633b58daaa8fe649a09a3bc29870735b7b281))

## [0.4.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.4.0...v0.4.1) (2024-05-15)


### Bug Fixes

* Update base image to version 0.12.0 ([2ae3cd6](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/2ae3cd6c250403208a8f1b4d5ae62346db92622f))

## [0.4.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.3.3...v0.4.0) (2024-05-14)


### Features

* changes to support the refactored umbrella values in a nubus deployment ([3943129](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/39431291d58c4e9fd25d7fc4f69ad4ac57301112))


### Bug Fixes

* allow for empty values in smtp configuration ([759416b](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/759416bab541cf92d8bd5938a5bd2c88c8bc369b))
* change default nubus database for keycloak-extensions to keycloak_extensions ([25e9093](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/25e90933839fde69e2a9837cde2f5fe8cb33966c))

## [0.3.3](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.3.2...v0.3.3) (2024-04-25)


### Bug Fixes

* add support for additional Kubernetes parameters ([ef89dfa](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/ef89dfa62236db2da944c6fbea1c5291d6ca755b))
* handler and proxy default enabled, fix service account names ([dfdfdf9](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/dfdfdf9992d88ebf742029d4abf1a2956ccf3dd7))
* handler and proxy default enabled, fix service account names ([af4b83c](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/af4b83ccf2d0b8313dd97311250b100312e5a638))

## [0.3.2](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.3.1...v0.3.2) (2024-04-05)


### Bug Fixes

* refactor labels in ingress, configmap, service, and deployment templates for umbrella compatibility ([4bfd588](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/4bfd58883bb3a26536bc050dcade7a766e07b788))

## [0.3.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.3.0...v0.3.1) (2024-04-04)


### Bug Fixes

* **helm:** change default gitregistry for proxy so packaged charts contain proper digests ([85f1e80](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/85f1e806c1c6d0d45c339d7a145c6a66689feecb))

## [0.3.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.2.2...v0.3.0) (2024-04-04)


### Features

* **helm:** major refactoring ([d540031](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/d5400318ac5155aee662d887c2460842422bd2b9))

## [0.2.2](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.2.1...v0.2.2) (2024-04-02)


### Bug Fixes

* **ci:** update common-ci from v1.16.2 to v1.25.0 ([11b209e](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/11b209e45ba426a4ff6a026121202d60df621b78))
* **helm/values:** add missing image parameters ([54c0006](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/54c0006ff2bd9abd6903a914222199817d3b0431))

## [0.2.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.2.0...v0.2.1) (2024-02-27)


### Bug Fixes

* **helmchart:** Enhance ingress templating support (e.g. to allow adding an alternative backend for /[secure] on ingress level) ([4c33c87](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/4c33c8774a2f3b599dd7aa3034d42f9f265b5f1a))

## [0.2.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.1.0...v0.2.0) (2024-01-23)


### Features

* Tiltfile for easier development ([62131b2](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/62131b2407592b4b8d589015fff0ba5f36d799b7))


### Bug Fixes

* **proxy:** 2fa new device login notification ([e159bfd](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/e159bfdf136746fd3bc22acac745c2a9ad1359b7))

## [0.1.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.0.5...v0.1.0) (2024-01-18)


### Features

* **ci:** add debian update check jobs for scheduled pipeline ([98c35c8](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/98c35c8df1e90631c1a461ad86207738bf9386c0))


### Bug Fixes

* **deps:** add renovate.json ([aefa8cd](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/aefa8cd5e6180aaaf4c803a4e490a426efa15ea8))
* **helm:** Add imagePullSecrets to helm charts ([e729c35](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/e729c3515d50495eabc2cea26f8eb303fa68dc51))
* **pre-commit:** remove legacy license hooks ([69f3d0e](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/69f3d0e70275cfd620a07b373ca1a9d72929f732))

## [0.0.5](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.0.4...v0.0.5) (2023-12-28)


### Bug Fixes

* **licensing/ci:** add spdx license headers, add license header checking pre-commit ([e169716](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/e16971686dd6b87abf37756f3377f51c44c718de))

## [0.0.4](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.0.3...v0.0.4) (2023-12-20)


### Bug Fixes

* **docker:** update ucs-base 5.2-0 from v0.7.2 ro v0.10.0 ([e59aed1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/e59aed126727f7845405b0825ae15e01d070c021))

## [0.0.3](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.0.2...v0.0.3) (2023-12-18)


### Bug Fixes

* **ci:** add Helm chart signing and publishing to souvap via OCI, common-ci 1.12.x ([1a5d4ce](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/1a5d4cefb762fd39dd095af7b26396a6c4900ea0))

## [0.0.2](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.0.1...v0.0.2) (2023-12-12)


### Bug Fixes

* **ci:** reference common-ci v1.11.x to push sbom and signature to souvap ([3d470e4](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/3d470e454dd0899ef5f04d9ca9517c30763b228c))
