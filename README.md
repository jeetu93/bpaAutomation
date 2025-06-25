# BPA Order Report Generator

This project contains scripts to fetch order details from the BPA (Business Process Automation) system for specified service types and generate a consolidated CSV report.

## Features

- Fetches order data for the following service types:
  - CEN-L2
  - CEN-L3
  - MPLS
  - ISP
- Retrieves data within a specified date range (currently hardcoded in `GetLogsNpayloads.py`).
- Authenticates with the BPA API using credentials stored in `inventory.py`.
- Processes the fetched data and generates a `report.csv` file.
- Outputs a summary to the console.

## Prerequisites

- Python 3
- `requests` library (install using `pip install requests`)

## Configuration

1.  **`inventory.py`**: This file stores the BPA API host and authorization credentials. You need to ensure the `PROD2` dictionary within this file has the correct `host` (including port if necessary) and `Authorization` token (Base64 encoded `username:password`).

    Example `inventory.py` structure:
    ```python
    PROD2 = {
        "host": "your-bpa-host.example.com:port",
        "Authorization": "your_base64_encoded_credentials"
    }
    # Other environments like LAB can also be defined
    ```

2.  **Date Range (Optional Modification)**:
    Currently, the date range for fetching orders is hardcoded in `GetLogsNpayloads.py`:
    ```python
    start_date_str = "14-05-2020 00:00:00"
    end_date_str = "18-05-2020 23:59:59"
    ```
    You can modify these lines directly in the script if you need to fetch data for a different period.

## Usage

1.  **Fetch Order Data**:
    Run the `GetLogsNpayloads.py` script. This will contact the BPA API, fetch data for all configured service types, and save it to `data.json`.
    ```bash
    python GetLogsNpayloads.py
    ```

2.  **Generate CSV Report**:
    After `data.json` has been created, run the `createCsvReport.py` script. This will process `data.json` and generate `report.csv`.
    ```bash
    python createCsvReport.py
    ```

## Output

-   **`data.json`**: Contains the raw JSON response (aggregated from all service types) from the BPA API.
-   **`report.csv`**: The primary output file, containing processed order details in CSV format. Key columns include `ra` (order number), `status`, `status_msg`, `ckt_id`, `service_type`, `payload`, and `update_time`.
-   **Console Output**: Both scripts provide progress messages. `createCsvReport.py` also prints a summary of processed orders, including counts of total, passed, failed, and in-progress orders.

## Scripts Overview

-   **`GetLogsNpayloads.py`**: Fetches data from BPA API for multiple service types and saves to `data.json`.
-   **`createCsvReport.py`**: Parses `data.json` and generates `report.csv` and a console summary.
-   **`bpatoken.py`**: Handles authentication with the BPA API to get an access token. Uses `inventory.py`.
-   **`inventory.py`**: Configuration file for BPA host and credentials.
-   **`data.json`**: Intermediate file storing raw data fetched from the API. (Generated)
-   **`report.csv`**: Final CSV report. (Generated)
