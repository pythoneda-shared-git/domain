# Github shared kernel

This package provides a reusable model of git concepts.

## How to declare it in your flake

Check the latest tag of the artifact repository: https://github.com/pythoneda-shared-git/shared/tags, and use it instead of the `[version]` placeholder below.

```nix
{
  description = "[..]";
  inputs = rec {
    [..]
    pythoneda-shared-git-shared = {
      [optional follows]
      url =
        "github:pythoneda-shared-git-def/shared/[version]";
    };
  };
  outputs = [..]
};
```

Should you use another PythonEDA modules, you might want to pin those also used by this project. The same applies to [https://nixos/nixpkgs](nixpkgs "nixpkgs") and [https://github.com/numtide/flake-utils](flake-utils "flake-utils").

The Nix flake is managed by the [https://github.com/pythoneda-shared-git-def/shared](shared "shared") definition repository.

