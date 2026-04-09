# Celery & Redis Setup Guide

This guide will walk you through how to activate the asynchronous backend jobs inside MediZentrum Hospital Management System!

## Redis Requirements

### 1. Start your Redis Server
Before any workers can intercept Celery tasks or API Caching requests, you must have an active Redis message broker listening on the default port `6379`.
- **Windows (WSL / Docker)**
  ```bash
  docker run -d -p 6379:6379 redis
  ```
- **Windows natively**
  If installed natively via Memurai or older Redis versions for Windows, ensure the background service is running.

## Running Celery (Backend Asynchronous Jobs)

Open a new terminal specifically aimed at your `Backend` configuration directory (and make sure your python `venv` must be activated).

### 2. Start the Celery Worker
The worker intercepts and executes live jobs (like taking a patient's command to generate their history CSV!).
```bash
python run_celery.py
```
*(Alternatively, you can run: `celery -A celery_config.celery_app worker --loglevel=info -P gevent`)*

### 3. Start the Celery Beat (Recurring Schedule Jobs)
Celery Beat acts as the timeline trigger and executes the daily routines (Sending Daily Appointment Reminders & Emitting Monthly System Reports).
Open a third terminal in `Backend` configured in `venv`, then execute:
```bash
celery -A celery_config.celery_app beat --loglevel=info
```

### 4. Viewing Jobs & Operations
Once running, any requested CSV Export will automatically generate log prints indicating the generation process in the **Worker Terminal**.
If you want a visual dashboard to inspect all task queues, runtime results, and schedules, install and run `Flower`:
```bash
pip install flower
celery -A celery_config.celery_app flower
```
You can access the UI simply by navigating over to `http://localhost:5555`.
