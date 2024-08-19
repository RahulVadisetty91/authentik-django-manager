#!/usr/bin/env python
"""Django manage.py script."""

import os
import sys
import warnings

from authentik.lib.config import CONFIG
from cryptography.hazmat.backends.openssl.backend import backend
from defusedxml import defuse_stdlib
from django.utils.autoreload import DJANGO_AUTORELOAD_ENV

from lifecycle.migrate import run_migrations
from lifecycle.wait_for_db import wait_for_db

# Suppress specific warnings
warnings.filterwarnings("ignore", "SelectableGroups dict interface")
warnings.filterwarnings(
    "ignore",
    "defusedxml.lxml is no longer supported and will be removed in a future release."
)
warnings.filterwarnings(
    "ignore",
    "defusedxml.cElementTree is deprecated, import from defusedxml.ElementTree instead."
)

# Defuse standard library XML modules to avoid security issues
defuse_stdlib()

if CONFIG.get_bool("compliance.fips.enabled", False):
    backend._enable_fips()

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authentik.root.settings")
    
    wait_for_db()
    
    if (
        len(sys.argv) > 1
        and sys.argv[1] in ["dev_server", "worker", "bootstrap_tasks"]
        and os.environ.get(DJANGO_AUTORELOAD_ENV) is None
    ):
        run_migrations()
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
