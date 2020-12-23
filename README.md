## Lab 9

The application is splitted into the cloud-native service, the frontend and the replay script which runs on the client side and simulates a sensor, which detects the vehicles in the traffic and sends the data to the service.

###  Setup / Usage

#### Replay Script (Sensor Simulator)
To run the code, sample traffic data is needed. The replay script connects over PubNub to the service and delivers the needed data. To run the python script input the following commands:
```console
foo@bar:~$ cd P09_VDP_Analytics_Service\replay
```

```console
foo@bar:~$ pip install -r requirements.txt
```

```console
foo@bar:~$ python replay.py
```

#### Frontend
After executing the python code, open the frontend to see the processed data in a dashboard.

The frontend is reachable under the following URL: https://p09-frontend-tmauecfg5a-oa.a.run.app/


#### API
The frontend gets its data from an API, which is deployed as a docker container to Google Cloud. The API is completely open and can be reached under the following URL: https://vdp-api-tmauecfg5a-oa.a.run.app/

The API documentation is written in OpenAPI and can be accessed under: https://app.swaggerhub.com/apis-docs/SCAD_HS20_Team2/vdp-analytics_service/1.0.0


### Design, Architecture and Implementation Decisions

#### Architecture
**The application consists of three main parts:**
- cloud-native service
- frontend
- replay script

The python replay script sends the detected data to the cloud service. The service accesses the database (MongoDB) to save the wanted vehicles and the data received from the sensor. The database runs on MongoDB Atlas. The frontend requests the statistic data from the cloud service every second and presents them to the user.

**The statistics include the following data:**
- average speed per vehicle category
- average length per vehicle category
- wanted vehicles
- traffic jam status

#### Communication
The communication between the sensor (in this case the replay script) and the cloud-service is realized with PubNub. This messaging framework follows the publish-subscribe pattern.  More about PubNub can be found on the following page: https://www.pubnub.com/.

The frontend accesses the service over the api. The OpenAPI documentation can be found below.

#### OpenAPI Service Description
The OpenAPI description can be found [here](https://app.swaggerhub.com/apis-docs/SCAD_HS20_Team2/vdp-analytics_service/1.0.0).

### Advertisement
The document with the advertisement can be found [here](https://github.com/sverbach/P09_VDP_Analytics_Service_Mirror/blob/master/Advertisment.pdf).
