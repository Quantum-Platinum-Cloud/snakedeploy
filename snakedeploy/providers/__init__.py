"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .github import GitHubProvider
from snakedeploy.exceptions import UnrecognizedProviderError
from snakedeploy.logger import logger

import re


class ProviderRunner:
    """A snakedeploy provider runner is in charge of determining the provider,
    and then providing entry points to interact with it.
    """

    def deploy(self, source, dest, force=False):
        """The deploy command uses the source url to derive a provider, checks
           that we have a place to clone or deploy to, and executes this request

        Arguments
        =========
        source (str) : the source address of the repository
        dest   (str) : the destination address (should not exist)
        force (bool) : If the directory exists, should it be overwritten?
        """
        provider = self.get_provider(source)
        dest = provider.clone(source, dest, force)
        name = "/".join(source.split("/")[-2:])
        logger.info(
            f"Repository {name} cloned to {dest}. Edit config and sample sheets."
        )

    def get_named_provider(name):
        """get a named provider, meaning determining based on name and not url"""
        if name == "github":
            provider = GitHubProvider()
        else:
            raise UnrecognizedProviderError(name)
        return provider

    def get_provider(self, url=None):
        """get provider will return the correct provider depending on a command (or
        other string) matching a regular expression.
        """
        provider = None
        if matches(GitHubProvider, url):
            provider = GitHubProvider()

        if not provider:
            raise UnrecognizedProviderError(
                f"We can't match a provider for the url {url}."
            )

        return provider


def matches(Executor, url):
    """Given a provider url, determine if it matches the regular expression
    that determines to use a provider or not.
    """
    if not hasattr(Executor, "matchstring"):
        raise NotImplementedError
    return not re.search(Executor.matchstring, url) == None