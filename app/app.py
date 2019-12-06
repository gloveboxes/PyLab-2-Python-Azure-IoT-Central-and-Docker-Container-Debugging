from datetime import datetime
import time
import sys
import json
import ptvsd
import telemetry_client
import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import DeviceProvisionService as dps


ptvsd.enable_attach(address=('0.0.0.0', 3000))

try:
    scope = os.environ['SCOPE']
    device_id = os.environ['DEVICE_ID']
    key = os.environ['KEY']
except:
    print("Missing Scope, Device Id, or Key environment variable")
    sys.exit(1)

if not scope or not device_id or not key:
    print("Missing Scope, Device Id, or Key environment variable")
    sys.exit(1)

sampleRateInSeconds = 6
mysensor = telemetry_client.Telemetry()
device = dps.Device(scope, device_id, key)


async def main():
    global device, sampleRateInSeconds

    connectionString = await device.connection_string
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
