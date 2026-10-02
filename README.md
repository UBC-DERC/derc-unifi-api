<!-- badges: start -->
[![lifecycle](https://img.shields.io/badge/lifecycle-lifecycle_planning-crimson.svg)]()


<!-- badges: end -->

# DERC Vision API

An OpenAPI endpoint for researchers using the UBC Unifi Camera System.

This project is designed to act as a pathway for researchers to access camera data directly, without control over the existing camera system (or the need for direct ownership or management of the various device consoles). It is intended to be used both to prototype and run computer vision projects operating at DERC, and also to help manage data coming from the camera systems in a well-designed system. The DERC Vision API defines critical metadata for camera and computer vision systems (through a `Camera` class), and ties them directly to video clips and stills.



## Contribution

This project was developed by:

* [![ORCID](https://img.shields.io/badge/ORCID-0000--0002--2700--4605-green.svg)](https://orcid.org/0000-0002-2700-4605): Simon Goring

Contributions to this repository are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Installing this Package

To install `derc_unifi_api` from this GitHub repository, either install using a graphical tool such as GitKraken or GitHub Desktop, or install from the console using:

```bash
git clone https://github.com/UBC-DERC/derc_unifi_api.git
cd derc_unifi_api
```

## How to Use this Repository

<!--
A short description of how this repository is expected to be used.
-->


### Setting up the `uv` environment

This project uses `uv` as a package manager and to manage virtual environments. To use development tools including `ruff` and `ty`, you first need to install and synchronize the project. First check that you have [`uv` installed](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
```

Now you are ready to work on the project.

## Funding Statement

This project was funded by FarmCredit Canada through a grant to Drs von Keyserlingk and Weary at the UBC Dairy Education and Research Farm.

---

![UBC Logo and name as a wide figure.](assets/ubc-logo-2018-fullsig-blue-rgb72.jpg)
