# Crime Pattern Analysis System (CPAS) / Crime Trend Mining

A full-stack crime analytics platform for incident tracking, trend analysis, and risk assessment — built to help identify high-risk areas and forecast crime trends using structured data and machine learning.

## Overview

CPAS centralizes crime incident data into a normalized relational database and layers SQL-based analysis and ML models on top to surface patterns that are hard to catch manually — anomalies, high-risk zones, and forecasted trend lines — all surfaced through a real-time dashboard.

## Features

- **Incident Tracking** — Structured recording of crimes, suspects, evidence, and case workflows.
- **Normalized Database Design** — A 3NF-normalized MySQL schema to keep crime records, suspect data, evidence, and case workflows consistent and query-efficient.
- **Anomaly Detection** — ML models flag unusual spikes or patterns in crime data that deviate from historical norms.
- **Risk Area Identification** — SQL-based and ML-driven analysis identifies geographic or categorical high-risk areas.
- **Trend Forecasting** — Predictive models forecast crime trend trajectories based on historical data.
- **Real-Time Dashboards** — Socket.IO powers live-updating dashboards for monitoring incidents as they're logged.
- **Containerized Deployment** — Fully Dockerized for scalable, reproducible deployment.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MySQL, SQLAlchemy (ORM) |
| ML | Scikit-learn |
| Real-Time | Socket.IO |
| Deployment | Docker |

## Database Design

The schema follows Third Normal Form (3NF) principles across core entities:
- Crimes
- Suspects
- Evidence
- Case Workflows

This keeps redundancy low and ensures updates to one entity (e.g., a suspect's details) don't require touching duplicated data elsewhere.

## Installation

```bash
git clone https://github.com/ERMRG444/crime_trend_mining.git
cd crime_trend_mining
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set up your MySQL database and update connection credentials in the config file, then run migrations:

```bash
flask db upgrade
```

## Usage

### Run locally

```bash
python app.py
```

### Run with Docker

```bash
docker-compose up --build
```

Then visit `http://localhost:5000` for the dashboard.

## Project Structure

```
crime_trend_mining/
├── app.py                  # Flask application entry point
├── models/                 # SQLAlchemy models (Crimes, Suspects, Evidence, Cases)
├── ml/
│   ├── anomaly_detection.py
│   └── trend_forecasting.py
├── sockets/                 # Socket.IO real-time event handlers
├── templates/                # Dashboard frontend
├── static/
├── docker-compose.yml
└── requirements.txt
```

## Future Improvements

- Add geospatial heatmaps for risk area visualization
- Expand forecasting models with seasonal/time-series features
- Role-based access control for law enforcement vs. analyst users

## Author

Vinit Hemkant Chaudhari — [LinkedIn](https://www.linkedin.com/in/vinit-chaudhari-154020376)
