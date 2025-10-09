# Solakon ONE Home Assistant Integration

A complete Home Assistant custom integration for Solakon ONE devices using Modbus TCP communication.

**Extended Version!**

> ⚠️ **IMPORTANT**: This is a Home Assistant **Integration**, not an Add-on. 
> - Do NOT add this as an Add-on repository
> - Install it through HACS as an Integration (see instructions below)

## Features

- Real-time monitoring of all inverter parameters
- PV string monitoring (voltage, current, power)
- Battery management (SOC, SOH, power, temperature)
- Grid import/export tracking
- Energy statistics (daily, monthly, yearly)
- Temperature monitoring
- Alarm and status monitoring
- Remote control hooks (import power limit, remote enable)
- Configurable update intervals
- Full UI configuration support


## Monitored Sensors

### Power Sensors
- PV Power (total from all strings)
- Active Power
- Reactive Power
- Load Power
- Battery Power

### Voltage & Current
- PV1/PV2/PV3/PV4 Voltage & Current
- Grid Phase Voltages (R/S/T)
- Battery Voltage, Current & SOC
- Load Voltage & Current

### Energy Statistics
- Total Energy Generated
- Daily Energy Generation
- Monthly/Yearly Generation
- Battery Charge/Discharge Today
- Grid Import/Export (Today & Total)

### Battery Information
- Battery Power
- Battery Voltage
- Battery Current
- Battery State of Charge
- **Note:** Battery SOH (State of Health) sensor will be available in a future update

### Control Entities
- Remote Control Enable (switch)
- Import Power Limit (number)

### System Information
- Internal Temperature
- Heatsink Temperature
- Power Factor
- Grid Frequency
- System Status
- Alarms

## Installation

### Prerequisites
- Home Assistant 2024.1.0 or newer
- HACS (Home Assistant Community Store) installed
- Your Solakon ONE device connected to your network with Modbus TCP enabled

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on **"Integrations"** (NOT Add-ons!)
3. Click the **three dots menu** in the top right → **"Custom repositories"**
4. Add this repository URL: `https://github.com/solakon-de/solakon-one-homeassistant`
5. Select category: **"Integration"** (⚠️ NOT "Add-on"!)
6. Click **"Add"**
7. Close the custom repositories dialog
8. Click **"+ Explore & Download Repositories"**
9. Search for **"Solakon ONE"** and install it
10. **Restart Home Assistant**
11. Go to **Settings → Devices & Services**
12. Click **"+ Add Integration"**
13. Search for **"Solakon ONE"** and configure it

### Manual Installation

1. Copy the `custom_components/solakon_one` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the integration via Settings → Devices & Services

## Configuration

### Via UI (Recommended)

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Solakon ONE"
4. Enter configuration:
   - **Host**: IP address of your Solakon ONE device
   - **Port**: Modbus TCP port (default: 502)
   - **Device Name**: Friendly name for your device
   - **Modbus Slave ID**: Usually 1 (range: 1-247)
   - **Update Interval**: How often to poll (10-300 seconds)

### Network Requirements

- Ensure your Solakon ONE device is connected to your network
- Modbus TCP must be enabled on the device
- Default Modbus TCP port is 502
- Device must be accessible from Home Assistant

## Troubleshooting

### Connection Issues

1. Verify network connectivity:
   ```bash
   ping <device-ip>
   ```

2. Test Modbus connection:
   ```bash
   telnet <device-ip> 502
   ```

3. Check Home Assistant logs:
   ```
   Settings → System → Logs → Search for "solakon"
   ```

### Common Issues

- **Cannot connect**: Verify IP address and port are correct
- **No data**: Check Modbus slave ID (usually 1)
- **Intermittent data**: Increase update interval if network is slow
- **Missing sensors**: Some sensors only appear if hardware is present (e.g., battery sensors)

## Energy Dashboard Integration

To add Solakon ONE data to your Energy Dashboard:

1. Go to Settings → Dashboards → Energy
2. Configure:
   - **Solar production**: Select "Solakon ONE Daily Energy"
   - **Grid consumption**: Select "Solakon ONE Grid Import Today"
   - **Return to grid**: Select "Solakon ONE Grid Export Today"
   - **Battery**: Select battery charge/discharge sensors

## Automation Examples

### Battery Power Monitoring
```yaml
automation:
  - alias: "Battery Discharging Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.solakon_one_battery_power
        below: -5000  # Alert when discharging more than 5kW
    action:
      - service: notify.mobile_app
        data:
          message: "Battery is discharging at high rate!"
```

### Import Power Limit
```yaml
automation:
  - alias: "Limit grid import during peak hours"
    trigger:
      - platform: time
        at: "17:00:00"
    action:
      - service: number.set_value
        target:
          entity_id: number.solakon_one_import_power_limit
        data:
          value: 5000  # Limit import to 5 kW
```

### Remote Control Enable Toggle
```yaml
automation:
  - alias: "Enable remote control when automation active"
    trigger:
      - platform: state
        entity_id: input_boolean.solakon_automation
        to: "on"
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.solakon_one_remote_control_enable
```


## Services

**Note:** Service functionality is currently under development and will be available in a future update. The following services are planned:

- `solakon_one.refresh_data`: Manually refresh all sensor data (coming soon)
- `solakon_one.set_battery_charge_limit`: Set max battery charge % (coming soon)
- `solakon_one.set_battery_discharge_limit`: Set min battery discharge % (coming soon)
- `solakon_one.set_work_mode`: Change inverter operation mode (coming soon)
- `solakon_one.set_time_of_use`: Configure TOU schedules (coming soon)

## Support

For issues or questions:
- Report issues on [GitHub](https://github.com/solakon-de/solakon-one-homeassistant/issues)

## License

This integration is provided as-is under the MIT License.
