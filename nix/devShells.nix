rec {
  shellHook-for = { package, pythoneda-base, python, nixpkgsRelease }: ''
    export PNAME="${package.pname}";
    export PVERSION="${package.version}";
    export PYVERSION="${python.name}";
    export NIXPKGSRELEASE="${nixpkgsRelease}";
    export PYTHONEDABASE="${pythoneda-base}";
    export PS1="\033[37m[\[\033[01;33m\]\$PNAME-\$PVERSION\033[01;37m|\033[01;32m\]\$PYVERSION\]\033[37m|\[\033[00m\]\[\033[01;34m\]\W\033[37m]\033[31m\$\[\033[00m\] ";
    echo;
    echo -e " \033[32m             _   _                          \033[35m_\033[0m";
    echo -e " \033[32m            | | | |                        \033[35m| | \033[37mGPLv3\033[0m";
    echo -e " \033[32m _ __  _   _| |_| |__   ___  _ __   \033[34m___  \033[35m__| | \033[36m__ _ \033[32mhttps://github.com/nixos/nixpkgs/tree/$NIXPKGSRELEASE\033[0m";
    echo -e " \033[32m| '_ \| | | | __| '_ \ / _ \| '_ \ \033[34m/ _ \\\\\033[35m/ _\` |\033[36m/ _\` |\033[33mhttps://github.com/pythoneda-shared/git/tree/$PVERSION\033[0m";
    echo -e " \033[32m| |_) | |_| | |_| | | | (_) | | | |\033[34m  __/\033[35m (_| |\033[36m (_| |\033[34mhttps://github.com/pythoneda-shared\033[0m";
    echo -e " \033[32m| .__/ \__, |\__|_| |_|\___/|_| |_|\033[34m\___|\033[35m\__,_|\033[36m\__,_|\033[35mhttps://github.com/pythoneda/base\033[0m";
    echo -e " \033[32m| |     __/ |                                       \033[36mhttps://github.com/pythoneda\033[0m";
    echo -e " \033[32m|_| \033[31mS\033[36mD\033[32m |___/                  \033[33mGIT                   \033[37mhttps://patreon.com/rydnr\033[0m";
    echo;
    echo " Thank you for using pythoneda-shared/git, PythonEDA in general, and for your appreciation of free software.";
    echo;
    export PYTHONPATH="$(python $PYTHONEDABASE/scripts/fix_pythonpath.py)";
  '';
  devShell-for = { package, pythoneda-base, python, pkgs, nixpkgsRelease }:
    pkgs.mkShell {
      buildInputs = [ package python.pkgs.pytest ];
      shellHook =
        shellHook-for { inherit package pythoneda-base python nixpkgsRelease; };
    };
}
