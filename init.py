from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the power monitor from a config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "threshold_1": entry.data.get("threshold_1", -100),
        "threshold_2": entry.data.get("threshold_2", -200), 
        "threshold_3": entry.data.get("threshold_3", -300)
    }

    async def monitor_power(call):
        power = call.data.get('power')
        if power is None:
            return

        thresholds = hass.data[DOMAIN][entry.entry_id]
        if power >= thresholds["threshold_1"]:
            state = 0
        elif power >= thresholds["threshold_2"]:
            state = 1
        elif power >= thresholds["threshold_3"]:
            state = 2
        else:
            state = 3

        hass.states.async_set('power_monitor.power_state', state)

    hass.services.async_register(DOMAIN, 'monitor_power', monitor_power)
    return True
