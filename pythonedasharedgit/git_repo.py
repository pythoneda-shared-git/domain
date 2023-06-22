"""
pythonedasharedgit/git_repo.py

This file declares the GitRepo class.

Copyright (C) 2023-today rydnr's pythoneda-shared/git

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
from pythoneda.entity import Entity
from pythoneda.value_object import attribute
from pythonedasharedgit.error_cloning_git_repository import ErrorCloningGitRepository
from pythonedasharedgit.git_checkout_failed import GitCheckoutFailed

import logging
import os
import re
import subprocess
from urllib.parse import urlparse
from typing import Dict


class GitRepo(Entity):
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
        :param repoInfo: The repository metadata.
        :type repoInfo: Dict
        :param subfolder: Whether it's a monorepo and we're interested only in a subfolder.
        :type subfolder: str
        """
        super().__init__()
        self._url = url
        self._rev = rev

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

    def clone(self, folder: str, subfolder: str) -> str:
        """
        Clones this repo in given folder.
        :param folder: The base folder of the cloned repository.
        :type folder: str
        :param subfolder: An optional subfolder.
        :type subfolder: str
        :return: The final folder of the cloned repository.
        :rtype: str
        """
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

        return result

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
