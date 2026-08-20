# BigQuery GitHub Scraper — One-Time Setup Guide

## Why BigQuery?
Instead of hitting GitHub API (which blocks after 10 requests/min),
BigQuery gives us a COMPLETE static mirror of ALL GitHub public repos.
One SQL query = up to 75,000 PLC code files with ZERO rate limits.

---

## Step 1: Create a Free Google Cloud Project (5 minutes)
1. Go to: https://console.cloud.google.com/
2. Click 'Create Project'.
3. Name it: lumina-plc-data (or anything you like).
4. Free tier includes: 1TB of BigQuery queries per month.

---

## Step 2: Enable the BigQuery API (1 minute)
1. In your project, go to: APIs & Services > Library
2. Search for 'BigQuery API' and click 'Enable'.

---

## Step 3: Create a Service Account Key (3 minutes)
1. Go to: IAM & Admin > Service Accounts
2. Click 'Create Service Account'.
3. Name: lumina-scraper
4. Grant Role: BigQuery > BigQuery Data Viewer + BigQuery Job User
5. Click 'Create Key' > JSON > Download the key file.
6. Save it as: gcp_service_key.json somewhere safe on your machine.

---

## Step 4: Set the Environment Variable
Open PowerShell and run:
  \ = 'C:\path\to\gcp_service_key.json'
  \ = 'lumina-plc-data'

---

## Step 5: Run the Scraper
  cd 'C:\Users\majip\Downloads\LLM REASEARCH'
  .\.venv\Scripts\python.exe lumina\dataset_pipeline\bigquery_github_scraper.py

Expected runtime: 5-15 minutes
Expected output: 30,000 - 75,000 verified PLC code records
