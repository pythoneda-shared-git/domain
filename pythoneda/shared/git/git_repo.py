# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_repo.py

This file declares the GitRepo class.

Copyright (C) 2023-today rydnr's pythoneda-shared-git/shared

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from git import Git, Repo
import os
from pythoneda.shared import attribute, Entity, EventReference
from pythoneda.shared.git import (
    GitTag,
    Version,
)
import re
import subprocess
from urllib.parse import urlparse
from typing import Dict, List


class GitRepo(Entity):
    """
    Represents a Git repository.

    Class name: GitRepo

    Responsibilities:
        - Represents a git repository and its metadata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        url: str,
        rev: str = "main",
        folder: str = None,
        repo=None,
        eventHistory: List[EventReference] = [],
    ):
        """
        Creates a new Git repository instance.
        :param url: The url of the repository.
        :type url: str
        :param rev: The revision.
        :type rev: str
        :param folder: The cloned folder.
        :type folder: str
        :param repo: The underlying repository.
        :type repo: git.Repo
        :param eventHistory: The event history.
        :type eventHistory: List[pythoneda.shared.EventReference]
        """
        self._url = url
        self._rev = rev
        self._folder = folder
        self._repo = repo
        super().__init__(eventHistory=eventHistory)

    @property
    @attribute
    def url(self) -> str:
        """
        Retrieves the repository url.
        :return: Such url.
        :rtype: str
        """
        return self._url

    @property
    @attribute
    def rev(self) -> str:
        """
        Retrieves the revision in the git repository we're interested in.
        :return: Such value.
        :rtype: str
        """
        return self._rev

    @property
    @attribute
    def folder(self) -> str:
        """
        Retrieves the folder where the repo is cloned.
        :return: Such value.
        :rtype: str
        """
        return self._folder

    @property
    @attribute
    def repo(self) -> Repo:
        """
        Retrieves the repo instance.
        :return: Such instance.
        :rtype: git.Repo
        """
        return self._repo

    @property
    def remote_url(self) -> str:
        """
        Retrieves the remote url of the current branch in the cloned folder.
        :return: Such url.
        :rtype: str
        """
        branch = self.repo.active_branch
        remote_name = self.repo.git.config(f"branch.{branch.name}.remote")
        return self.repo.remotes[remote_name].url

    @classmethod
    def from_folder(cls, folder: str):
        """
        Creates a GitRepo from given folder.
        :param folder: The cloned repository.
        :type folder: str
        :return: A GitRepo.
        :rtype: pythoneda.shared.git.GitRepo
        """
        result = None

        repo = Repo(folder)

        if repo.active_branch and repo.active_branch.tracking_branch():
            remote_name = repo.active_branch.tracking_branch().remote_name
            branch = repo.active_branch.tracking_branch().name.split("/")[-1]
            remote = repo.remote(remote_name)
            result = GitRepo(remote.url, branch, folder, repo)

        return result

    def latest_tag(self) -> str:
        """
        Retrieves the latest tag, if the repo has already been cloned.
        :return: Such name.
        :rtype: str
        """
        return GitTag(self.folder).latest_tag()

    @classmethod
    def url_is_a_git_repo(cls, url: str) -> bool:
        """
        Checks whether given url points to a git repository.
        :param url: The url to check.
        :type url: str
        :return: True in such case.
        :rtype: bool
        """
        try:
            subprocess.check_output(["git", "ls-remote", url], stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False

    def repo_owner_and_repo_name(self) -> tuple:
        """
        Retrieves the owner and repository name.
        :return: The tuple (owner, repo).
        :rtype: tuple
        """
        return self.__class__.extract_repo_owner_and_repo_name(self.url)

    @classmethod
    def extract_repo_owner_and_repo_name(cls, url: str) -> tuple:
        """
        Extracts the repo owner and repo name from given url.
        :param url: The url.
        :type url: str
        :return: The tuple (owner, repo).
        :rtype: tuple
        """
        owner = None
        repo_name = None
        try:
            owner, repo_name = re.match(
                r"(?:https?://)?(?:www\.)?.*\.com/([^/]+)/([^/]+)", url
            ).groups()
        except Exception as err:
            try:
                owner, repo_name, _ = re.match(
                    r"github:([^/]+)?/([^/]+)?/(.*)?", url
                ).groups()
            except Exception as anotherErr:
                GitRepo.logger().error(f"Invalid repo: {url}, {err}, {anotherErr}")

        return owner, repo_name

    def sha256(self) -> str:
        """
        Retrieves the sha256 checksum of the repository.
        :return: Such checksum.
        :rtype: str
        """
        result = subprocess.run(
            ["nix-prefetch-git", "--deepClone", f"{self.url}/tree/{self.rev}"],
            check=True,
            capture_output=True,
            text=True,
        )
        output = result.stdout
        GitRepo.logger().debug(
            f"nix-prefetch-git --deepClone {self.url}/tree/{self.rev} -> {output}"
        )

        return output.splitlines()[-1]

    def clone(
        self, sshUsername: str, privateKeyFile: str, privateKeyPassphrase: str
    ) -> Repo:
        """
        Clones this repo in given folder.
        :param sshUsername: The SSH username.
        :type sshUsername: str
        :param privateKeyFile: The private key for SSH authentication.
        :type privateKeyFile: str
        :param privateKeyPassphrase: The passphrase of the private key.
        :type privateKeyPassphrase: str
        :return: A git.Repo instance.
        :rtype: git.Repo
        """
        raise NotImplementedError()

    @classmethod
    def extract_url_and_subfolder(cls, url: str) -> tuple:
        """
        Extracts the url and subfolder from given url.
        :param url: The repository url.
        :type url: str
        :return: The tuple (url, subfolder)
        :rtype: tuple
        """
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split("/")

        if len(path_parts) > 4 and path_parts[3] == "tree":
            repo_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_parts[1]}/{path_parts[2]}"
            subfolder = "/".join(path_parts[5:])
        elif len(path_parts) > 3:
            repo_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_parts[1]}/{path_parts[2]}"
            subfolder = "/".join(path_parts[3:])
        else:
            repo_url = url
            subfolder = None

        return repo_url, subfolder

    def in_github(self) -> bool:
        """
        Checks if the repository is hosted in gitHub.com
        :return: True in such case.
        :rtype: bool
        """
        parsed_url = urlparse(self.url)
        return parsed_url.netloc == "github.com"

    def tag_version(self, version: Version):
        """
        Tags given version.
        :param version: The version.
        :type version: pythoneda.shared.git.Version
        :raise pythoneda.shared.git.GitTagFailed: If the tag fails.
        """
        GitTag(self.folder).create_tag(version.value)

    def increase_major(self, tag: bool = False) -> Version:
        """
        Creates a new tag increasing the major in current version.
        :param tag: Whether to tag automatically or not.
        :type tag: bool
        :return: The new version.
        :rtype: pythoneda.shared.git.Version
        """
        latest_tag = self.latest_tag()
        if latest_tag is None:
            version = Version("0.0.0")
        else:
            version = Version(latest_tag).increase_major()
        if tag:
            self.tag_version(version)
        return version

    def increase_minor(self, tag: bool = False) -> Version:
        """
        Creates a new tag increasing the minor in current version.
        :param tag: Whether to tag automatically or not.
        :type tag: bool
        :return: The new version.
        :rtype: pythoneda.shared.git.Version
        """
        latest_tag = self.latest_tag()
        if latest_tag is None:
            version = Version("0.0.0")
        else:
            version = Version(latest_tag).increase_minor()
        if tag:
            self.tag_version(version)
        return version

    def increase_patch(self, tag: bool = False) -> Version:
        """
        Creates a new tag increasing the patch in current version.
        :param tag: Whether to tag automatically or not.
        :type tag: bool
        :return: The new version.
        :rtype: pythoneda.shared.git.Version
        """
        latest_tag = self.latest_tag()
        if latest_tag is None:
            version = Version("0.0.0")
        else:
            version = Version(latest_tag).increase_patch()
        if tag:
            self.tag_version(version)
        return version

    def increase_prerelease(self, tag: bool = False) -> Version:
        """
        Creates a new tag increasing the prerelease in current version.
        :param tag: Whether to tag automatically or not.
        :type tag: bool
        :return: The new version.
        :rtype: pythoneda.shared.git.Version
        """
        latest_tag = self.latest_tag()
        if latest_tag is None:
            version = Version("0.0.0")
        else:
            version = Version(latest_tag).increase_prerelease()
        if tag:
            self.tag_version(version)
        return version

    def increase_build(self, tag: bool = False) -> Version:
        """
        Creates a new tag increasing the build in current version.
        :param tag: Whether to tag automatically or not.
        :type tag: bool
        :return: The new version.
        :rtype: pythoneda.shared.git.Version
        """
        latest_tag = self.latest_tag()
        if latest_tag is None:
            version = Version("0.0.0")
        else:
            version = Version(latest_tag).increase_build()
        if tag:
            self.tag_version(version)
        return version

    @classmethod
    def remote_urls(cls, clonedFolder: str) -> Dict:
        """
        Retrieves the remote urls of given repository.
        :param clonedFolder: The repository folder.
        :type clonedFolder: str
        :return: For each remote repository, a list with its urls.
        :rtype: Dict[List[str]]
        """
        repo = Repo(clonedFolder)
        result = {}
        for remote in repo.remotes:
            result[remote.name] = list(remote.urls)
        return result

    @classmethod
    def current_branch(cls, clonedFolder: str) -> str:
        """
        Retrieves the current branch of given repository.
        :param clonedFolder: The repository folder.
        :type clonedFolder: str
        :return: The current branch.
        :rtype: str
        """
        repo = Repo(clonedFolder)
        return repo.active_branch.name


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
