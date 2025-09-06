"""Modbus communication for Solakon ONE."""
from __future__ import annotations

import asyncio
import logging
import struct
from typing import Any

from homeassistant.components.modbus import modbus
from homeassistant.core import HomeAssistant

from .const import REGISTERS

_LOGGER = logging.getLogger(__name__)


class SolakonModbusHub:
    """Modbus hub for Solakon ONE device."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        slave_id: int,
        scan_interval: int,
    ) -> None:
        """Initialize the Modbus hub."""
        self._hass = hass
        self._host = host
        self._port = port
        self._slave_id = slave_id
        self.scan_interval = scan_interval
        self._client = None
        self._lock = asyncio.Lock()

    async def async_setup(self) -> None:
        """Set up the Modbus connection."""
        # Use Home Assistant's built-in modbus component
        self._client = await modbus.async_get_client(
            self._hass,
            name=f"solakon_{self._host}",
            host=self._host,
            port=self._port,
            type="tcp",
        )

    async def async_close(self) -> None:
        """Close the Modbus connection."""
        if self._client:
            self._client.close()

    async def async_test_connection(self) -> bool:
        """Test the Modbus connection."""
        try:
            result = await self._async_read_holding_registers(30000, 1)
            return result is not None
        except Exception as err:
            _LOGGER.error("Connection test failed: %s", err)
            return False

    async def async_get_device_info(self) -> dict[str, Any]:
        """Get device information."""
        info = {}
        try:
            # Read model name
            model_data = await self._async_read_holding_registers(
                REGISTERS["model_name"]["address"],
                REGISTERS["model_name"]["length"]
            )
            if model_data:
                info["model"] = self._parse_string(model_data)

            # Read serial number
            serial_data = await self._async_read_holding_registers(
                REGISTERS["serial_number"]["address"],
                REGISTERS["serial_number"]["length"]
            )
            if serial_data:
                info["serial"] = self._parse_string(serial_data)

            # Read manufacturer ID
            mfg_data = await self._async_read_holding_registers(
                REGISTERS["mfg_id"]["address"],
                REGISTERS["mfg_id"]["length"]
            )
            if mfg_data:
                info["manufacturer"] = self._parse_string(mfg_data)

        except Exception as err:
            _LOGGER.error("Failed to get device info: %s", err)

        return info

    async def async_read_all_data(self) -> dict[str, Any]:
        """Read all data from the device."""
        data = {}
        
        async with self._lock:
            for key, register in REGISTERS.items():
                try:
                    value = await self._async_read_register(register)
                    if value is not None:
                        data[key] = value
                except Exception as err:
                    _LOGGER.debug("Failed to read %s: %s", key, err)
                    data[key] = None

        return data

    async def _async_read_register(self, register: dict) -> Any:
        """Read a single register."""
        try:
            raw_data = await self._async_read_holding_registers(
                register["address"],
                register["length"]
            )
            
            if raw_data is None:
                return None

            return self._parse_register_value(raw_data, register)
        except Exception as err:
            _LOGGER.debug("Error reading register %s: %s", register["address"], err)
            return None

    async def _async_read_holding_registers(self, address: int, count: int) -> list[int] | None:
        """Read holding registers from the device."""
        if not self._client:
            return None

        try:
            result = await self._hass.async_add_executor_job(
                self._client.read_holding_registers,
                address,
                count,
                self._slave_id
            )
            
            if result.isError():
                _LOGGER.debug("Modbus error reading address %s: %s", address, result)
                return None
                
            return result.registers
        except Exception as err:
            _LOGGER.debug("Exception reading address %s: %s", address, err)
            return None

    def _parse_register_value(self, data: list[int], register: dict) -> Any:
        """Parse register value based on type."""
        reg_type = register.get("type", "u16")
        
        try:
            if reg_type == "string":
                return self._parse_string(data)
            elif reg_type == "u16":
                value = data[0]
            elif reg_type == "i16":
                value = self._to_signed16(data[0])
            elif reg_type == "u32":
                value = (data[0] << 16) | data[1]
            elif reg_type == "i32":
                value = self._to_signed32((data[0] << 16) | data[1])
            elif reg_type == "bitfield16":
                return self._parse_bitfield16(data[0])
            else:
                value = data[0] if len(data) == 1 else data

            # Apply scaling if defined
            if "scale" in register:
                value = value / register["scale"]

            return value
        except Exception as err:
            _LOGGER.debug("Error parsing register value: %s", err)
            return None

    def _parse_string(self, data: list[int]) -> str:
        """Parse string from register data."""
        chars = []
        for value in data:
            chars.append(chr((value >> 8) & 0xFF))
            chars.append(chr(value & 0xFF))
        return "".join(chars).rstrip("\x00")

    def _to_signed16(self, value: int) -> int:
        """Convert unsigned 16-bit to signed."""
        if value > 0x7FFF:
            return value - 0x10000
        return value

    def _to_signed32(self, value: int) -> int:
        """Convert unsigned 32-bit to signed."""
        if value > 0x7FFFFFFF:
            return value - 0x100000000
        return value

    def _parse_bitfield16(self, value: int) -> dict:
        """Parse 16-bit bitfield."""
        bits = {}
        for i in range(16):
            bits[f"bit{i}"] = bool(value & (1 << i))
        
        # Parse specific status bits if this is status_1
        if value & 0x01:
            bits["standby"] = True
        if value & 0x04:
            bits["operation"] = True
        if value & 0x40:
            bits["fault"] = True
            
        return bits

    async def async_write_register(self, address: int, value: int) -> bool:
        """Write a single register."""
        if not self._client:
            return False

        try:
            result = await self._hass.async_add_executor_job(
                self._client.write_register,
                address,
                value,
                self._slave_id
            )
            return not result.isError()
        except Exception as err:
            _LOGGER.error("Error writing register %s: %s", address, err)
            return False

    async def async_write_registers(self, address: int, values: list[int]) -> bool:
        """Write multiple registers."""
        if not self._client:
            return False

        try:
            result = await self._hass.async_add_executor_job(
                self._client.write_registers,
                address,
                values,
                self._slave_id
            )
            return not result.isError()
        except Exception as err:
            _LOGGER.error("Error writing registers %s: %s", address, err)
            return False