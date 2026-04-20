"""
Fixtures compartidas para todos los tests de Ollama
Este archivo complementa tests/repository/conftest.py
"""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_installed_device_service():
    """Mock del servicio InstalledDeviceService"""
    service = Mock()
    return service


@pytest.fixture
def mock_state_device_service():
    """Mock del servicio StateDeviceService"""
    service = Mock()
    return service


@pytest.fixture
def mock_command_device_service():
    """Mock del servicio CommandDeviceService"""
    service = Mock()
    return service


@pytest.fixture
def mock_track_device_service():
    """Mock del servicio TrackDeviceService"""
    service = Mock()
    return service


@pytest.fixture
def mock_mqtt_provider():
    """Mock del proveedor MQTT"""
    provider = Mock()
    provider.publish = Mock(return_value=None)
    provider.get_topic = Mock(return_value=None)
    return provider
