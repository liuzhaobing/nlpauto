#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
from utils.handler import Handlers
from conf.env import *


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nlpauto.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def pre():
    Handlers.make_parent_dirs(LOG_PATH)
    Handlers.make_parent_dirs(UPLOAD_PATH)
    Handlers.make_parent_dirs(TEXT_AGGREGATION_PATH)
    Handlers.make_parent_dirs(TEST_SDK_ENTITY_PATH)
    Handlers.make_parent_dirs(SKILL_BADCASE_AUTO_PULL_PATH)


if __name__ == '__main__':
    pre()
    main()
