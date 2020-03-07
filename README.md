# Tunisair APP



Tunisair APP is a web application built using Python as the backend technology and Angular as the frontend technology. The web application aims to help Tunisair (national airline in Tunisia) reduce flight delays by predicting the `Remaining Useful Life - RUL` of aircraft components and providing real-time dashboard to monitor the health of aircrafts.
The project got us the first prize at the OpenGovDataHack2020 national hackathon.
Getting the first place required us to train a predictive model using a `Gradient Boosting` model, deploy it on the cloud (`using AWS EC2 server and RDS PostgreSQL instance`) and integrate it in a dashboard to help the administration avoid unexpected component failures.

The project is deployed and accessible through this [link](http://52.87.166.206)

[![N|Solid](https://alaeddineabdessalem.com/assets/img/achievements/opengovdatahack2020.jpg)](https://alaeddineabdessalem.com/assets/img/achievements/opengovdatahack2020.jpg)
# Description
The project consists in predicting the `Remaining Useful Life - RUL` of the aircraft's Turbofan engine. Sensors on the aircraft keep sending sensor data to the webservice. The app predicts the `RUL` using the trained model, ingests data point to database, sends email alarm when the engine reaches danger state and exposes engines health data in a REST API for the frontend.
Therefore, building the project consisted in different steps :
1. Training the machine learning model
2. Building the Microservices (REST API)
3. Building the Frontend
4. Creating scripts to simulate sending sensor data from aircraft

## Model Training :
We used the dataset provided in the Nasa repository for the Turbofan engine (check it [here](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/#turbofan)). The dataset comes with a research paper, describing the dataset and sensors data.
[![N|Solid](https://alaeddineabdessalem.com/assets/img/projects/research_paper.png)](https://alaeddineabdessalem.com/assets/img/projects/research_paper.png)

After training the model, accuracy was validated and plotted :
[![N|Solid](https://alaeddineabdessalem.com/assets/img/projects/model_training_result.png)](https://alaeddineabdessalem.com/assets/img/projects/model_training_result.png)

## REST API :
The REST API provides several endpoints listed below :
1. `GET /api/aircraft/<string:aircraftid>` : Fetches RUL data points for a specific aircraft identified by `aircraftid` from database and returns them ordered by timestamp. It also returns aircraft type and health status of the aircraft. Frontend uses this endpoint to visualize the aircraft RUL graph and show aircraft health status (`healthy` or `in danger`)
2. `POST /api/aircraft/<string:aircraftid>` : This endpoint receives sensor data for an aircraft from request payload as well as a timestamp value. It will call the machine learning model, predict the RUL value, put the new data point in the database and checks the health status of the aircraft. If the aircraft is in `danger` status, it will send an email to the administrator, showing the `RUL` value and a link to the aircraft graph :
[![N|Solid](https://alaeddineabdessalem.com/assets/img/projects/aircraft_status_email.png)](https://alaeddineabdessalem.com/assets/img/projects/aircraft_status_email.png)
This endpoint, is used by ingestion scripts to simulate aircrafts sending sensor data.
3. `GET /api/aircraft` : This endpoint returns RUL datapoints for all aircrafts in database, to be shown in the main dashboard like so :
4. [![N|Solid](https://alaeddineabdessalem.com/assets/img/projects/aircrafts_dashboard.png)](https://alaeddineabdessalem.com/assets/img/projects/aircrafts_dashboard.png)
5. `GET /api/flight/<int:day>/<int:month>/<int:year>` : This endpoint returns live data about flight in Tunis Carthage Airport. Data is scraped from the airport website in real-time and exposed in this endpoint.
## Frontend :
The Frontend is built using AngularJS. The single page web application keeps consuming the webservice using crons, to keep real-time insights about aircrafts data and updated graphs.

[![N|Solid](https://alaeddineabdessalem.com/assets/img/projects/MaintainIt.png)](https://alaeddineabdessalem.com/assets/img/projects/MaintainIt.png)
## Data ingestion scripts :
The script `flood_rul/flood_sousse.py` will get sample sensor data from the dataset and consume the REST API to send the data. Since the last sensor values corresponds to a deteriorated engine, the aircraft will enter an `in danger` status and an email will be sent.
To use the script, first delete the `RUL` data points from the frontend :
[![N|Solid](https://alaeddineabdessalem.com/assets/img/projects/clear_sousse.png)](https://alaeddineabdessalem.com/assets/img/projects/clear_sousse.png)
Then run the script : 
```python
python flood_rul/flood_sousse.py
```

### Tech

To develop such a project, here is the used tech stack:

* [AngularJS] - HTML enhanced for web apps!
* [Django](https://www.djangoproject.com) - python framework for the backend REST API
* [Flask](https://palletsprojects.com/p/flask/) - python framework for the backend REST API
* [Scikit-learn](https://scikit-learn.org) - we used the `GradientBoostingRegressor` from the scikit-learn library to train and deploy the Gradient Boosting model



