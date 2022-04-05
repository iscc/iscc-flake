# ISCC - Flake Microservice

**A microservice for generating unique identifiers for distributed computing.**


The [ISCC Flake-Code](https://core.iscc.codes/units/code_flake/) is unique, time-sorted identifier
composed of an 48-bit timestamp and 16 to 208 bit randomness.

It is a flexible implementation of a [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) 
that can be generated in various bit-sizes and converted into different representations.


# Development

## Requirements

- [Python](https://python.org) 3.7 - 3.10
- [Poetry](https://pypi.org/project/poetry/)

## Clone and install dependencies

```shell
git clone https://github.com/iscc/iscc-flake.git
poetry install
```

## Run tests
```shell
poe test
```

## Run development server
```shell
poe develop
```

## List helper commands
```shell
poe --help
```

