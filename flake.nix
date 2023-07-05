{
  description = "Shared kernel for git concepts";

  inputs = rec {
    nixos.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils/v1.0.0";
    pythoneda-base = {
      url = "github:pythoneda/base/0.0.1a15";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
    };
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixos { inherit system; };
        description = "Shared kernel for git concepts";
        license = pkgs.lib.licenses.gpl3;
        homepage = "https://github.com/pythoneda-shared/git";
        maintainers = with pkgs.lib.maintainers; [ ];
        nixpkgsRelease = "nixos-23.05";
        shared = import ./nix/devShells.nix;
        pythoneda-shared-git-for = { version, pythoneda-base, python }:
          let
            pname = "pythoneda-shared-git";
            pythonVersionParts = builtins.splitVersion python.version;
            pythonMajorVersion = builtins.head pythonVersionParts;
            pythonMajorMinorVersion =
              "${pythonMajorVersion}.${builtins.elemAt pythonVersionParts 1}";
            pnameWithUnderscores =
              builtins.replaceStrings [ "-" ] [ "_" ] pname;
            wheelName =
              "${pnameWithUnderscores}-${version}-py${pythonMajorVersion}-none-any.whl";
          in python.pkgs.buildPythonPackage rec {
            inherit pname version;
            projectDir = ./.;
            src = ./.;
            format = "pyproject";

            nativeBuildInputs = with python.pkgs; [ pip pkgs.jq poetry-core ];
            propagatedBuildInputs = with python.pkgs; [
              dulwich
              GitPython
              paramiko
              pythoneda-base
              semver
            ];

            checkInputs = with python.pkgs; [ pytest ];

            pythonImportsCheck = [ "pythonedasharedgit" ];

            preBuild = ''
              python -m venv .env
              source .env/bin/activate
              pip install ${pythoneda-base}/dist/pythoneda_base-${pythoneda-base.version}-py3-none-any.whl
              rm -rf .env
            '';

            postInstall = ''
              mkdir $out/dist
              cp dist/${wheelName} $out/dist
              jq ".url = \"$out/dist/${wheelName}\"" $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json > temp.json && mv temp.json $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json
            '';

            meta = with pkgs.lib; {
              inherit description license homepage maintainers;
            };
          };
        pythoneda-shared-git-0_0_1a4-for = { pythoneda-base, python }:
          pythoneda-shared-git-for {
            version = "0.0.1a4";
            inherit pythoneda-base python;
          };
      in rec {
        packages = rec {
          pythoneda-shared-git-0_0_1a4-python39 =
            pythoneda-shared-git-0_0_1a4-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python39;
              python = pkgs.python39;
            };
          pythoneda-shared-git-0_0_1a4-python310 =
            pythoneda-shared-git-0_0_1a4-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python310;
              python = pkgs.python310;
            };
          pythoneda-shared-git-latest-python39 =
            pythoneda-shared-git-0_0_1a4-python39;
          pythoneda-shared-git-latest-python310 =
            pythoneda-shared-git-0_0_1a4-python310;
          pythoneda-shared-git-latest = pythoneda-shared-git-latest-python310;
          default = pythoneda-shared-git-latest;
        };
        defaultPackage = packages.default;
        devShells = rec {
          pythoneda-shared-git-0_0_1a4-python39 = shared.devShell-for {
            package = packages.pythoneda-shared-git-0_0_1a4-python39;
            pythoneda-base =
              pythoneda-base.packages.${system}.pythoneda-base-latest-python39;
            python = pkgs.python39;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-shared-git-0_0_1a4-python310 = shared.devShell-for {
            package = packages.pythoneda-shared-git-0_0_1a4-python310;
            pythoneda-base =
              pythoneda-base.packages.${system}.pythoneda-base-latest-python310;
            python = pkgs.python310;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-shared-git-latest-python39 =
            pythoneda-shared-git-0_0_1a4-python39;
          pythoneda-shared-git-latest-python310 =
            pythoneda-shared-git-0_0_1a4-python310;
          pythoneda-shared-git-latest = pythoneda-shared-git-latest-python310;
          default = pythoneda-shared-git-latest;

        };
      });
}
