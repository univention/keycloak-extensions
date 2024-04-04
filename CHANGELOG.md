# Changelog

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
