"""
pythoneda/shared/git/ssh_git_repo.py

This file declares the SshGitRepo class.

Copyright (C) 2023-today rydnr's pythoneda-shared-git/git

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
import atexit
from dulwich.repo import Repo
from dulwich.client import get_transport_and_path
from dulwich.protocol import Protocol, ZERO_SHA
from git import Repo
import os
from paramiko import RSAKey, AutoAddPolicy
from paramiko.client import SSHClient
from paramiko.agent import AgentRequestHandler, AgentServerProxy
from pythoneda.shared.git.git_repo import GitRepo
from pythoneda.shared.git.ssh_vendor import SshVendor
from pythoneda.value_object import attribute, sensitive
import shutil
import tempfile

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
#        self._private_key_file = privateKeyFile
        self._private_key_file = "/home/chous/.ssh/id_rsa-unveilingpartner.pub"
#        self._private_key_passphrase = privateKeyPassphrase
        self._private_key_passphrase = ""

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
#    @attribute
    def private_key_file(self) -> str:
        """
        Retrieves the location of the private key.
        :return: Such path.
        :rtype: str
        """
        return self._private_key_file

    @property
    @attribute
#    @sensitive
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
#        vendor = SshVendor(self.ssh_username, self.private_key_file, self.private_key_passphrase)
#        client, path = get_transport_and_path(self.url, ssh_vendor=vendor)
        self._folder = tempfile.TemporaryDirectory().name
        add_folder_to_cleanup(self._folder)

        ssh_cmd = f'ssh -i {self.private_key_file} -o StrictHostKeyChecking=no'

        os.environ['GIT_SSH_COMMAND'] = ssh_cmd
        result = Repo.clone_from(self.url, self._folder)
        self._repo = result
        print(f'repo -> {result}')
        return result


_folders_to_cleanup = []

def add_folder_to_cleanup(folder: str):
    """
    Adds a new folder to cleanup at exit.
    :param folder: The new folder.
    :type folder: str
    """
    _folders_to_cleanup.append(folder)

def cleanup():
    """
    Cleans up cloned repositories.
    """
    for folder in _folders_to_cleanup:
        shutil.rmtree(folder)

atexit.register(cleanup)
