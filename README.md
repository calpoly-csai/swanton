# swanton
Swanton Pacific Ranch chatbot with a knowledge graph on a Raspberry Pi.
Please refer to the [Cal Poly CSAI Docs](https://docs.calpolycsai.com/projects/swanton-ranch-ai) for a conceptual understanding of the project and [this repository's wiki](https://github.com/calpoly-csai/swanton/wiki) for more information about setup and operation.
## Getting Started

### Step 1 - Setup a fresh Debian 10 or Raspbian image
On a raspberry pi, we recommend using the AIY voicekit image from [here](https://github.com/google/aiyprojects-raspbian/releases) for your sd card.

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
