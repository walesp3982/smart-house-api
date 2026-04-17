"""
Fixtures compartidas para todos los tests de Ollama
Este archivo complementa tests/repository/conftest.py
"""

from unittest.mock import Mock

import pytest

from app.entities.device import DeviceEntity, DeviceType
from app.entities.installed_device import InstalledDeviceWithDevice
from app.services.ollama import OllamaConversationService


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


@pytest.fixture
def ollama_service_with_mocks(
    mock_installed_device_service,
    mock_state_device_service,
    mock_command_device_service,
    mock_track_device_service,
    mock_mqtt_provider,
):
    """OllamaConversationService con todos los mocks"""
    service = OllamaConversationService(
        installed_device_service=mock_installed_device_service,
        state_device_service=mock_state_device_service,
        command_device_service=mock_command_device_service,
        track_device_service=mock_track_device_service,
        mqtt_provider=mock_mqtt_provider,
    )
    return service


@pytest.fixture
def sample_light_device():
    """Dispositivo de luz de prueba"""
    device = DeviceEntity(
        id=1,
        type=DeviceType.LIGHT,
        device_uuid="light-001",
        activation_code="code-light-001",
    )
    installed_device = InstalledDeviceWithDevice(
        id=1,
        name="Luz Sala",
        device_id=1,
        house_id=1,
        area_id=1,
        user_id=1,
        device=device,
    )
    return installed_device


@pytest.fixture
def sample_door_device():
    """Dispositivo de puerta de prueba"""
    device = DeviceEntity(
        id=2,
        type=DeviceType.DOOR,
        device_uuid="door-001",
        activation_code="code-door-001",
    )
    installed_device = InstalledDeviceWithDevice(
        id=2,
        name="Puerta Principal",
        device_id=2,
        house_id=1,
        area_id=1,
        user_id=1,
        device=device,
    )
    return installed_device
