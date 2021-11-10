# Himitsu
![interactive mode
](interactive.png)

А steganographic script that puts files into an image

## Installation
```console
# clone the repo
$ git clone https://github.com/Ryokucha-N/himitsu.git

# change the working directory
$ cd himitsu
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

if save mode is selected:
```console
$ python3 himitsu.py s [input_image] [input_file] [output_image]
```

if load mode is selected:
```console
$ python3 himitsu.py l [input_image] [output_file]
```
