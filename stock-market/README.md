This setups the infrastructure for Airflow, in Docker, as close as possible to a deploy in a Kubernetes/Helm environment: having containers for the airflow-scheduler, airflow-web, airflow-triggerer, and airflow-worker (with the CeleryExecutor)

Getting Started
1. Start setting up the infrastructure in Docker with:

Airflow with CeleryExecutor:

docker compose -f compose.celery.yaml up -d
Airflow with LocalExecutor:

docker compose -f compose.local.yaml up -d
2. Airflow WebUI can be accessed at:

open http://localhost:8080
3. Airflow DAGs:

To deploy Airflow DAGs, just move them inside the dags folder and Airflow should pick it up soon enough

TODO's:
 PEP-517: Packaging and dependency management with uv
 Code format/lint with Ruff
 Run Airflow DAGs on Docker
 Build Airflow DAGs with TaskFlow API
 Deploy Airflow to Kubernetes with Helm
 Run/Deploy Airflow DAGs on Kubernetes with KubernetesPodOperator