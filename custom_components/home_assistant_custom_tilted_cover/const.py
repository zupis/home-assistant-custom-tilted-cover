"""Constants for the Home Assistant Custom Tilted Cover integration."""

# Domain for the integration
DOMAIN = "home_assistant_custom_tilted_cover"

# Platforms to be set up
PLATFORMS = ["cover"]

# Configuration keys
CONF_NAME = "name"
CONF_UP_SWITCH = "up_switch_entity_id"
CONF_DOWN_SWITCH = "down_switch_entity_id"
CONF_TRAVEL_TIME_UP = "travel_time_up"
CONF_TRAVEL_TIME_DOWN = "travel_time_down"
CONF_TILT_TIME_OPEN = "tilt_time_open"
CONF_TILT_TIME_CLOSE = "tilt_time_close"

# Default values
DEFAULT_TRAVEL_TIME = 25
DEFAULT_TILT_TIME = 1.5
