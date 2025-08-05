"""The Home Assistant Custom Tilted Cover integration."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

# Set up logging
_LOGGER = logging.getLogger(__name__)

# Log that the file is being loaded by Python
_LOGGER.info("The __init__.py file for Custom Tilted Cover is being executed.")


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the component. This is a dummy function to satisfy HA if needed."""
    # This will not be used since we have a config flow, but its presence can help.
    _LOGGER.debug("Async_setup called, but integration uses config flow.")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Home Assistant Custom Tilted Cover from a config entry."""
    _LOGGER.info("Setting up config entry for Custom Tilted Cover: %s", entry.title)

    # Store an instance of the entry for the platform to access
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.data

    # Forward the setup to the cover platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    _LOGGER.info("Successfully forwarded setup to platforms for %s", entry.title)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading config entry for Custom Tilted Cover: %s", entry.title)
    
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Remove the config entry from hass.data
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info("Successfully unloaded entry: %s", entry.title)

    return unload_ok
