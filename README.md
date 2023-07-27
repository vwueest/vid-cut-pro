<img src="./assets/logo.svg" alt="logo" width="50%">

Easy video cutting tool in python using Qt and MPV

![screenshot](./assets/screenshot.png)

## Build instructions

To create the executable, simply run `rm -r build dist vidcutpro.spec; pyinstaller vidcutpro.py --onefile --noconsole`

to install it system wide to to the git repo and run

``` bash

echo "[Desktop Entry]\nVersion=1.0
Name=VidCutPro\nComment=Easy to use video cutting tool based on mpv and ffmpeg\nExec=${HOME}/.local/bin/vidcutpro\nIcon=${HOME}/.local/share/icons/hicolor/1024x1024/apps/vidcutpro.png\nTerminal=false\nType=Application\nCategories=Utility;" > vidcutpro.desktop

ln -s ${PWD}/vidcutpro ${HOME}/.local/bin/vidcutpro
ln -s ${PWD}/assets/logo.png ${HOME}/.local/share/icons/hicolor/1024x1024/apps/vidcutpro.png
ln -s ${PWD}/vidcutpro.desktop ${HOME}/.local/share/applications/vidcutpro.desktop
```
