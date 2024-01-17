# vim: set fileencoding=utf-8
"""
pythoneda/shared/git/__init__.py

This file ensures pythoneda.shared.git is a package.

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .error_cloning_git_repository import ErrorCloningGitRepository
from .git_add_failed import GitAddFailed
from .git_add_all_failed import GitAddAllFailed
from .git_apply_failed import GitApplyFailed
from .git_checkout_failed import GitCheckoutFailed
from .git_check_attr_all_failed import GitCheckAttrAllFailed
from .git_check_attr_failed import GitCheckAttrFailed
from .git_diff_failed import GitDiffFailed
from .git_init_failed import GitInitFailed
from .git_push_branch_failed import GitPushBranchFailed
from .git_push_failed import GitPushFailed
from .git_push_tags_failed import GitPushTagsFailed
from .git_stash_pop_failed import GitStashPopFailed
from .git_stash_push_failed import GitStashPushFailed
from .git_tag_failed import GitTagFailed

from .git_operation import GitOperation
from .git_add import GitAdd
from .git_apply import GitApply
from .git_check_attr import GitCheckAttr
from .git_diff import GitDiff
from .git_init import GitInit
from .git_progress_logging import GitProgressLogging
from .git_push import GitPush
from .git_stash import GitStash
from .git_tag import GitTag
from .ssh_private_key_git_policy import SshPrivateKeyGitPolicy
from .ssh_vendor import SshVendor
from .version import Version
from .git_repo import GitRepo
from .ssh_git_repo import SshGitRepo
from .git_commit_failed import GitCommitFailed
from .git_commit import GitCommit
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
