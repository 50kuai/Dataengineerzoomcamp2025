FROM python:3.9.1

# Install system dependencies for psycopg2 and pgcli
RUN apt-get update && apt-get install -y wget libpq-dev build-essential

# Install Python packages
RUN pip install pandas sqlalchemy psycopg2 pgcli

#getting env variable
ENV DB_USER=
ENV DB_PASS=
ENV DB_HOST=
ENV DB_PORT=
ENV DB_NAME=
ENV DB_TABLENAME=
ENV URL=

# Set the working directory
WORKDIR /app

# Copy your Python script into the container
COPY ingest_data.py ingest_data.py 

# Set the entry point to run the Python script
ENTRYPOINT ["python", "ingest_data.py"]