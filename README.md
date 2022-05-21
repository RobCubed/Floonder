# Floonder
Simple frontend for OvenMediaEngine, using flask





# Installation guidelines are for an older version, new instructions will be added soon
## Installation
* Install FFMPEG for your respective platform. This will likely be in your repositories on Linux. On Windows, download it from the [website](https://ffmpeg.org/) and put `ffmpeg.exe` in the Floonder directory
* Download [rtsp-simple-server](https://github.com/aler9/rtsp-simple-server) for your respective platform
* Extract and configure. The only 100% required change is to enable the `api` option to `yes`.
* Install the Python dependencies. The simplest way is to execute this command: `pip install --user flask passlib`.
* Set up `config.py`. Rename `config.template.py` to `config.py` and set the values as commented.
* Run `python3 app.py`
