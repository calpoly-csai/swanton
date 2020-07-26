# swanton
Swanton Pacific Ranch chatbot with a knowledge graph on a Raspberry Pi

## Getting Started

### On a fresh Debian/Raspbian image
```
sudo apt update \
    && sudo apt install -y git \
    && git clone https://github.com/calpoly-csai/swanton \
    && cd swanton \
    && ./debian_setup.sh
```

### On a [Google Voice Kit Raspbian][voice_kit_raspbian] image

<details>

So, uh..

[it's a bit complicated](https://github.com/google/aiyprojects-raspbian/issues/527)

[quite a bit complicated](https://github.com/google/aiyprojects-raspbian/issues/608)

but the commands below should make life easy 😎

</details>

```
sudo apt update \
    && sudo apt install -y git \
    && git clone https://github.com/calpoly-csai/swanton \
    && cd swanton \
    && ./voice_kit_raspbian_setup.sh \

sudo reboot

sudo ./debian_setup.sh

source $HOME/.poetry/env
```


## Verify Versions

### python3 >= 3.6
```
$ python3 --version
Python 3.7.3
```

### pip3 >= 20 using python >= 3.6
```
$ pip3 --version
pip 20.1.1 from /usr/local/lib/python3.7/dist-packages/pip (python 3.7)
```

### poetry
```
$ poetry --version
Poetry version 1.0.10
```


[voice_kit_raspbian]: https://github.com/google/aiyprojects-raspbian
