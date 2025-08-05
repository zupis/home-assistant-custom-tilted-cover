"""Cover platform for the Home Assistant Custom Tilted Cover integration."""
import asyncio
import logging
from typing import Any

from homeassistant.components.cover import (
    ATTR_POSITION,
    ATTR_TILT_POSITION,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_DOWN_SWITCH,
    CONF_TILT_TIME_CLOSE,
    CONF_TILT_TIME_OPEN,
    CONF_TRAVEL_TIME_DOWN,
    CONF_TRAVEL_TIME_UP,
    CONF_UP_SWITCH,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Tilted Cover from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([CustomTiltedCover(hass, config_entry.entry_id, config)])


class CustomTiltedCover(CoverEntity):
    """Representation of a Tilted Cover."""

    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant, unique_id: str, config: dict) -> None:
        """Initialize the cover."""
        self.hass = hass
        self._attr_unique_id = unique_id
        self._attr_name = config[CONF_NAME]
        self._up_switch_entity_id = config[CONF_UP_SWITCH]
        self._down_switch_entity_id = config[CONF_DOWN_SWITCH]
        self._travel_time_up = config[CONF_TRAVEL_TIME_UP]
        self._travel_time_down = config[CONF_TRAVEL_TIME_DOWN]
        self._tilt_time_open = config[CONF_TILT_TIME_OPEN]
        self._tilt_time_close = config[CONF_TILT_TIME_CLOSE]

        self._attr_is_closed = True
        self._attr_is_closing = False
        self._attr_is_opening = False
        self._attr_current_cover_tilt_position = 0 # 0 = closed, 100 = open
        self._attr_current_cover_position = 0 # 0 = closed, 100 = open

        self._attr_supported_features = (
            CoverEntityFeature.OPEN
            | CoverEntityFeature.CLOSE
            | CoverEntityFeature.STOP
            | CoverEntityFeature.OPEN_TILT
            | CoverEntityFeature.CLOSE_TILT
        )
        # To support SET_POSITION and SET_TILT_POSITION, you would need
        # to implement position tracking logic.
        # self._attr_supported_features |= (
        #     CoverEntityFeature.SET_POSITION | CoverEntityFeature.SET_TILT_POSITION
        # )

        self._movement_task = None

    async def _async_timed_movement(self, switch_entity_id: str, duration: float):
        """Start a timed movement and update state."""
        try:
            # Turn on the switch
            await self._async_call_switch_service(SERVICE_TURN_ON, switch_entity_id)
            # Wait for the specified duration
            await asyncio.sleep(duration)
        except asyncio.CancelledError:
            _LOGGER.debug("Movement was cancelled")
        finally:
            # Always ensure the switch is turned off
            await self._async_call_switch_service(SERVICE_TURN_OFF, switch_entity_id)
            self._movement_task = None
            self._attr_is_opening = False
            self._attr_is_closing = False
            self.async_write_ha_state()


    async def _async_call_switch_service(self, service: str, entity_id: str):
        """Call a service on a switch entity."""
        await self.hass.services.async_call(
            "switch",
            service,
            {"entity_id": entity_id},
            blocking=True,
        )

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        if self._movement_task:
            self._movement_task.cancel()

        self._attr_is_opening = True
        self.async_write_ha_state()

        self._movement_task = self.hass.async_create_task(
            self._async_timed_movement(self._up_switch_entity_id, self._travel_time_up)
        )
        await self._movement_task

        self._attr_is_closed = False
        self._attr_current_cover_position = 100
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        if self._movement_task:
            self._movement_task.cancel()

        self._attr_is_closing = True
        self.async_write_ha_state()

        self._movement_task = self.hass.async_create_task(
            self._async_timed_movement(self._down_switch_entity_id, self._travel_time_down)
        )
        await self._movement_task

        self._attr_is_closed = True
        self._attr_current_cover_position = 0
        self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Stop the cover movement."""
        if self._movement_task:
            self._movement_task.cancel()
            self._movement_task = None

        self._attr_is_opening = False
        self._attr_is_closing = False
        # Here you would need to calculate the new position based on elapsed time
        # For simplicity, we just stop the motors.
        await self._async_call_switch_service(SERVICE_TURN_OFF, self._up_switch_entity_id)
        await self._async_call_switch_service(SERVICE_TURN_OFF, self._down_switch_entity_id)
        self.async_write_ha_state()

    async def async_open_tilt(self, **kwargs: Any) -> None:
        """Open the cover tilt."""
        if self._movement_task:
            self._movement_task.cancel()

        self._movement_task = self.hass.async_create_task(
            self._async_timed_movement(self._up_switch_entity_id, self._tilt_time_open)
        )
        await self._movement_task

        self._attr_current_cover_tilt_position = 100
        self.async_write_ha_state()

    async def async_close_tilt(self, **kwargs: Any) -> None:
        """Close the cover tilt."""
        if self._movement_task:
            self._movement_task.cancel()

        self._movement_task = self.hass.async_create_task(
            self._async_timed_movement(self._down_switch_entity_id, self._tilt_time_close)
        )
        await self._movement_task

        self._attr_current_cover_tilt_position = 0
        self.async_write_ha_state()
