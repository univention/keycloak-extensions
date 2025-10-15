# Changelog

## [0.23.0](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.22.0...v0.23.0) (2025-10-15)


### Features

* adjust to common behavior / add tests for labels and image configuration ([b99a4bb](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/b99a4bbdfe86841dd61d23be7e449a0eadd39a67)), closes [[secure]/dev/internal/team-nubus#1398](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1398)
* generate captcha secret / add tests on secrets ([ebedbdc](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/ebedbdc71d8015c4fdcbfdabe7b3fd28a873e169)), closes [[secure]/dev/internal/team-nubus#1398](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1398)
* generate keycloak secret / add tests on secrets ([c7e8dc8](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/c7e8dc801021cfa48f5a4dc2ce24d71935baee2c)), closes [[secure]/dev/internal/team-nubus#1398](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1398)
* generate postgresql secret / add tests on secrets ([baf6a9e](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/baf6a9e7bdde69c9fa1af94ef1189a3ab47c69a3)), closes [[secure]/dev/internal/team-nubus#1398](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1398)
* generate smtp secret / add tests on secrets ([efea83b](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/efea83b5f0e4f261e27a85a767c39a3ef8e6c07f)), closes [[secure]/dev/internal/team-nubus#1398](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1398)
* replace additional component annotations with global ones and add chart test ([9de3fd8](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/9de3fd8a886935e46b16862b2e79f3e3e217974c)), closes [[secure]/dev/internal/team-nubus#1398](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1398)


### Bug Fixes

* correct typos in require messages ([5a5ec84](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/5a5ec84cb677fe6f872d17cad3c49c13c55b8904)), closes [[secure]/dev/internal/team-nubus#1398](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1398)

## [0.22.0](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.21.2...v0.22.0) (2025-09-29)


### Features

* template improvements for kyverno ([54a384c](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/54a384c8d9f26e998ff769746474451a8777be10)), closes [[secure]/dev/internal/team-nubus#1426](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1426)

## [0.21.2](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.21.1...v0.21.2) (2025-09-11)


### Bug Fixes

* **deps:** Update gitregistry.knut.[secure].de/[secure]/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20250909 ([143f9c8](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/143f9c8fee85dd6cbef6f6d50bb583118f8c61e1)), closes [#0](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/issues/0)

## [0.21.1](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.21.0...v0.21.1) (2025-08-27)


### Bug Fixes

* **deps:** Update gitregistry.knut.[secure].de/[secure]/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250821 ([6ec1bb1](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/6ec1bb1da7dbc059382670373fb10b3a1257fd55)), closes [#0](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/issues/0)

## [0.21.0](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.20.0...v0.21.0) (2025-08-26)


### Features

* upgrade bitnami charts ([cd6af7f](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/cd6af7fcf3915308c5f495aed06e6a696ae3010d)), closes [[secure]/dev/internal/team-nubus#1406](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1406)

## [0.20.0](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.19.2...v0.20.0) (2025-07-17)


### Features

* update ucs-base to 5.2.2-build.20250714 ([7d2506e](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/7d2506e59a58c67f29c8c0de28ea3498eef28adf)), closes [[secure]/dev/internal/team-nubus#1320](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1320)

## [0.19.2](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.19.1...v0.19.2) (2025-06-23)


### Bug Fixes

* use default cluster ingress class if not defined ([3d908e0](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/3d908e02f200fdc0c0b93dc128b4a0179176bc92)), closes [[secure]/dev/internal/team-nubus#1134](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1134)

## [0.19.1](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.19.0...v0.19.1) (2025-06-23)


### Bug Fixes

* bump umc-base-image version ([6fcc0aa](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/6fcc0aa5490d31697ea822d8a3a6198c5efa4891)), closes [[secure]/dev/internal/team-nubus#1263](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1263)

## [0.19.0](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/compare/v0.18.0...v0.19.0) (2025-06-20)


### Features

* email login notice contains configurable timezone ([451280e](https://git.knut.[secure].de/[secure]/dev/projects/keycloak/keycloak-extensions/commit/451280e3c827e75466de3777e787a7fb60021b5c)), closes [[secure]/dev/internal/team-nubus#1163](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1163)

## [0.18.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.17.0...v0.18.0) (2025-05-11)


### Features

* move and upgrade ucs-base-image to 0.17.3-build-2025-05-11 ([0635e3d](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/0635e3da9052ffdb989f7b29090c3473a5851b61))


### Bug Fixes

* add bitnami to package-helm-charts ([a11865f](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/a11865f056b462760c8216d4712be488585a3582))
* move addlicense pre-commit hook ([77d898e](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/77d898e867797e7a41e426068960d17b1782b9a9))
* update common-ci to main ([161b291](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/161b291c037eb0ab63e2028f4d237839f25a473a))

## [0.17.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.16.1...v0.17.0) (2025-04-29)


### Features

* Bump ucs-base-image version ([1b3d914](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/1b3d9148b2b4153f7e72874c0fbaa36a33afd3d9)), closes [[secure]/dev/internal/team-nubus#1155](https://git.knut.[secure].de/[secure]/dev/internal/team-nubus/issues/1155)

## [0.16.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.16.0...v0.16.1) (2025-02-27)


### Bug Fixes

* url encode postgresql user and password ([44baa76](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/44baa769bcca520a73da806a1506cdf5e986c5f6))

## [0.16.0](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.15.4...v0.16.0) (2025-02-26)


### Features

* Bump ucs-base-image to use released apt sources ([ad664b8](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/ad664b8dcf732b125030be3976c41bc534e45af4))

## [0.15.4](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.15.3...v0.15.4) (2025-02-10)


### Bug Fixes

* add .kyverno to helmignore ([7f96935](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/7f9693502cc9318e20c19c1eef1297cf2614e9d9))

## [0.15.3](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.15.2...v0.15.3) (2025-01-24)


### Bug Fixes

* **proxy:** Redis SSL activation variable gets passed as a string, which gets always treated as true ([a30b1bf](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/a30b1bf8857a11cae4813bf73e7e00ddea6bb03a))

## [0.15.2](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.15.1...v0.15.2) (2025-01-24)


### Bug Fixes

* **handler:** pin httpx version ([94e511d](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/94e511d4ad6689657feb5d43fad865262c5ea32e))

## [0.15.1](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/compare/v0.15.0...v0.15.1) (2025-01-22)


### Bug Fixes

* **proxy:** handle failed promise during token decoding ([56f0822](https://git.knut.[secure].de/[secure]/components/keycloak-extensions/commit/56f0822173ca5a19bd9828952cd72751cef8d351))

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
