SolarQuant
==========

SolarQuant is an open source system for predicting energy generation/consumption
using Machine Learning techniques implemented with Keras (TensorFlow backend).

## System + Components
In the SolarQuant system, the main system processes are identified as TRAINING jobs
and PREDICTION jobs. The processes follow a state system with the following order:
"initial" -> "retrieving data" -> "training"/"predicting" -> "finished". Once a job
completes (ie. in "finished" state), visualizations of neural network output can
be viewed.

### SolarNetwork API
The data used to produce predictive Neural Network models is retrieved from the
SolarNetwork APIs. The data retrieved includes aggregated kWh readings for 30 and 
60 min intervals and weather datum for locations. These are used as inputs for 
neural network training. 

### MySQL Database
Locally, data such as SolarNetwork API datum, intermediate values, neural network 
training output, correlation and predictive output are stored in a MySQL database. 
Additionally, process states are stored in the MySQL database. 

### Scheduling

A main component of SolarQuant is the Java-based scheduling system. A jarfile is run
periodically by CRON, which allows the progression of processes from state to state.
The Java system also handles errors and process failures.

### Data Retrieval
A Python module accesses the SolarNetwork APIs and manipulates the data in a fashion
that allows it to be stored MySQL tables for future use. The data is also transformed
 so that it may be used as an input to the predictive NN model. An important feature here
is that it does not allow redundancy - it will only download data that does not
already exist by checking time stamps.

### Keras / TensorFlow Module
The important functional part of this system is the Neural Network system that
forecasts energy readings. A Python module feeds preprocesed energy and weather datum
to the model implemented via Keras (Current model is a basic well tuned feed-forward 
network/perceptron, but can be swapped out for another with same input/output dimensions) 
for training, and feeds weather data alone for making predictions.  

### Web Front-End

A PHP/HTML/JS frontend exists that allows a user to easily manage their data sources,
prediction and training jobs, and view logs. The d3 graphing library has been used
for visualizing the output of the NN model.

## Setting Up / Deploying

Requires an Ubuntu setup.
