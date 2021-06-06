from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from subprocess import check_call
from sys import exit
from octoprint.util import ResettableTimer
from gpiozero import LED, Button, OutputDevice
import flask

class CaseController(
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin
	):

    leds = dict(
        red_led = 19,
        amber_led = 13,
        green_led = 5
    )

    buttons = dict(
        red_button = 21,
        amber_button = 20,
        green_button = 26
    )

    relay_pin = 17

    print_off_request = False

    #This dictionary holds all of the IO devices of the system by name
    io_devices = dict()

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
        ]


    def get_template_vars(self):
        return dict(shutdowncmd=self.io_devices['relay'].value)


    def on_api_get(self, request):
        self.toggle_printer()

        return flask.jsonify(status="ok")


    def on_after_startup(self):
        #Add the LEDs to the dictionary of operable devices
        for led in self.leds:
            try:
                self.io_devices[led] =  LED(pin = self.leds[led])
            except:
                self._logger.info("Pin {} ({}) is not valid".format(led, self.leds[led]))

        #Add the buttons to the dictionary of operable devices
        for button in self.buttons:
            try:
                self.io_devices[button] =  Button(pin=self.buttons[button], hold_time = 5)
            except:
                self._logger.info("Pin {} ({}) is not valid".format(button, self.buttons[button]))

        #Add the relay to the dictionary of operable devices and turn it on
        try:
            self.io_devices['relay'] = OutputDevice(pin = self.relay_pin, initial_value = True)
            self._logger.info("Printer ON")
        except:
            self._logger.info("Relay pin {} is not valid".format(relay_pin))

            #Stop the script here if the relay pin is invalid
            raise RunTimeError

        #Assign function calls to the red power button
        try:
            self.io_devices['red_button'].when_held = self.shutdown

            self.io_devices['red_led'].on()
        except:
            self._logger.info("Power button assignment failed")

        #Assign functionality to the 2nd button (amber)
        try:
            self.io_devices['amber_button'].when_pressed = self.toggle_printer

            self.io_devices['amber_led'].on()
        except:
            self._logger.info("Printer power button assignment failed")

        #Assign functionality to the 3rd button (green)
        try:
            #TODO assign this button to a fucntion
            self.io_devices['green_button'].when_pressed = self.io_devices['green_led'].toggle
        except:
            self._logger.info("Green button functional assignment failed")

        self._logger.info("IO configured")

        #Attempt autoconnect to printer
        self._printer.connect()


    def poll(self):
        #Evaluate if printer shutdown is safe or not
        temps = self._printer.get_current_temperatures()
        self._logger.info("Temp= {}".format(temps['tool0']['actual']))

        if temps['tool0']['actual'] < 50:
            self._pollster.cancel()
            self._printer.disconnect()

            self.io_devices['relay'].off()

            self._logger.info("Relay OFF")

            if 'amber_led' in self.io_devices:
                self.io_devices['amber_led'].off()

        #Start the polling process until the hotend has cooled if deemed not safe
        else:
            self._logger.info("Temperature is too high")

            self._pollster.reset()
            self._pollster = ResettableTimer(interval = 10.0, function = self.poll)
            self._pollster.start()

            self.io_devices['amber_led'].on()
            self.io_devices['amber_led'].blink(on_time = 0.5, off_time = 0.5, n = 9)


    def toggle_printer(self):
        if self.io_devices['relay'].value:
            self._logger.info("Attempting to turn printer off...")

            #If printer is not connected, do nothing
            if self._printer.get_current_connection()[0] == "Closed":
                self._logger.info("Printer is not connected")

            #TODO Finish this
            #If printer is printing, make or cancel a shutdown request
            elif self._printer.is_printing():
                if print_off_request:
                    print_off_request = False
                    self._logger.info("Printer shutdown request cancelled")
                else:
                    print_off_request = True
                    self._logger.info("Printer shutdown request made")

            else:
                self._logger.info("Timer started...")
                self.io_devices['amber_led'].off()
                try:
                    self._pollster.reset()
                except AttributeError:
                    pass

                self._pollster = ResettableTimer(interval = 1.0, function = self.poll)
                self._pollster.start()

        else:
            if 'amber_led' in self.io_devices:
                self.io_devices['amber_led'].on()

            self.io_devices['relay'].on()

            #Attempt autoconnect to printer
            self._printer.connect()


    def shutdown(self):
        #If the relay is on hault shutdown
        if not self.io_devices['relay'].value:
            self.io_devices['red_led'].off()
            self._logger.info("Initiating shutdown...")
            self._printer.disconnect()

            check_call(["sudo", "shutdown", "now"])
        else:
            self._logger.info("Printer relay is on, aborting system shutdown")

    #TODO add settings customization
    #Variable pin assignments
    #Duration between temperature polls
    #Cutoff temperature
    #Autoconnect on relay powerup

    def __init__(self):
        self._pollster = None

__plugin_name__ = "Case Control"
__plugin_pythoncompat__ = ">=3, <4"
__plugin_implementation__ = CaseController()
