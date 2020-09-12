import obd
from obd import OBDStatus
import uuid

class Automobile:
  """Performs OBD queries on the automobile"""

  def __init__(self, port, baudrate, protocol, fast, timeout, checkvoltage):
    """Default constructor accepting parameters for creating a conection to OBD2 interface"""

    self._port = port
    self._baudrate = baudrate
    self._protocol = protocol
    self._fast = fast
    self._timeout = timeout
    self._checkvoltage = checkvoltage

    self._connection = obd.OBD(self._port, self._baudrate, self._protocol, self._fast, self._timeout, self._checkvoltage)

    self._commands = {}

  def get_connection(self):
    """Returns the connection to the automobiles OBD2 interface"""
    return self._connection

  def set_connection(self, value):
    """Sets a connection to the automobiles OBD2 interface"""
    self._connection = value

  connection = property(get_connection, set_connection)

  def addCommands(self, commandList):
    """Add a list of commands to query the automobile about"""

    for command in list(commandList):
      self.addCommand(command)
    return self._connection

  def addCommand(self, command):
    """Add a specific command to query the automobile about"""

    # Establish the defaults
    name = command  # By default the name is the command
    cmd = command   # By default the command is a string representation from the obd-python command table
    convertTo = None

    # If the this is a dictionary, parse out it's parts
    if isinstance(command, dict):
      cmd = command['command']
      convertTo = None
      name = command['command']  # dictionary must have a command, but the name is optional, as the command can be the name (in this case it must be a string)

      if 'name' in command:
        name = command['name']
      
      if 'convertTo' in command:
        convertTo = command['convertTo']

    # If the command part of of the dictionary is a strig convert it now
    if isinstance(cmd, str):
      cmd = obd.commands[cmd]

    # The name must be a string
    if not isinstance(name, str):
      name = uuid.uuid1()

    self._commands[name] =  {
      'command': cmd,
      'convertTo': convertTo
    }
    return self._commands

  def query(self):
    """Query the entire list of commands that have been set up"""
    
    responses = {}
    for name in list(self._commands):
      cmd = self._commands[name]

      result = self._connection.query(cmd['command'])
      
      if cmd['convertTo']:
        result.value = result.value.to(cmd['convertTo'])

      responses[name] = {
        'result': result
      }
    return responses
