<img src="./assets/logo.svg" alt="logo" width="50%">

Easy video cutting and speed up / slow down tool based on ffmpeg. Extremely fast editing without loss of video quality!

![screenshot](./assets/screenshot.png)

## Run instructions
First install the required python dependencies with `pip install -r requirements.txt`.
Then run the program with `python vidcutpro.py`.

## Installation instructions
You can create an application menu entry for easy access. 
To set it up, change to the git repo and run:

``` bash
# creates desktop file in the current directory according to your home directory
echo "[Desktop Entry]
Version=1.0
Name=VidCutPro
Comment=Easy to use video cutting tool based on mpv and ffmpeg
Exec=sh -c '$(which python3) $(pwd)/vidcutpro.py'
Icon=${HOME}/.local/share/icons/hicolor/512x512/apps/vidcutpro.png
Terminal=false
Type=Application
Categories=Utility;" > vidcutpro.desktop

# copies files to this repo
rm ${HOME}/.local/share/icons/hicolor/512x512/apps/vidcutpro.png
rm ${HOME}/.local/share/applications/vidcutpro.desktop
cp -s ${PWD}/assets/logo.png ${HOME}/.local/share/icons/hicolor/512x512/apps/vidcutpro.png
cp -s ${PWD}/vidcutpro.desktop ${HOME}/.local/share/applications/vidcutpro.desktop
```
