# SafeQR FastAPI Application

This repository contains the SafeQR FastAPI application, which is packaged as a Docker image. This document provides instructions on how to build, run, and stop the Docker container for this application.

## Prerequisites

- **Docker**: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).

## Build the Docker Image

If you haven't built the Docker image yet, you can do so with the following command:

```bash
docker build -t safeqr-fastapi-app .
```

## Run the Docker Container

To run the Docker container from the image, use the following command:

```bash
docker run -d --name safeqr-ml -p 8000:8000 safeqr-fastapi-app
```

This will start the FastAPI application in a Docker container, making it accessible at `http://localhost:8000`.

## Stop/Kill the Docker Container

To stop the running container, first, find the container ID:

```bash
docker ps
```

This command lists all running containers. Find the `CONTAINER ID` for `safeqr-fastapi-app`.

To stop the container, use:

```bash
docker stop <container_id>
```

Replace `<container_id>` with the actual ID of your container.

If you want to remove the container entirely after stopping it:

```bash
docker rm <container_id>
```

## Accessing the Application Logs

If you need to view the logs of the running container, use:

```bash
docker logs <container_id>
```

## Removing the Docker Image

If you need to remove the Docker image, use the following command:

```bash
docker rmi safeqr-fastapi-app
```

This will remove the Docker image from your local machine.

## Troubleshooting

- **Port Conflict**: If port 8000 is already in use, you can change the port mapping. For example, to map the container's port 8000 to port 8080 on your machine, use:

  ```bash
  docker run -d -p 8080:8000 safeqr-fastapi-app
  ```

- **Container Already Running**: If you get an error that the container is already running, stop the existing container as shown above.


