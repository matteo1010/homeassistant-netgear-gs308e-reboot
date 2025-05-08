import requests
import hashlib
import logging
from bs4 import BeautifulSoup
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def get_hidden_input_value(session, url, input_id):
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        hidden_input = soup.find("input", {"type": "hidden", "id": input_id})
        return hidden_input.get("value") if hidden_input else None
    except requests.RequestException as e:
        _LOGGER.error(f"Request error: {e}")
        return None

def merge_strings(str1, str2):
    return "".join(a + b for a, b in zip(str1, str2)) + str1[len(str2):] + str2[len(str1):]

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the switch entity from UI config."""
    ip_address = entry.data["ip_address"]
    password = entry.data["password"]
    async_add_entities([SwitchRebooter(ip_address, password)])

class SwitchRebooter(SwitchEntity):
    """Home Assistant switch to reboot a network switch."""

    def __init__(self, ip_address, password):
        self.ip_address = ip_address
        self.password = password
        self.session = requests.Session()
        self._attr_name = f"Switch Rebooter {ip_address}"
        self._attr_unique_id = f"switch_rebooter_{ip_address}"
        self._is_on = False

    async def async_turn_on(self, **kwargs):
        """Trigger the reboot."""
        await self.hass.async_add_executor_job(self.reboot_switch)

    async def async_turn_off(self, **kwargs):
        """No action needed for turning off."""
        pass

    def reboot_switch(self):
        """Login and send reboot command."""
        rand_value = get_hidden_input_value(self.session, f"http://{self.ip_address}/", "rand")
        if not rand_value:
            _LOGGER.error("Failed to retrieve rand value.")
            return

        hashed_password = hashlib.md5(merge_strings(self.password, rand_value).encode()).hexdigest()
        response = self.session.post(
            f"http://{self.ip_address}/login.cgi",
            data={"password": hashed_password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.ok:
            _LOGGER.info("Login successful!")
        else:
            _LOGGER.error("Login failed.")
            return

        reboot_rand_value = get_hidden_input_value(self.session, f"http://{self.ip_address}/device_reboot.htm", "hash")
        if not reboot_rand_value:
            _LOGGER.error("Failed to retrieve reboot hash value.")
            return

        response = self.session.post(
            f"http://{self.ip_address}/device_reboot.cgi",
            data={"CBox": "on", "hash": reboot_rand_value},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.ok:
            _LOGGER.info("Reboot successful!")
        else:
            _LOGGER.error("Reboot failed.")
