# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from models.device import Device
from modules.notifier import Notifier


@pytest.fixture
def keycloak_mock():
    mock = MagicMock()
    mock.get_user_email.return_value = "test@example.com"
    return mock


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def device():
    device = Device(
        keycloak_device_id="device123",
        fingerprint_device_id="fingerprint123",
        user_id="user123",
        is_notified=False,
    )
    device.created_at = datetime(2024, 5, 20, 12, 0, 0, tzinfo=timezone.utc)
    return device


@pytest.mark.parametrize("timezone,valid,expected_hour", [
    ("UTC", True, 12),  # Default timezone
    ("Europe/Berlin", True, 14),  # UTC+2 in summer
    ("Asia/Tokyo", True, 21),  # UTC+9
    ("Etc/GMT+2", True, 10),  # UTC-2
    ("Africa/Nairobi", True, 15),  # UTC+3
    ("InvalidZone", False, 12),  # Invalid timezone should fallback to UTC
])
@patch("modules.notifier.mail.Email")
@patch("modules.notifier.session", new_callable=MagicMock)
def test_notify_new_logins_timezones(mock_session, mock_email_class, device, timezone, valid, expected_hour, keycloak_mock):
    # Set ENV variable for timezone
    os.environ["EMAIL_TIMEZONE"] = timezone

    mock_email_instance = MagicMock()
    mock_email_class.return_value = mock_email_instance

    # Mock database query
    mock_session.query.return_value.filter.return_value.all.return_value = [
        device]

    # Create Notifier instance
    notifier = Notifier(keycloak_mock)
    notifier.notify_new_logins()

    # Verify that Email was created with the correct details
    mock_email_class.assert_called_once()
    args, _ = mock_email_class.call_args

    # First argument should be the email address
    assert args[0] == "test@example.com"

    # Second argument should be the details dict
    details = args[1]
    assert "Time" in details

    # Check for correct timezone name
    expected_timezone = timezone if valid else "UTC"
    # Check for correct hour based on timezone
    expected_time = f"2024-05-20 {expected_hour}:00:00 ({expected_timezone})"
    assert details["Time"] == expected_time

    assert "Device ID" in details
    assert details["Device ID"] == "device123"
    assert "Fingerprint" in details
    assert details["Fingerprint"] == "fingerprint123"

    # Verify that send was called
    mock_email_instance.send.assert_called_once()
