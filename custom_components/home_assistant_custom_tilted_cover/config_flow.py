"""Config flow for Home Assistant Custom Tilted Cover."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector

from .const import (
    CONF_DOWN_SWITCH,
    CONF_TILT_TIME_CLOSE,
    CONF_TILT_TIME_OPEN,
    CONF_TRAVEL_TIME_DOWN,
    CONF_TRAVEL_TIME_UP,
    CONF_UP_SWITCH,
    DEFAULT_TILT_TIME,
    DEFAULT_TRAVEL_TIME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class TiltedCoverConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Home Assistant Custom Tilted Cover."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # You can add validation here if needed
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        # Schema for the user form
        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME): selector.TextSelector(),
                vol.Required(CONF_UP_SWITCH): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch"),
                ),
                vol.Required(CONF_DOWN_SWITCH): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch"),
                ),
                vol.Required(
                    CONF_TRAVEL_TIME_DOWN, default=DEFAULT_TRAVEL_TIME
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=100, step=0.1, mode="box", unit_of_measurement="s"
                    ),
                ),
                vol.Required(
                    CONF_TRAVEL_TIME_UP, default=DEFAULT_TRAVEL_TIME
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=100, step=0.1, mode="box", unit_of_measurement="s"
                    ),
                ),
                vol.Required(
                    CONF_TILT_TIME_OPEN, default=DEFAULT_TILT_TIME
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=10, step=0.1, mode="box", unit_of_measurement="s"
                    ),
                ),
                vol.Required(
                    CONF_TILT_TIME_CLOSE, default=DEFAULT_TILT_TIME
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0, max=10, step=0.1, mode="box", unit_of_measurement="s"
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
