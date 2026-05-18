# Solution README

All stretch reqruiements have been completed.


## How to run the code

**Python 3.12** is recommended to be installed but other forms of Python 3 should also work.

Check version:

```
python --version
```

## Project Setup

Clone repository

```
git clone https://github.com/RossCampbell99/Optima-Data-Engineering-Assessment.git
```

Set the working directory in terminal:

```
cd data-engineering/datapipeline
```

## Create and Activate Virtual Environment

Create venv using Python 3.12 (or whatever version you are using):

```
python3.12 -m venv venv
```

Activate it:

### macOS / Linux
```
source venv/bin/activate
```

### Windows
```
venv\Scripts\activate
```

## Install Dependencies

Install project requirements:

```
pip install -r solution/requirements.txt
```


## Run Solution

```
python solution/main.py
```

## Run Unit Tests

Install pytest:

```
pip install pytest
```

Run unit tests:
```
python -m pytest
```

## Cloud Setup Overview

This project can be deployed to AWS using the Serverless Framework.

---

### Components

- **CI/CD pipeline (`gitlab-ci.yml`)**
  - Runs automated tests using `pytest`
  - Runs code style / linting checks
  - Deploys the application to AWS using the Serverless Framework

- **Docker**
  - Installs dependencies from `requirements.txt`
  - Provides a reproducible environment across local, CI, and cloud
  - Packages and copies application code for deployment

- **Infrastructure as Code (`serverless.yml` or Terraform)**
  - Defines AWS Lambda function (entry point: `main()`; typically `lambda_handler()` in production)
  - Configures IAM permissions (e.g. S3 read/write access)
  - Provisions required AWS resources

---

### Considerations

- **S3 integration**
  - Reads input CSV files from an S3 bucket
  - Writes processed results back to S3 (e.g. `stats_{year}.json`)

- **Event-driven execution**
  - Lambda can be triggered by S3 events
  - Automatically runs when either input CSV is updated
  - Updates and overwrites `stats_year.json` in S3
```
