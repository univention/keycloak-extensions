# End-to-end tests for the Brute Force Prevention

## Installation

```
pip install -r requirements_test.txt
playwright install  # installs required browsers
```

## How to run tests

Please make sure you have the proxy running.

Then just run the following command. 

```
pytest --base-url <proxy-base-url> --slowmo 500
```

Here `--slowmo` is required because the handler needs some time to block devices/IP, and this 
makes the automated tests run at a human-like pace.

We support the following custom command line options defined in `tests/conftest.py`

1. `username`: Username to use when logging into the Keycloak admin console. Defaults to `"admin"`
2. `password` Password to use when logging into the Keycloak admin console. Defaults to `"univention"`
3. `num-device-block`: Number of failed login attempts for device block. Defaults to `5`.
4. `num-ip-block`: Number of failed login attempts for IP block. Defaults to `7`. 
Must be higher than `num-device-block`
5. `release-duration`: Number of seconds after which blocks are released. Default is `60`.

Some other useful supported options:

1. `headed`: Use headed browsers with `--headed`.
2. `slowmo`: Will run things in slow motion e.g. `--slowmo 500`

### Running with `docker`

```
docker build -t e2e:latest .
docker run -it --network="host" e2e:latest pytest --base-url http://localhost:8181 --slowmo 500

```

## Available tests

| Test                                                                                                                    | Source                                |
|-------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| Many failed login with browser A; browser blocked                                                                       | `tests/test_block::test_device_block` |
| Browser A block is released after a minute                                                                              | `tests/test_block::test_device_block` |
| Browser A blocked, but browser B can login                                                                              | `tests/test_block::test_device_block` |
| Many failed logins with browser A and IP X; browser A blocked. more failed logins with browser B and IP X; IP X blocked | `tests/test_block::test_ip_block`     |
| IP X block is released after a minute                                                                                   | `tests/test_block::test_ip_block`     |
| IP X blocked, but IP Y can login                                                                                        | `tests/test_block::test_ip_block`     |

## For test engineers

We use the [page object pattern](https://martinfowler.com/bliki/PageObject.html)
to represent Keycloak admin pages. The page objects are in `src/pages`.

You can pip install the page objects as a package using

```
pip install -e .
```

While this is not strictly necessary to run the tests (`pytest` finds the necessary
packages using the `[tool.pytest.ini_options]` in `pyproject.toml`), this will
help the IDE in autocompletion etc., and generally improve the development
experience.
