# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_checkout.py

This file declares the GitCheckout class.

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
from .git_check_attr_all_failed import GitCheckoutAllFailed
from .git_check_attr_failed import GitCheckoutFailed
from .git_operation import GitOperation
from typing import Dict


class GitCheckout(GitOperation):
    """
    Provides git checkout operations.

    Class name: GitCheckout

    Responsibilities:
        - Provides "git checkout" operations.

    Collaborators:
        - pythoneda.shared.git.GitCheckoutFailed: If the operation fails.
    """

    def __init__(self, folder: str):
        """
        Creates a new GitCheckout instance for given folder.
        :param folder: The cloned repository.
        :type folder: str
        """
        super().__init__(folder)

    def checkout(self, rev: str, file: str = None):
        """
        Performs a checkout.
        :param rev: The revision.
        :type rev: str
        :param file: The file to check out. Optional
        :type file: str
        """
        result = None

        args = ["git", "checkout", rev]
        if file:
            args.append(file)

        (code, stdout, stderr) = self.run(args)
        if code != 0:
            if stderr != "":
                GitCheckout.logger().error(stderr)
            if stdout != "":
                GitCheckout.logger().error(stdout)
            raise GitCheckoutFailed(self.folder, rev, file, stderr)
        GitCheckout.logger().debug(f"git checkout {rev} {file} -> {result}")

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
