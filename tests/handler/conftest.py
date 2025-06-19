# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import os
import sys

# Add the project root to PYTHONPATH
project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../handler'))
sys.path.insert(0, project_root)

# Debugging output
print(f"Added {project_root} to PYTHONPATH")

# Set required environment variables for tests
os.environ["MAIL_FROM"] = "no-reply@univention.test"
os.environ["SMTP_USERNAME"] = "test_user"
os.environ["SMTP_PASSWORD"] = "test_password"
os.environ["SMTP_AUTH_ENABLED"] = "true"
os.environ["NEW_DEVICE_LOGIN_SUBJECT"] = "New device login"
