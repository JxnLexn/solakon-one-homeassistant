"""Number platform for Solakon ONE integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NUMBER_DEFINITIONS, REGISTERS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solakon ONE number entities."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    hub = data["hub"]

    device_info = await hub.async_get_device_info()

    entities: list[SolakonNumber] = []
    for key, definition in NUMBER_DEFINITIONS.items():
        register_key = definition["register"]
        if register_key not in REGISTERS:
            _LOGGER.warning(
                "Skipping number %s: register %s not defined", key, register_key
            )
            continue

        entities.append(
            SolakonNumber(
                coordinator=coordinator,
                config_entry=config_entry,
                hub=hub,
                number_key=key,
                definition=definition,
                device_info=device_info,
            )
        )

    if entities:
        async_add_entities(entities)


class SolakonNumber(CoordinatorEntity, NumberEntity):
    """Representation of a writable Solakon ONE value."""

    _attr_has_entity_name = True
    _attr_mode = NumberMode.AUTO

    def __init__(
        self,
        coordinator,
        config_entry: ConfigEntry,
        hub,
        number_key: str,
        definition: dict[str, Any],
        device_info: dict[str, Any],
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._hub = hub
        self._number_key = number_key
        self._definition = definition
        self._register_key = definition["register"]
        self._register_config = REGISTERS[self._register_key]
        self._attr_unique_id = f"{config_entry.entry_id}_{number_key}"
        self.entity_id = f"number.solakon_one_{number_key}"

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
        self._attr_native_unit_of_measurement = definition.get("unit")
        if (min_value := definition.get("min")) is not None:
            self._attr_native_min_value = min_value
        if (max_value := definition.get("max")) is not None:
            self._attr_native_max_value = max_value
        if (step := definition.get("step")) is not None:
            self._attr_native_step = step

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        value = self.coordinator.data.get(self._register_key)
        if value is None:
            return None
        return float(value)

    async def async_set_native_value(self, value: float) -> None:
        """Set a new value."""
        step = self._attr_native_step or 1
        int_value = int(round(value / step) * step)

        min_value = self._attr_native_min_value
        max_value = self._attr_native_max_value
        if min_value is not None:
            int_value = max(int_value, int(min_value))
        if max_value is not None:
            int_value = min(int_value, int(max_value))

        address = self._register_config["address"]
        count = self._register_config.get("count", 1)

        if count == 1:
            success = await self._hub.async_write_register(address, int_value)
        else:
            registers = self._value_to_registers(int_value, count)
            success = await self._hub.async_write_registers(address, registers)

        if not success:
            raise HomeAssistantError(
                f"Failed to write value {int_value} to register {address}"
            )

        # Optimistically update and refresh
        self.coordinator.data[self._register_key] = int_value
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    @staticmethod
    def _value_to_registers(value: int, register_count: int) -> list[int]:
        """Convert integer value to Modbus register payload."""
        if register_count == 1:
            return [value & 0xFFFF]

        if register_count == 2:
            if value < 0:
                value = (1 << 32) + value
            high = (value >> 16) & 0xFFFF
            low = value & 0xFFFF
            return [high, low]

        raise ValueError(f"Unsupported register count: {register_count}")
