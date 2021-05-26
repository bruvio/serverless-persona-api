FROM lambci/lambda:build-python3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

RUN pip install pytest

COPY .env .
COPY requirements.txt ./

RUN /bin/bash -c "source .env"
RUN pip install --no-cache-dir -r requirements.txt
