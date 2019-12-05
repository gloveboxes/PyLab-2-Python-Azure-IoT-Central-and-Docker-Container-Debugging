from datetime import datetime
import time
import sys
import json
import ptvsd
import telemetry_client
import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient


ptvsd.enable_attach(address=('0.0.0.0', 3000))

try:
    connectionString = os.environ['CONNECTION_STRING']
except:
    print("Missing Connection String")
    sys.exit(1)

if connectionString == '':
    print("Missing Connection String")
    sys.exit(1)

sampleRateInSeconds = 6
mysensor = telemetry_client.Telemetry()


async def main():
    global connectionString, sampleRateInSeconds
    device_client = IoTHubDeviceClient.create_from_connection_string(
        connectionString)
    await device_client.connect()

    msgId = 1
    while True:
        try:
            temperature, pressure, humidity, timestamp, cpu_temperature = mysensor.measure()

            data = {
                "Geo": 'Sydney, AU',
                "Humidity": humidity,
                "Pressure": pressure,
                "Temperature": temperature,
                "CpuTemperature": cpu_temperature,
                "Epoch": timestamp,
                "Id": msgId
            }

            telemetry = json.dumps(data)
            print(telemetry)

            await device_client.send_message(telemetry)

            msgId += 1

            time.sleep(sampleRateInSeconds)

        except KeyboardInterrupt:
            print("IoTHubClient sample stopped")
            return

        except:
            print("Unexpected error")
            time.sleep(sampleRateInSeconds)


if __name__ == "__main__":
    asyncio.run(main())
