# Bike Point Pipeline

A lightweight ELT pipeline using **Python**, **Snowflake**, **GitHub Actions**, and **Kestra** to extract and load live bike station data from the **TFL Bike Point API** into your Snowflake warehouse.

---

## Python Script: `main.py`
A simple Python script that:
- Calls the TFL Bike Point API to retrieve real-time station data
- Saves the API response as a `.json` file in the `data/` directory
- Uploads the most recent file to an S3 bucket
- Deletes the local file after a successful upload

---

## Functions

 ### `extract_bikes()`
- Calls the TFL Bike Point API
- Saves the response as a `.json` file inside the `data/` folder

### `load_bikes()`
- Finds the most recent `.json` file (ignoring `.gitkeep`)
- Uploads it to the specified S3 bucket
- Deletes the file locally after a successful upload

---

## How to Run

1. Clone the repo  
2. Create a `.env` file with your credentials (see below)  
3. Install dependencies  
4. Run the ETL script:

```bash
python main.py
```

---

## Environment Variables

Create a `.env` file in the root directory with the following:

```dotenv
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_BUCKET_NAME=your_bucket_name
```

---

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Testing Individual Functions

You can test the functions on their own by importing them in an interactive session or script:

```python
from modules.extract_bike_points import extract_bikes
from modules.load_bike_points import load_bikes

extract_bikes()
load_bikes()
```

---

## GitHub Actions Automation
This pipeline can be automated using GitHub Actions.
Location: `.github/workflows/bike-point.yml`

---

## Kestra Orchestration
This pipeline can also be orchestrated using Kestra. A Kestra flow YAML is provided to automatically:
- Clone this repo
- Install dependencies
- Run main.py inside a Docker container

---

## Snowflake + SQL Pipeline
Once files are in S3, they’re staged and transformed in Snowflake.

### Key SQL Scripts in `/snowflake/`:
- `s3_load.sql`: Loads JSON from S3 into raw Snowflake tables
- `transform.sql`: Unnests the raw JSON and creates structured silver layer tables
- `stored_procedure.sql`: A Snowflake stored procedure that keeps your silver tables fresh via streams and tasks

---

## Folder Structure Summary
```bash
.
├── data/                          # JSON files (auto-deleted after upload)
│   └── .gitkeep
├── modules/                      # Python functions
│   ├── extract_bike_points.py
│   └── load_bike_points.py
├── main.py                       # Main script
├── kestra/
│   └── bike_point.yml            # Kestra flow
├── .github/
│   └── workflows/
│       └── bike-point.yml        # GitHub Actions automation
└── requirements.txt

```

