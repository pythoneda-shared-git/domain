"""
pythonedasharedgit/ssh_git_repo.py

This file declares the SshGitRepo class.

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
from dulwich import porcelain
from git import Repo
from pythoneda.value_object import attribute, sensitive
from pythonedaartifacteventgittagging.tag_credentials_provided import TagCredentialsProvided
from pythonedasharedgit.git_repo import GitRepo
from pythonedasharedgit.ssh_vendor import SshVendor

class SshGitRepo(GitRepo):
    """
    Represents a Git repository accessed via SSH.

    Class name: SshGitRepo

    Responsibilities:
        - Represents a git repository and its metadata.
        - Clone a git repository via SSH.

    Collaborators:
        - GitRepo: To provide support for git operations.
    """

    def __init__(self, url: str, rev: str, sshUsername: str, privateKeyFile: str, privateKeyPassphrase: str):
        """
        Creates a new Git repository instance.
        :param url: The url of the repository.
        :type url: str
        :param rev: The revision.
        :type rev: str
        :param sshUsername: The SSH username.
        :type sshUsername: str
        :param privateKeyFile: The private key for SSH authentication.
        :type privateKeyFile: str
        :param privateKeyPassphrase: The passphrase of the private key.
        :type privateKeyPassphrase: str
        """
        super().__init__(url, rev)
        self._ssh_username = sshUsername
        self._private_key_file = privateKeyFile
        self._private_key_passphrase = privateKeyPassphrase

    @property
    @attribute
    @sensitive
    def ssh_username(self) -> str:
        """
        Retrieves the SSH user name.
        :return: Such user name.
        :rtype: str
        """
        return self._ssh_username

    @property
    @attribute
    @sensitive
    def private_key_file(self) -> str:
        """
        Retrieves the location of the private key.
        :return: Such path.
        :rtype: str
        """
        return self._private_key_file

    @property
    @attribute
    @sensitive
    def private_key_passphrase(self) -> str:
        """
        Retrieves the private key passphrase.
        :return: Such value.
        :rtype: str
        """
        return self._private_key_passphrase


    def clone(self) -> Repo:
        """
        Clones this repo via SSH.
        :return: A git.Repo instance.
        :rtype: git.Repo
        """
        vendor = SshVendor(self.ssh_username, self.private_key_file, self.private_key_passphrase)
        self._folder = tempfile.TemporaryDirectory()
        add_folder_to_cleanup(self._folder)
        return porcelain.clone(self.url, self._folder, ssh_vendor=vendor)
