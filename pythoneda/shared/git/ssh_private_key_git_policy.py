"""
pythoneda/shared/git/ssh_private_key_git_policy.py

This file declares the SshPrivateKeyGitPolicy class.

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
import os
import paramiko
from pythoneda.value_object import attribute, sensitive, ValueObject
from typing import Dict

class SshPrivateKeyGitPolicy(ValueObject):
    """
    A policy to use a private key for git operations over ssh.

    Class name: SshPrivateKeyGitPolicy

    Responsibilities:
        - Build a git.transport instance configured to use a private key.

    Collaborators:
        - None
    """
    def __init__(self, username: str, privateKeyFile: str, passphrase: str):
        """
        Creates a new SshPrivateKeyGitPolicy instance.
        :param username: The SSH username.
        :type username: str
        :param privateKey: The path to the private key.
        :type privateKey: str
        :param passphrase: The passphrase of the private key.
        :type passphrase: str
        """
        super().__init__()
        self._username = username
        self._private_key = privateKey
        self._passphrase = passphrase

    @property
    @attribute
    def username(self) -> str:
        """
        Retrieves the SSH username.
        :return: Such value.
        :rtype: str
        """
        return self._username

    @property
    @attribute
    @sensitive
    def private_key(self) -> str:
        """
        Retrieves the path of the private key file.
        :return: Such path.
        :rtype: str
        """
        return self._private_key

    @property
    @attribute
    @sensitive
    def passphrase(self) -> str:
        """
        Retrieves the passphrase.
        :return: Such value.
        :rtype: str
        """
        return self._passphrase

    def build_transport(self):
        """
        Builds a git.transport.Transport instance to use a private key.
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())

        # Provide the path to the private key and its passphrase
        pkey = paramiko.RSAKey.from_private_key_file(
            self.private_key, password=self.passphrase,
        )

        client.connect(args[0], username=self.username, pkey=pkey)
        return client.get_transport()
