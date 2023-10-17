# Secret Manager

## Overview

This is an ongoing project aimed at providing a secure and manageable way to store and retrieve secrets like API keys, passwords, and other sensitive information. The project utilizes Python for the backend logic and uses SQLite3 for storing the encrypted secrets. Additionally, it includes a `Dockerfile` and `docker-compose.yml` to containerize the application, making it portable and easy to deploy.

## Features

- Securely encrypt and decrypt secrets using Fernet symmetric encryption
- Easy-to-use interactive CLI
- SQLite3 database for secret storage
- Containerization support via Docker

## Prerequisites

- Python 3.x
- Docker and Docker Compose
- SQLite3

## Getting Started

### Clone the Repository:

```
git clone git@github.com:sohaib1khan/secret_manager.git
cd secret_manager
```

### Build and Start the Container

Run the `env_setup` script to create the `Dockerfile` and `docker-compose.yml`, and to launch the container.

```
./env_setup
```

### Usage

Once inside the Docker container, navigate to the `/app` directory and run the `secret_manager.py` script.

```
python3 app/secret_manager.py
```

You'll then be prompted with an interactive CLI where you can add, retrieve, delete, and list all stored secrets.

## Future Updates

This project is continuously growing. Expect more features and improvements in the future.