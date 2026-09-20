# Home Manager module for VidCutPro. No flakes.
#
#   # ~/.config/home-manager/home.nix (or wherever your config lives)
#   {
#     imports = [ (import /home/you/src/vid-cut-pro/nix/hm-module.nix) ];
#     programs.vidcutpro.enable = true;
#   }
#
# To pin a checkout instead of using a local path:
#
#   let
#     vidcutpro = builtins.fetchGit {
#       url = "git+ssh://git@github.com/vwueest/vid-cut-pro.git";
#       ref = "main";
#     };
#   in { imports = [ (import "${vidcutpro}/nix/hm-module.nix") ]; }
#
# Installs ~/.local/bin/vidcutpro, a desktop entry that claims the common video
# mime types, and the app icon. The launcher exists because the app is a PyQt5
# script, not a package: it needs ffmpeg on PATH and the Qt platform plugins
# pointed at the right store paths, neither of which the script can arrange for
# itself.
{ config, lib, pkgs, ... }:

let
  cfg = config.programs.vidcutpro;

  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    ffmpeg-python
    pyqt5
  ]);

  launcher = pkgs.writeShellScript "vidcutpro-launcher" ''
    if [ "$XDG_SESSION_TYPE" = "wayland" ] || [ -n "$WAYLAND_DISPLAY" ]; then
      export QT_QPA_PLATFORM=wayland
    fi
    export QT_PLUGIN_PATH="${pkgs.qt5.qtbase.bin}/${pkgs.qt5.qtbase.qtPluginPrefix}:${pkgs.qt5.qtwayland.bin}/${pkgs.qt5.qtbase.qtPluginPrefix}:${pkgs.qgnomeplatform}/${pkgs.qt5.qtbase.qtPluginPrefix}:${pkgs.adwaita-qt}/${pkgs.qt5.qtbase.qtPluginPrefix}"
    if [ "$XDG_CURRENT_DESKTOP" = "GNOME" ] || [ "$XDG_CURRENT_DESKTOP" = "ubuntu:GNOME" ]; then
      export QT_QPA_PLATFORMTHEME=gnome
    fi
    export PATH="${pkgs.lib.makeBinPath [
      pkgs.ffmpeg
      pkgs.libnotify
      pkgs.xdg-utils
    ]}:$PATH"

    exec ${pythonEnv}/bin/python3 ${../vidcutpro.py} "$@"
  '';

  desktopEntry = pkgs.makeDesktopItem {
    name = "vidcutpro";
    desktopName = "VidCutPro";
    comment = "Easy to use video cutting tool based on ffmpeg";
    exec = "${launcher} %f";
    icon = "vidcutpro";
    terminal = false;
    categories = [ "AudioVideo" "Video" "Utility" ];
    mimeTypes = cfg.mimeTypes;
  };
in
{
  options.programs.vidcutpro = {
    enable = lib.mkEnableOption "VidCutPro, a video cutting tool over ffmpeg";

    mimeTypes = lib.mkOption {
      type = lib.types.listOf lib.types.str;
      default = [ "video/mp4" "video/x-matroska" "video/webm" "video/avi" ];
      description = ''
        Video types the desktop entry offers to open.

        This only puts VidCutPro in the "Open With" list; it does not make it
        the default handler for them.
      '';
    };
  };

  config = lib.mkIf cfg.enable {
    home.packages = [ desktopEntry ];

    home.file.".local/bin/vidcutpro".source = launcher;

    home.file.".local/share/icons/hicolor/512x512/apps/vidcutpro.png".source =
      ../assets/logo.png;
  };
}
