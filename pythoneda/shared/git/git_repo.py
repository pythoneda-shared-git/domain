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
import abc
from git import Git, Repo
import logging
import os
from pythoneda.entity import Entity
from pythoneda.shared.git.error_cloning_git_repository import ErrorCloningGitRepository
from pythoneda.shared.git.git_checkout_failed import GitCheckoutFailed
from pythoneda.shared.git.git_progress_logging import GitProgressLogging
from pythoneda.shared.git.git_push import GitPush
from pythoneda.shared.git.git_tag import GitTag
from pythoneda.shared.git.ssh_private_key_git_policy import SshPrivateKeyGitPolicy
from pythoneda.shared.git.version import Version
from pythoneda.value_object import attribute
import re
import semver
import subprocess
from urllib.parse import urlparse
from typing import Dict, List

class GitRepo(Entity, abc.ABC):
    """
    Represents a Git repository.

    Class name: GitRepo

    Responsibilities:
        - Represents a git repository and its metadata.

    Collaborators:
        - None
    """

    def __init__(self, url: str, rev: str):
        """
        Creates a new Git repository instance.
        :param url: The url of the repository.
        :type url: str
        :param rev: The revision.
        :type rev: str
        """
        super().__init__()
        self._url = url
        self._rev = rev
        self._folder = None
        self._repo = None

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

    def latest_tag(self) -> str:
        """
        Retrieves the latest tag, if the repo has already been cloned.
        :return: Such name.
        :rtype: str
        """
        result = None
        if self._repo is not None:
            versions = []
            for tag in self._repo.tags:
                try:
                    version_info = semver.VersionInfo.parse(tag.name)
                    build = 0
                    match = re.search(r"\+build\.(\d+)", tag.name)
                    if match:
                        build = int(match.group(1))

                    versions.append((version_info, build, tag.name))
                except ValueError:
                    pass

            if versions:
                versions.sort(key=lambda v: (v[0], v[1]), reverse=True)
                result = versions[0][2]

        return result

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

    @classmethod
    def tag_exists(cls, url: str, tag: str) -> bool:
        """
        Checks whether a tag exists in given repository.
        :param url: The url of the repository.
        :type url: str
        :param tag: The tag to check.
        :type tag: str
        :return: True in such case.
        :rtype: bool
        """
        result = False
        try:
            output = subprocess.run(["git", "ls-remote", "--tags", url, tag], stdout=subprocess.PIPE, text=True)
            result = not (output.stdout is None) and (len(output.stdout) > 0)
        except subprocess.CalledProcessError:
            pass
        return result

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
        pattern = r"(?:https?://)?(?:www\.)?.*\.com/([^/]+)/([^/]+)"
        try:
            match = re.match(pattern, url)
            owner, repo_name = match.groups()
            return owner, repo_name

        except:
            logging.getLogger(cls.__name__).error(f"Invalid repo: {url}")

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
        logging.getLogger(__name__).debug(
            f"nix-prefetch-git --deepClone {self.url}/tree/{self.rev} -> {output}"
        )

        return output.splitlines()[-1]

    @abc.abstractmethod
    def clone(self, sshUsername: str, privateKeyFile: str, privateKeyPassphrase: str) -> Repo:
        """
        Clones this repo in given folder.
        :param sshUsername: The SSH username.
        :type sshUsername: str
        :param privateKey: The private key for SSH authentication.
        :type privateKey: str
        :param passphrase: The passphrase of the private key.
        :type passphrase: str
        :return: A git.Repo instance.
        :rtype: git.Repo
        """

    def raw_clone(self, folder: str, subfolder:str=None) -> Repo:
        """
        Clones this repo in given folder.
        :param folder: The base folder of the cloned repository.
        :type folder: str
        :param subfolder: An optional subfolder.
        :type subfolder: str
        :return: The final folder of the cloned repository.
        :rtype: str
        """
        result = folder

        if subfolder:
            result = os.path.join(folder, subfolder)

        try:
            subprocess.run(
                ["git", "clone", self.url, subfolder],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=folder,
            )
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise ErrorCloningGitRepository(self.url, folder)
        try:
            subprocess.run(
                ["git", "checkout", self.rev],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=result,
            )
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise GitCheckoutFailed(self.url, self.rev, folder)

        return Repo(result)

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
        Checks if the repository is hosted in github.com
        :return: True in such case.
        :rtype: bool
        """
        parsed_url = urlparse(self.url)
        return parsed_url.netloc == "github.com"

    def tag_version(self, version: Version):
        """
        Tags the repository with a new version, and pushes the tag.
        :param version: The new version.
        :type version: Version
        """
        print(f'folder -> {self._folder}, type -> {type(self._folder)}')
        GitTag(self._folder).create_tag(version.value)
        GitPush(self._folder).push_tags()

    def increase_major(self) -> Version:
        """
        Creates a new tag increasing the major in current version.
        :return: The new version.
        :rtype: Version from pythonedasharedgit.version
        """
        version = Version(self.latest_tag()).increase_major()
        self.tag_version(version)
        return version

    def increase_minor(self) -> Version:
        """
        Creates a new tag increasing the minor in current version.
        :return: The new version.
        :rtype: Version from pythonedasharedgit.version
        """
        version = Version(self.latest_tag()).increase_minor()
        self.tag_version(version)
        return version

    def increase_patch(self) -> Version:
        """
        Creates a new tag increasing the patch in current version.
        :return: The new version.
        :rtype: Version from pythonedasharedgit.version
        """
        version = Version(self.latest_tag()).increase_patch()
        self.tag_version(version)
        return version

    def increase_prerelease(self) -> Version:
        """
        Creates a new tag increasing the prerelease in current version.
        :return: The new version.
        :rtype: Version from pythonedasharedgit.version
        """
        version = Version(self.latest_tag()).increase_prerelease()
        self.tag_version(version)
        return version

    def increase_build(self) -> Version:
        """
        Creates a new tag increasing the build in current version.
        :return: The new version.
        :rtype: Version from pythonedasharedgit.version
        """
        print(f'latest_tag -> {self.latest_tag()}')
        version = Version(self.latest_tag()).increase_build()
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
