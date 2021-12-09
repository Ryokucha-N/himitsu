# Himitsu
![interactive mode
](interactive.png)

А steganographic script  to hide files in images and audio files

Supported audio formats:
  .waw(stereo)


Supported image formats:
  .png
  .tga
  .tif
  
but theoretically all RGBA image formats with lossless compression are supported


## Installation
```console
# clone the repo
$ git clone https://github.com/Ryokucha-N/himitsu.git

# change the working directory
$ cd himitsu

# install the requirements
$ python3 -m pip install -r requirements.txt
```
## Usage
### interactive
```console
$ python3 himitsu.py
```
Select the mode (enter the menu item number). Next, enter the data that the script requires.

### with arguments
```console
$ python3 himitsu.py [mode] [arguments]
```

Saving:
```console
# image
$ python3 himitsu.py si [input_image] [input_datafile] [output_image]

# audio
$ python3 himitsu.py sa [input_audio] [input_datafile] [output_audio]
```

Loading:
```console
# image
$ python3 himitsu.py li [input_image] [output_datafile]

# audio
$ python3 himitsu.py li [input_audio] [output_datafile]
```
