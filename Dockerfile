FROM python:3.11-slim as builder

WORKDIR /app

# -------
# Install necessary python packages
COPY requirements.txt ./
RUN python -m pip wheel --wheel-dir /app/wheels -r requirements.txt

# -------
# Final stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

RUN mkdir -p /usr/local/gcloud && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz && /usr/local/gcloud/google-cloud-sdk/install.sh

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

RUN adduser --disabled-password jobrunner
USER jobrunner
RUN python -m pip install --no-cache /wheels/*

COPY --chown=jobrunner ../job_search job_search