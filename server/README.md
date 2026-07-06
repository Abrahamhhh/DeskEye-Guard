# Server Module

This folder contains the backend service for DeskEye Guard.

## Responsibilities

- Receive state data from ESP32-S3
- Store behavior records
- Provide APIs for frontend dashboard
- Generate simple daily statistics

## Possible API Design

- `POST /api/state`: upload current behavior state
- `GET /api/state/latest`: get latest state
- `GET /api/records`: get historical records
- `GET /api/statistics`: get summary statistics

## Possible Tech Stack

Early prototype:

- Python Flask or FastAPI
- SQLite database

Later version:

- Node.js / Express
- PostgreSQL or cloud database
- WebSocket real-time updates

## First Milestone

The first server milestone is to receive a JSON state packet and return it to the frontend through a simple API.
