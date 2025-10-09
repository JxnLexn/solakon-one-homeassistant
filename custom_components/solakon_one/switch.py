"""Switch platform for Solakon ONE integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REGISTERS, SWITCH_DEFINITIONS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solakon ONE switch entities."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    hub = data["hub"]

    device_info = await hub.async_get_device_info()

    entities: list[SolakonSwitch] = []
    for key, definition in SWITCH_DEFINITIONS.items():
        register_key = definition["register"]
        if register_key not in REGISTERS:
            _LOGGER.warning(
                "Skipping switch %s: register %s not defined", key, register_key
            )
            continue

        entities.append(
            SolakonSwitch(
                coordinator=coordinator,
                config_entry=config_entry,
                hub=hub,
                switch_key=key,
                definition=definition,
                device_info=device_info,
            )
        )

    if entities:
        async_add_entities(entities)


class SolakonSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a writable Solakon ONE switch."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        config_entry: ConfigEntry,
        hub,
        switch_key: str,
        definition: dict[str, Any],
        device_info: dict[str, Any],
    ) -> None:
        """Initialize the switch entity."""
        super().__init__(coordinator)
        self._hub = hub
        self._switch_key = switch_key
        self._definition = definition
        self._register_key = definition["register"]
        self._register_config = REGISTERS[self._register_key]
        self._bit = definition["bit"]
        self._attr_unique_id = f"{config_entry.entry_id}_{switch_key}"
        self.entity_id = f"switch.solakon_one_{switch_key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=config_entry.data.get("name", "Solakon ONE"),
            manufacturer=device_info.get("manufacturer", "Solakon"),
            model=device_info.get("model", "One"),
            sw_version=device_info.get("version"),
            serial_number=device_info.get("serial"),
        )

        self._attr_name = definition["name"]
        self._attr_icon = definition.get("icon")

    @property
    def is_on(self) -> bool:
        """Return the switch state."""
        value = self.coordinator.data.get(self._register_key)
        if value is None:
            return False
        return bool(value & (1 << self._bit))

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._write_bit(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._write_bit(False)

    async def _write_bit(self, state: bool) -> None:
        """Write a single bit to the Modbus register."""
        current = self.coordinator.data.get(self._register_key, 0)
        if state:
            new_value = current | (1 << self._bit)
        else:
            new_value = current & ~(1 << self._bit)

        address = self._register_config["address"]
        success = await self._hub.async_write_register(address, new_value)
        if not success:
            raise HomeAssistantError(
                f"Failed to write value {new_value} to register {address}"
            )

        self.coordinator.data[self._register_key] = new_value
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()
