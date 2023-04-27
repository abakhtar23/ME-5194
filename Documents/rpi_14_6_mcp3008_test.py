from gpiozero import MCP3008

mcp = MCP3008(channel = 0, clock_pin = 18, mosi_pin = 24, miso_pin = 23, select_pin = 25)
VREF = 3.3

while True:
	value = mcp.value
	voltage = value * VREF
	print("Soil Moisture Voltage: {}".format(voltage))
