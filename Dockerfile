# Staged build to reduce image size by building a wheel
FROM python:3.10.11-slim-bullseye as build

WORKDIR /app
COPY ./. /app/

RUN python3 setup.py bdist_wheel

# Install just the wheel file
FROM python:3.10.11-slim-bullseye

COPY --from=build /app/dist/*.whl /tmp/

RUN pip3 install /tmp/*.whl

ENTRYPOINT ["/usr/local/bin/python3", "-m", "python_library"]
