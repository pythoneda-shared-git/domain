# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/git_check_attr.py

This file declares the GitCheckAttr class.

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
from .git_check_attr_all_failed import GitCheckAttrAllFailed
from .git_check_attr_failed import GitCheckAttrFailed
from .git_operation import GitOperation
from typing import Dict


class GitCheckAttr(GitOperation):
    """
    Provides git check-attr operations.

    Class name: GitCheckAttr

    Responsibilities:
        - Provides "git check-attr" operations.

    Collaborators:
        - pythoneda.shared.git.GitCheckAttrFailed: If the operation fails.
    """

    def __init__(self, folder: str):
        """
        Creates a new GitCheckAttr instance for given folder.
        :param folder: The cloned repository.
        :type folder: str
        """
        super().__init__(folder)

    @staticmethod
    def _extract_attributes(output: str) -> Dict[str, str]:
        """
        Parses the output of `git check-attr`.
        :param output: The output.
        :type output: str
        :return: A dictionary of attribute names and values.
        :rtype: Dict[str,str]
        """
        result = {}

        for line in output.strip().split("\n"):
            parts = line.split(": ")
            if len(parts) == 3:
                result[parts[1]] = parts[2]

        return result

    def check_attr_all(self, file: str) -> Dict[str, str]:
        """
        Retrieves all attributes of given file.
        :param file: The file to inspect.
        :type file: str
        :return: A dictionary with the attribute names and values.
        :rtype: Dict[str, str]
        """
        result = None

        (code, stdout, stderr) = self.run(["git", "check-attr", "-a", file])
        GitCheckAttr.logger().debug(f"git check-attr -a {file} -> {code}")
        if code == 0:
            result = self._extract_attributes(stdout)
        else:
            if stderr != "":
                GitCheckAttr.logger().error(stderr)
            if stdout != "":
                GitCheckAttr.logger().error(stdout)
            raise GitCheckAttrAllFailed(self.folder, file, stderr)

        return result

    def check_attr(self, attr: str, file: str) -> str:
        """
        Retrieves an attribute of given file.
        :param attr: The attribute name.
        :type attr: str
        :param file: The file to inspect.
        :type file: str
        :return: The value of the attribute, if it's defined; None otherwise.
        :rtype: str
        """
        result = None

        (code, stdout, stderr) = self.run(["git", "check-attr", attr, file])
        if code == 0:
            result = self._extract_attributes(stdout).get(attr, None)

        else:
            if stderr != "":
                GitCheckAttr.logger().error(stderr)
            if stdout != "":
                GitCheckAttr.logger().error(stdout)
            raise GitCheckAttrFailed(self.folder, attr, file, stderr)
        GitCheckAttr.logger().debug(f"git check-attr {attr} {file} -> {result}")

        return result
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
