import csv
import time
import copy
from datetime import datetime
import requests
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException


def send_data(measurement):
    data = copy.deepcopy(measurement)
    data[timestamp] = datetime.strftime(data[timestamp], "%d.%m.%Y %H:%M:%S.%f")
    try:
        envelope = pubnub.publish().channel(pubnub_channel).message(data).sync()
        print("publish timetoken: %d" % envelope.result.timetoken)
        print(data)
    except PubNubException as e:
        print(e)
        send_data(measurement)

def reset_database():
    requests.post("https://vdp-api-tmauecfg5a-oa.a.run.app/vehicleRecords/reset")

reset_database()
measurements = []
pubnub_channel = "M0114.3"
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-67dfeb92-3ac7-11eb-88bb-1ad0e2424f4f"
pnconfig.publish_key = "pub-c-d5c9ad1c-c81a-4098-beb3-239de56fa4ed"
pubnub = PubNub(pnconfig)
pubnub.subscribe().channels(pubnub_channel).execute()
timestamp = "timestamp"
vehicle_class = "class"
length = "length"
speed = "speed"

with open('P09_VDP.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            measurements.append({
                timestamp: datetime.strptime(row[0], "%d.%m.%Y %H:%M:%S.%f"),
                vehicle_class: row[4],
                length: row[5],
                speed: row[7]
            })
            line_count += 1

measurements.reverse()

send_data(measurements[0])
for i in range(len(measurements)-1):
    delta = measurements[i+1][timestamp] - measurements[i][timestamp]
    time.sleep(delta.total_seconds())
    send_data(measurements[i+1])

pubnub.unsubscribe().channels(pubnub_channel).execute()