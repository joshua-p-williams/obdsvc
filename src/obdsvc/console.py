import click
import time

from . import __version__
from . import automobile
from . import redispub

@click.command()

@click.option('--port', default=None, help='The UNIX device file or Windows COM Port for your adapter. The default value (None) will auto select a port.')
@click.option('--baudrate', default=None, help='The baudrate at which to set the serial connection. This can vary from adapter to adapter. Typical values are: 9600, 38400, 19200, 57600, 115200. The default value (None) will auto select a baudrate.')
@click.option('--protocol', default=None, help='Force the protocol to use. The default value (None) will auto select a protocol. 1 = SAE J1850 PWM, 2 = SAE J1850 VPW, 3 = AUTO, ISO 9141-2, 4 = ISO 14230-4 (KWP 5BAUD), 5 = ISO 14230-4 (KWP FAST), 6 = ISO 15765-4 (CAN 11/500), 7 = ISO 15765-4 (CAN 29/500), 8 = ISO 15765-4 (CAN 11/250), 9 = ISO 15765-4 (CAN 29/250), A = SAE J1939 (CAN 29/250)')
@click.option('--fast', default=True, help='Allows commands to be optimized before being sent to the car. Disabling fast mode will guarantee that python-OBD outputs the unaltered command for every request.')
@click.option('--timeout', default=0.1, help='Specifies the connection timeout in seconds.')
@click.option('--checkvoltage', default=True, help='Optional argument that is True by default and when set to False disables the detection of the car supply voltage on OBDII port (which should be about 12V). This control assumes that, if the voltage is lower than 6V, the OBDII port is disconnected from the car. If the option is enabled, it adds the OBDStatus.OBD_CONNECTED status, which is set when enough voltage is returned (socket connected to the car) but the ignition is off (no communication with the vehicle). Setting the option to False should be needed when the adapter does not support the voltage pin or more generally when the hardware provides unreliable results, or if the pin reads the switched ignition voltage rather than the battery positive (this depends on the car).')
@click.option('--redishost', default='localhost', help='The redis host.')

@click.version_option(version=__version__)

def main(port, baudrate, protocol, fast, timeout, checkvoltage, redishost):
  """A service to relay OBD2 info onto a seperate application message bus."""

  # Create a connection with the car
  car = automobile.Automobile(port, baudrate, protocol, fast, timeout, checkvoltage)
  redis = redispub.RedisPub(redishost)

  # Set up the commands we want to query the car about
  car.addCommands([
    'RPM', 
    {'command': 'SPEED', 'convertTo': 'mph'}, 
    {'name': 'ENGINE_TEMP', 'command': 'COOLANT_TEMP', 'convertTo': 'degF'}, 
  ])

  # Main loop where we continually query the car
  while (1):
    responses = car.query()
    for name in list(responses):
      response = responses[name]['result']
      redis.publishResponse(name, response)

    time.sleep(.5)
