<img src="./assets/logo.svg" alt="logo" width="50%">

Easy video cutting tool in python using Qt and MPV

![screenshot](./assets/screenshot.png)

## Build instructions
(currently not working)
To create the executable, simply run `sudo cp $(which ffmpeg) .; pyinstaller vidcutpro.spec -y`.
The executable will be in the `dist` folder.

## Installation

First build the binary with the build instruction. To install it, move to the git repo and run:

``` bash
# creates desktop file
echo "[Desktop Entry]\nVersion=1.0\nName=VidCutPro\nComment=Easy to use video cutting tool based on mpv and ffmpeg\nExec=${HOME}/.local/bin/vidcutpro\nIcon=${HOME}/.local/share/icons/hicolor/1024x1024/apps/vidcutpro.png\nTerminal=false\nType=Application\nCategories=Utility;" > vidcutpro.desktop

# links files to this repo
ln -s ${PWD}/dist/VidCutPro ${HOME}/.local/bin/vidcutpro
ln -s ${PWD}/assets/logo.png ${HOME}/.local/share/icons/hicolor/1024x1024/apps/vidcutpro.png
ln -s ${PWD}/vidcutpro.desktop ${HOME}/.local/share/applications/vidcutpro.desktop
```
