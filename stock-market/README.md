# Project: Investor Portfolio Tracker

This repository contains the code and configuration for an end-to-end data engineering project developed during the Data Engineering Zoomcamp 2025. The project constructs a portfolio tracker that enables investors to monitor portfolio value, track stock transactions, and derive financial insights from both real-time and historical data.

![image](https://github.com/user-attachments/assets/f873d220-fcf3-4a21-950e-19df39485e7c)

## Problem Statement

The objective is to create a robust system that answers critical investor questions, including:

* Current share holdings for current portfolio.
* Current total portfolio valuation.
* Holdings price per stock.
<img width="901" alt="Screenshot 2025-03-11 at 9 47 38 PM" src="https://github.com/user-attachments/assets/ab5d8919-3182-4606-9ea0-a7658c6b8496" />




This is achieved by transforming raw transactional data into structured, actionable information using dbt models.

## Technologies Employed

This project utilizes a modern data stack, incorporating the following technologies:

* **Terraform:** Infrastructure as Code (IaC) for automated GCP resource provisioning.
* **Google Cloud Platform (GCP):** Cloud-based services for data storage and warehousing.
* **BigQuery:** Data warehouse for storing and querying transactional and stock market data.
* **Apache Airflow:** Workflow orchestration for data ingestion and processing.
* **dbt (Data Build Tool):** Data transformation and modeling.
* **Google Data Studio:** Data visualization and reporting.

## Project Workflow

1.  **Infrastructure Provisioning (Terraform):**
    * Automated creation of GCP resources, including BigQuery datasets and Cloud Storage buckets.

2.  **Data Ingestion (Airflow & Python):**
    * Scheduled daily extraction of stock market data from external APIs.
    * Loading of raw data into BigQuery.

3.  **Data Transformation (dbt):**
    * Data cleaning, modeling, and structuring of transactional data.
    * Aggregation of stock positions and calculation of portfolio performance metrics.

4.  **Data Visualization (Google Data Studio):**
    * Creation of interactive dashboards for portfolio performance monitoring.

## Project Setup and Execution

1.  **Repository Cloning:**

    ```bash
    git clone [https://github.com/50kuai/stock-market.git](https://github.com/50kuai/stock-market.git)
    cd stock-market
    ```

2.  **Google Cloud Platform Configuration:**

    * Create a GCP account via the Google Cloud Console.
    * Establish a new GCP project.
    * Enable the BigQuery, Cloud Storage, and Compute Engine APIs.

3.  **Terraform and Google Cloud SDK Installation:**

    * Install Terraform from the [HashiCorp website](https://www.terraform.io/downloads).
    * Install the Google Cloud SDK from the [Google Cloud website](https://cloud.google.com/sdk/docs/install).
    * Authenticate with GCP:

        ```bash
        gcloud auth application-default login
        ```

4.  **Terraform Initialization and Application:**

    ```bash
    terraform init
    terraform plan
    terraform apply
    ```

    Terraform will provision the necessary GCP resources, including BigQuery datasets, storage buckets, and service accounts.

5.  **Airflow Setup:**

    * Start Airflow using Docker Compose:

        ```bash
        docker-compose up -d
        ```

    * Access the Airflow UI at `http://localhost:8080`.
    * Trigger the DAG responsible for fetching stock data and loading it into BigQuery.

6.  **dbt Configuration and Execution:**

    * Initialize the dbt project:

        ```bash
        dbt init stock_market_dbt
        cd stock_market_dbt
        ```

    * Configure the dbt profile (`profiles.yml`) with your GCP project details:

        ```yaml
        stock_market_dbt:
          target: dev
          outputs:
            dev:
              type: bigquery
              method: service-account
              project: your-gcp-project-id
              dataset: stock_dataset
              threads: 4
              keyfile: /path/to/your-service-account.json
        ```

    * Replace `your-gcp-project-id` and `/path/to/your-service-account.json` with your actual GCP project ID and service account key file path.
    * Execute dbt models:

        ```bash
        dbt run
        ```

7.  **Google Data Studio Dashboard Creation:**

    * Open Google Data Studio.
    * Connect BigQuery as a data source and select the `stock_dataset`.
    * Develop visualizations to monitor portfolio performance.

## Project Outcomes

* Automated GCP resource provisioning via Terraform.
* Automated data ingestion pipeline using Airflow.
* Data transformation and modeling with dbt.
* Interactive portfolio performance visualization with Google Data Studio.

**Note:** Ensure that all required environment variables and service account credentials are correctly configured before running the project. Securely manage your credentials and avoid committing sensitive information to the repository.
