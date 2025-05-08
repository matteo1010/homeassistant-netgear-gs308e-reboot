# Switch Rebooter GS308E

This Home Assistant custom component allows you to reboot a Netgear GS308E network switch.

## Installation

1.  Copy the `switch_rebootergs308e` directory to your `<config>/custom_components` directory.
2.  Restart Home Assistant.
3.  Configure the integration via the Home Assistant UI, by going to "Configuration" -> "Integrations" and searching for "Switch Rebooter GS308E".

## Configuration

The following parameters need to be configured through the Home Assistant UI:

-   **IP Address:** The IP address of your Netgear GS308E switch.
-   **Password:** The password to access your Netgear GS308E switch.

## Usage

Once configured, a switch entity will be created in Home Assistant.  You can toggle this switch to reboot the network switch.  

**Note:** Turning the switch "off" in Home Assistant does not perform any action.  It is only the "on" action that triggers a reboot.

## Requirements

-   `requests`
-   `beautifulsoup4`

These dependencies will be automatically installed by Home Assistant.

## Limitations

-   This component is specifically designed for the Netgear GS308E switch. It may not work with other switch models.
-   The component relies on the web interface of the switch. Changes to the switch's firmware or web interface may break the component.

## Credits

This component was developed to provide a convenient way to reboot the Netgear GS308E switch from Home Assistant.