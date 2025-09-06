"""Constants for the Solakon ONE integration."""
from typing import Final

DOMAIN: Final = "solakon_one"
DEFAULT_NAME: Final = "Solakon ONE"
DEFAULT_PORT: Final = 502
DEFAULT_SLAVE_ID: Final = 1
DEFAULT_SCAN_INTERVAL: Final = 30
SCAN_INTERVAL: Final = 30

# Register definitions
REGISTERS = {
    # Model Information (Table 3-1)
    "model_name": {"address": 30000, "length": 16, "type": "string"},
    "serial_number": {"address": 30016, "length": 16, "type": "string"},
    "mfg_id": {"address": 30032, "length": 16, "type": "string"},
    
    # Version Information (Table 3-2)
    "master_version": {"address": 36001, "length": 1, "type": "u16"},
    "slave_version": {"address": 36002, "length": 1, "type": "u16"},
    "manager_version": {"address": 36003, "length": 1, "type": "u16"},
    
    # Protocol & Device Info (Table 3-5)
    "protocol_version": {"address": 39000, "length": 2, "type": "u32"},
    "rated_power": {"address": 39053, "length": 2, "type": "i32", "scale": 1000, "unit": "kW"},
    "max_active_power": {"address": 39055, "length": 2, "type": "i32", "scale": 1000, "unit": "kW"},
    
    # Status
    "status_1": {"address": 39063, "length": 1, "type": "bitfield16"},
    "alarm_1": {"address": 39067, "length": 1, "type": "bitfield16"},
    "alarm_2": {"address": 39068, "length": 1, "type": "bitfield16"},
    "alarm_3": {"address": 39069, "length": 1, "type": "bitfield16"},
    
    # PV Input
    "pv1_voltage": {"address": 39070, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "pv1_current": {"address": 39071, "length": 1, "type": "i16", "scale": 100, "unit": "A"},
    "pv2_voltage": {"address": 39072, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "pv2_current": {"address": 39073, "length": 1, "type": "i16", "scale": 100, "unit": "A"},
    "pv3_voltage": {"address": 39074, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "pv3_current": {"address": 39075, "length": 1, "type": "i16", "scale": 100, "unit": "A"},
    "pv4_voltage": {"address": 39076, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "pv4_current": {"address": 39077, "length": 1, "type": "i16", "scale": 100, "unit": "A"},
    "total_pv_power": {"address": 39118, "length": 2, "type": "i32", "scale": 1000, "unit": "kW"},
    
    # Grid Information
    "grid_r_voltage": {"address": 39123, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "grid_s_voltage": {"address": 39124, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "grid_t_voltage": {"address": 39125, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "grid_r_current": {"address": 39126, "length": 1, "type": "i16", "scale": 100, "unit": "A"},
    "grid_s_current": {"address": 39127, "length": 1, "type": "i16", "scale": 100, "unit": "A"},
    "grid_t_current": {"address": 39128, "length": 1, "type": "i16", "scale": 100, "unit": "A"},
    "active_power": {"address": 39134, "length": 2, "type": "i32", "scale": 1000, "unit": "kW"},
    "reactive_power": {"address": 39136, "length": 2, "type": "i32", "scale": 1000, "unit": "kVar"},
    "power_factor": {"address": 39138, "length": 1, "type": "i16", "scale": 1000},
    "grid_frequency": {"address": 39139, "length": 1, "type": "i16", "scale": 100, "unit": "Hz"},
    
    # Temperature
    "internal_temp": {"address": 39141, "length": 1, "type": "i16", "scale": 10, "unit": "°C"},
    "heatsink_temp": {"address": 39142, "length": 1, "type": "i16", "scale": 10, "unit": "°C"},
    
    # Energy Statistics
    "cumulative_generation": {"address": 39149, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    "daily_generation": {"address": 39151, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    "monthly_generation": {"address": 39153, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    "yearly_generation": {"address": 39155, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    
    # Battery Information
    "battery1_voltage": {"address": 39227, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "battery1_current": {"address": 39228, "length": 2, "type": "i32", "scale": 1000, "unit": "A"},
    "battery1_power": {"address": 39230, "length": 2, "type": "i32", "scale": 1, "unit": "W"},
    "battery1_soc": {"address": 39232, "length": 1, "type": "u16", "scale": 1, "unit": "%"},
    "battery1_soh": {"address": 39233, "length": 1, "type": "u16", "scale": 1, "unit": "%"},
    "battery1_temp": {"address": 39234, "length": 1, "type": "i16", "scale": 10, "unit": "°C"},
    "battery_combined_power": {"address": 39237, "length": 2, "type": "i32", "scale": 1, "unit": "W"},
    "battery_charge_today": {"address": 39239, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    "battery_discharge_today": {"address": 39241, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    
    # Load/Consumption
    "load_power": {"address": 39263, "length": 2, "type": "i32", "scale": 1, "unit": "W"},
    "load_voltage": {"address": 39265, "length": 1, "type": "i16", "scale": 10, "unit": "V"},
    "load_current": {"address": 39266, "length": 1, "type": "i16", "scale": 100, "unit": "A"},
    
    # Grid Import/Export
    "grid_import_today": {"address": 39279, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    "grid_export_today": {"address": 39281, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    "grid_import_total": {"address": 39283, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
    "grid_export_total": {"address": 39285, "length": 2, "type": "u32", "scale": 100, "unit": "kWh"},
}

# Sensor definitions for Home Assistant
SENSOR_DEFINITIONS = {
    # Power sensors
    "total_pv_power": {
        "name": "PV Power",
        "device_class": "power",
        "state_class": "measurement",
        "unit": "kW",
        "icon": "mdi:solar-power",
    },
    "active_power": {
        "name": "Active Power",
        "device_class": "power",
        "state_class": "measurement",
        "unit": "kW",
        "icon": "mdi:flash",
    },
    "reactive_power": {
        "name": "Reactive Power",
        "device_class": "reactive_power",
        "state_class": "measurement",
        "unit": "kVar",
        "icon": "mdi:flash-outline",
    },
    "load_power": {
        "name": "Load Power",
        "device_class": "power",
        "state_class": "measurement",
        "unit": "W",
        "icon": "mdi:home-lightning-bolt",
    },
    "battery_combined_power": {
        "name": "Battery Power",
        "device_class": "power",
        "state_class": "measurement",
        "unit": "W",
        "icon": "mdi:battery-charging",
    },
    
    # Voltage sensors
    "pv1_voltage": {
        "name": "PV1 Voltage",
        "device_class": "voltage",
        "state_class": "measurement",
        "unit": "V",
        "icon": "mdi:flash",
    },
    "pv2_voltage": {
        "name": "PV2 Voltage",
        "device_class": "voltage",
        "state_class": "measurement",
        "unit": "V",
        "icon": "mdi:flash",
    },
    "grid_r_voltage": {
        "name": "Grid R Voltage",
        "device_class": "voltage",
        "state_class": "measurement",
        "unit": "V",
        "icon": "mdi:sine-wave",
    },
    "battery1_voltage": {
        "name": "Battery Voltage",
        "device_class": "voltage",
        "state_class": "measurement",
        "unit": "V",
        "icon": "mdi:battery",
    },
    
    # Current sensors
    "pv1_current": {
        "name": "PV1 Current",
        "device_class": "current",
        "state_class": "measurement",
        "unit": "A",
        "icon": "mdi:current-dc",
    },
    "pv2_current": {
        "name": "PV2 Current",
        "device_class": "current",
        "state_class": "measurement",
        "unit": "A",
        "icon": "mdi:current-dc",
    },
    "battery1_current": {
        "name": "Battery Current",
        "device_class": "current",
        "state_class": "measurement",
        "unit": "A",
        "icon": "mdi:current-dc",
    },
    
    # Energy sensors
    "cumulative_generation": {
        "name": "Total Energy",
        "device_class": "energy",
        "state_class": "total_increasing",
        "unit": "kWh",
        "icon": "mdi:solar-panel",
    },
    "daily_generation": {
        "name": "Daily Energy",
        "device_class": "energy",
        "state_class": "total_increasing",
        "unit": "kWh",
        "icon": "mdi:solar-panel",
    },
    "battery_charge_today": {
        "name": "Battery Charge Today",
        "device_class": "energy",
        "state_class": "total_increasing",
        "unit": "kWh",
        "icon": "mdi:battery-charging",
    },
    "battery_discharge_today": {
        "name": "Battery Discharge Today",
        "device_class": "energy",
        "state_class": "total_increasing",
        "unit": "kWh",
        "icon": "mdi:battery-minus",
    },
    "grid_import_today": {
        "name": "Grid Import Today",
        "device_class": "energy",
        "state_class": "total_increasing",
        "unit": "kWh",
        "icon": "mdi:transmission-tower-import",
    },
    "grid_export_today": {
        "name": "Grid Export Today",
        "device_class": "energy",
        "state_class": "total_increasing",
        "unit": "kWh",
        "icon": "mdi:transmission-tower-export",
    },
    
    # Temperature sensors
    "internal_temp": {
        "name": "Internal Temperature",
        "device_class": "temperature",
        "state_class": "measurement",
        "unit": "°C",
        "icon": "mdi:thermometer",
    },
    "battery1_temp": {
        "name": "Battery Temperature",
        "device_class": "temperature",
        "state_class": "measurement",
        "unit": "°C",
        "icon": "mdi:thermometer",
    },
    
    # Battery status
    "battery1_soc": {
        "name": "Battery SOC",
        "device_class": "battery",
        "state_class": "measurement",
        "unit": "%",
        "icon": "mdi:battery",
    },
    "battery1_soh": {
        "name": "Battery SOH",
        "state_class": "measurement",
        "unit": "%",
        "icon": "mdi:battery-heart",
    },
    
    # Other sensors
    "power_factor": {
        "name": "Power Factor",
        "device_class": "power_factor",
        "state_class": "measurement",
        "icon": "mdi:angle-acute",
    },
    "grid_frequency": {
        "name": "Grid Frequency",
        "device_class": "frequency",
        "state_class": "measurement",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
    },
}