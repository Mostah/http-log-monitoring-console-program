# HTTP log monitoring console program

## Overview

This project is a simple console program that monitors HTTP traffic. I build the structure of the project in order to be easily maintainable and scalable. Also, it contains tests, comments and a complete documentation to anyone who wants to contribute.


---
## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Project structure](#project-structure)
- [Details on the implementation](#details-on-the-implementation)
- [Possible improvements](#possible-improvements)

---
## Usage

### Requirements

* Python3.7 & pip3 installed
* Minimal terminal size 156x44
* Port 5000 available

### Install

```bash
make init
pip3 install -r requirements.txt
```

### Run

Run the server in one bash:
```bash
make run-server
```

WARNING: the GUI is not responsive, it needs a minimal size of 156x44

Run the client app (with default parameters) in another one:
```bash
make run-app
```

Run the client app with custom parameters:

```bash
python3 monitoring.py [-h] [--f FILE] [--thd THRESHOLD]
    [--wd WINDOW_TIME]
    [--tf TIMEFRAME]

# e.g: python3 monitoring.py --f access.log --thd 10 --wd 120 --tf 10
```

Run tests

```bash
make run-test
```

* FILE: file containing the formatted logs
* THRESHOLD: average hits per seconds that should trigger an alert
* WINDOW_TIME: timeframe (in sec) over which is computed the average hits per seconds for the alerting system (120 sec by default)
* TIMEFRAME: timeframe (in min) over which is computed all the statistics (10 min by default)

---
## Project structure

    ├── front
    │   ├── __init__.py
    │   ├── console_GUI.py
    │   └── service.py
    ├── back
    │   ├── app
    │   │   ├── models
    │   │   │   ├── __init__.py
    │   │   │   ├── alerts.py
    │   │   │   ├── general_traffic.py
    │   │   │   ├── json.py
    │   │   │   └── section_traffic.py
    │   │   ├── routes
    │   │   │   ├── __init__.py
    │   │   │   ├── alerts.py
    │   │   │   ├── general_traffic.py
    │   │   │   └── section_traffic.py
    │   │   ├── __init__.py
    │   │   ├── config.py
    │   │   └── utils.py
    │   ├── log_pipeline
    │   │   ├── __init__.py
    │   │   ├── alerter.py
    │   │   ├── log_reader.py
    │   │   ├── metrics.py
    │   │   ├── service.py
    │   │   ├── statistics_manager.py
    │   │   └── statistics.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── test_alerter.py
    │   │   ├── test_statistics_manager.py
    │   │   ├── test_statistics.py
    │   │   └── testdata.py
    │   ├── logs
    │   │   └── sample_csv.txt
    │   ├── __init__.py
    │   ├── run.py
    │   └── .flaskenv
    ├── __init__.py
    ├── monitoring.py
    ├── makefile
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
---
## Details on the implementation

### General
This project has been implemented with the Python language for one main reason: it may not be the fastest and the most scalable language but its syntax is concise and easy to write, thus small applications can be implemented quickly. Furthermore, with the right project structure, one can overcome Python's scalability limitation with horizontal scaling and vertical scaling. 

In the objective to make this project scalable, I chose to implement a back-end and a front-end that can run separately. Furthermore, I designed a pipeline that can run independently from both the application server and the GUI. Its purpose is to read logs, turn them into metrics and trigger alerts when necessary.

However, for the demonstration purpose, even if both the GUI and the pipeline do not interact with each other, they are launch together. Therefore one cannot quit the console GUI without exiting the pipeline process.

Let's take a deeper look into the project structure: 

### Console GUI

I used `npyscreen`, a library working on top of `curse`, to implement the console GUI. It was quite easy to use, but it lacks good online documentation and there are some limitations. For example, it is not possible to access some information such as in which column is a cell, in which row am I writing inside a component. Therefore, to get to the actual interface, with dynamic colors for each column, I tricked the library by adding a fixed amount of ' ' (space) for each element of a column to recognize value from it without the user seeing it.

To fetch the data from wherever it is stored, I chose to use a service that gets the data and format it to be ready to display. Therefore, if changes are made in the back-end, only the service needs to be modified. In the current implementation, the GUI is rerendered every second, therefore a lot of requests are made (one for every type of data, see Flask server for more information). A possible improvement to reduce the number of requests without changing the performance and quality of the app would be to wait for the server to tell the client that there is a new alert. This improvement could reduce by 30% the quantity of request sent by a client to the API.

Also, in the current version, the console GUI won't launch if the server is not running as it doesn't handle any request error, if this was project was continued, this improvement should be near the top of the list.

### Flask server

`Flask` is a framework for Python used to create web applications quickly, it offers good processes for database interaction. In my app, I distinguished three different models:
* `Alerts`: contain every information about an alert
* `GeneralTraffic`: general statistics from the logs
* `SectionTraffic`: statistics about a specific section

In the current state of the application, the `GeneralTraffic` model doesn't bring anything, as it could be possible (with some changes in the pipeline) to deduce its values from all the sections.

Also, I Implemented some basic routes for the three different models, but in the current state of the application some aren't use, but they were used at some point in the development. However, if the project were to be continued, some could be useful.



### Pipeline

The pipeline is the core structure of the project: it reads logs, saves the computed metrics in the database, and triggers an alert if necessary. It is composed of three main components: `LogReader`, `StatisticsManager`, and `Alerter`.

#### Log reader

The `LogReader` gives the rhythm of the whole pipeline, it sends one batch of logs every second (almost precisely, there is an offset of 0.0003s per seconds). This characteristic is very important for the rest of the pipeline. Also, for the scenario purpose of the application (by taking as input a log file from another day), the log reader defines a fictional time used by the whole pipeline.

I have implemented this module so that it carefully read one line at a time and do not store the whole file in memory. However, In the current state, the log reader cannot read logs in real-time. I put a lock while reading the logs so that no other processes can access it, and it never releases the resource, even after reading the whole file. However, the improvement should not be hard to make, but as I didn't have the time to write a `LogWriter` module, I didn't make the change.

In the current state of the module, there are two issues. A major one is that it doesn't check if a log is rightly formatted and not corrupted. As the sample CSV file of the log folder doesn't contain such logs, I didn't bother to implement one. But if for some reason the module read a corrupted log, it would break the whole pipeline. This improvement is at the top of the improvement list for security purposes. The minor one is that logs can arrive late, thus the log file is not sorted by time. However, as our hits statistics are computed over a 10s timeframe, and that a log is not likely to arrive more than 10s late, it should not impact too badly the statistics.

I did some stress tests on the pipeline to find its breaking point. On my computer, with the current implementation, the log reader can handle safely 1000 logs per second (the actual limit is around 1200), but not much more. If at some point the pipeline process of one second of logs takes more than one seconds in computational time, the reader won't be able to send a batch every second and will distort metrics and alerts It might even never send any batch if it takes more than one second to read a second of logs. This is the critical point of the structure.

#### Statistics manager

The `StatisticsManager` follows the rhythm given by the log reader. The purpose of this step in the pipeline is to update the metrics with the new batch of logs and send them to the alerter and the service (which do the connection with the database). 

For computation purposes, it keeps all the logs within the timeframe selected by the user. Therefore, if the timeframe or the data flow is too large, it could be a major memory issue. One improvement that would solve this issue is to either store the data in a database instead of keeping it in memory. Or change the way of computing the statistics to not store any logs, which would require a more complex structure of the `Statistics`.

#### Alerter

The `Alerter` follow the rhythm given by the statistics manager and check if an alert has to be triggered. I decided to not use directly the threshold set by the user in the alerting logic, but a difference of 5%, as the average hits per second can fluctuate around the threshold.

This module suffers from the same potential memory issue as the statistics manager if the selected time window for the alerting system is too large, or too many data is going through the pipeline

#### Service

In the current implementation, the `Alerter` and `StatisticsManager` send their data through a service that has direct access to the database. I designed it that way because I didn't need to separate the pipeline from the server application. However, it has been designed to be changed easily if the structure of the back-end had to evolve. The routes write in the database through the API are already implemented.

### Tests

The current test coverage of the application is far from 100%, only the pipeline is covered. `Alerter`, `Statistics`, and `StatisticsManager` are fully covered as their correctness is essential for this application, but it would be a great improvement to test the `LogReader` as well. Also, all other modules from the server application (especially the routes) and the front should be tested as well.

### Conclusion

As a conclusion, this app could handle very well the logs from several small web applications at the same time and a few medium ones on its own, but its capacity is not big enough to handle a big web application that could generate a traffic of more than 1000 requests per second. Nevertheless, this project structure has been designed to be scalable both vertically and horizontally. 

The vertical scaling because by adding more memory or computational capacity it will be able to handle more requests per second without making any change in the actual structure. 

The horizontal scaling because with some improvement the application could be launched on multiple servers. The same server application could be installed on several servers, each serving and storing data for only a pool of users. But also, the pipeline could be separated from the actual application server and could run in another one to gain in flow capacity.

## Possible improvements

As I went through the details of the implementation, I reported several existing issues and described small improvements that would solve them. Here are some bigger improvements that could be interesting to make but that would take more time to implement: 

* The application could trigger alerts on other metrics, such as the availability of a section going down which could inform about a server down. Also, this tool could be improved to handle any logs and compute useful specific stats on them. To do so, it would be necessary to create a statistics manager and alerter for each type of log, but the rest of the application could stay like this.
* The creation of an authentication system in the API that redirects a user to the server serving him. This would require some small changes in the database and the implementation of an authentication module in the server application. The front also has to be adapted to collect the user information and send them to the server.
* The implementation of a real frontend as the console is quite limited for displaying information. The front end could include data visualization in real-time and historical information (all data are already stored in the database).

---
Lastly, with a project like this, it's impossible to choose a break-off point. There is always another corner to sand down or a function tout could execute a bit faster, but the clock is ticking, and I have to turn this project in.

Thank you for taking the time to review my project, I hope you've found it to be easy to follow. 

Please contact me at thomas.vindard@supelec.fr if you encounter any issue launching the application.