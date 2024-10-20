<img src="./assets/logo.svg" alt="logo" width="50%">

Easy video cutting and speed up / slow down tool based on ffmpeg. Extremely fast editing without loss of video quality!

![screenshot](./assets/screenshot.png)

## Run instructions
First install the required python dependencies with `pip install -r requirements.txt`.
Then run the program with `python vidcutpro.py`.

## Build instructions
If you would like to create a standalone executable, you can do so by running `pyinstaller vidcutpro.spec -y`.
The executable will be in the `dist` folder and is roughly 70 MB in size.

## Installation instructions
You can create an application menu entry for easy access to the application. 
First build the binary with the build instruction.
To install it, change to the git repo and run:

``` bash
# creates desktop file in the current directory according to your home directory
echo "[Desktop Entry]
Version=1.0
Name=VidCutPro
Comment=Easy to use video cutting tool based on mpv and ffmpeg
Exec=${HOME}/.local/bin/vidcutpro
Icon=${HOME}/.local/share/icons/hicolor/512x512/apps/vidcutpro.png
Terminal=false
Type=Application
Categories=Utility;" > vidcutpro.desktop

# copies files to this repo
rm ${HOME}/.local/bin/vidcutpro
rm ${HOME}/.local/share/icons/hicolor/512x512/apps/vidcutpro.png
rm ${HOME}/.local/share/applications/vidcutpro.desktop
cp -s ${PWD}/dist/VidCutPro ${HOME}/.local/bin/vidcutpro
cp -s ${PWD}/assets/logo3.png ${HOME}/.local/share/icons/hicolor/512x512/apps/vidcutpro.png
cp -s ${PWD}/vidcutpro.desktop ${HOME}/.local/share/applications/vidcutpro.desktop
```
