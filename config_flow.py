import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from .const import DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("ip_address"): cv.string,
        vol.Required("password"): cv.string,
    }
)

class SwitchRebooterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Switch Rebooter."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=f"Switch Rebooter {user_input['ip_address']}", data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
