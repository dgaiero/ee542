# NAME TBD

- [NAME TBD](#name-tbd)
  - [Installing and Setup](#installing-and-setup)
    - [Setting up a new raspberry pi](#setting-up-a-new-raspberry-pi)
    - [Installing `Python 3.9.0`](#installing-python-390)
    - [Miscellanous](#miscellanous)

## Installing and Setup

<!-- Requires `vcgencmd` command. If this is not included on your installation, you can add the unofficial PPA `ppa:ubuntu-raspi2/ppa` with the following:

* `sudo add-apt-repository ppa:ubuntu-raspi2/ppa`
* `sudo apt-get update` -->

<!-- To use the spi and i2c libraries, you need the `Python.h` header file. This can
be obtained using the following command:
* `sudo apt install libpython3.7-dev` -->

### Setting up a new raspberry pi

> This guide assumes you are running `raspberrian`

You can run the `configure.sh` file, or follow the steps below. Please note,
if you run `configure.sh`, you still need to follow steps 1-3 outlined below.

1. Run ssh-keygen to generate a new deploy key on the pi
2. Copy the id_rsa.pub key to the GitHub `deploy keys` section. Make sure to give the key a useful name and **not** give it write access.[^1]
3. Clone the repository (`git@github.com:dgaiero/cpe542.git`)
4. Create a `.env` file with the following text:
`echo PYTHONPATH=${PYTHONPATH}:${PWD} >> .env`
5. Add the `AWS` certificates.
6. Install `python 3.9` (follow section below)
7. Enable `i2c` and `spi`
   1. `sudo raspi-config`
   2. Select option `5`
   3. Enable `i2c` and `spi` options
   4. Reboot `sudo reboot`
   5. Install `spi` dependencies: `sudo apt install python-smbus python3-smbus python-dev python3-dev`
   6. Install `i2c` tools: `sudo apt install i2c-tools`
   7. In `/boot/config.txt`, verify that the following lines are set to `on`
      1. `dtparam=i2c1=on`
      2. `dtparam=i2c_arm=on`
   8. Verify that `i2c-dev` is in `/etc/modules`
   9. Add the current account to the `i2c` group: `sudo adduser $USER i2c`
8. For `awscrt`, `cmake` and `libssl-dev` must be installed
   - `sudo apt install cmake libssl-dev`
9. Install `pipenv`: `sudo apt install pipenv`
10. Setup `pipenv`: `pipenv innstall --dev`

### Installing `Python 3.9.0`

The instructions outlined below install this python version _without_ modifying any current python install.

```shell
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
cd /tmp
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
tar -xf Python-3.9.0.tgz
cd Python-3.9.0
./configure --enable-optimizations
sudo make altinstall
```

### Miscellanous

- If you need to remove the virtual environment, run `pipenv --rm`.
- If your `Pipfile.lock` gets out of date, you can run `pipenv lock` to update the `Pipfile.lock` file
- To see what i2c devices are connected, use the command `i2cdetect -y 1`

[^1]: This is used so you don't have to login to the pi with your github account
or link your github account to the pi.
