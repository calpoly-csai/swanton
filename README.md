# swanton
Swanton Pacific Ranch chatbot with a knowledge graph on a Raspberry Pi

## Getting Started

### Step 1 - Setup a fresh Debian 10 or Raspbian image

<details> 
    
```
$ cat /etc/os-release

PRETTY_NAME="Debian GNU/Linux 9 (stretch)"
NAME="Debian GNU/Linux"
VERSION_ID="9"
VERSION="9 (stretch)"
VERSION_CODENAME=stretch
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```

</details> 

```
sudo apt update \
    && sudo apt install -y git \
    && git clone https://github.com/calpoly-csai/swanton \
    && cd swanton \
    && ./debian_setup.sh
    
source $HOME/.poetry/env
```

### Step 2 - Verify Versions

python3 >= 3.6
```
$ python3 --version
Python 3.7.3
```

pip3 >= 20 using python >= 3.6
```
$ pip3 --version
pip 20.1.1 from /usr/local/lib/python3.7/dist-packages/pip (python 3.7)
```

poetry
```
$ poetry --version
Poetry version 1.0.10
```

### Step 3 - Install Python Dependencies
```
poetry install
```

[voice_kit_raspbian]: https://github.com/google/aiyprojects-raspbian
