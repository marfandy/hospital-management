# hospital-management

## Quick Start

Prerequisites

- git
- python >= 3.8

This presume that you have installed apps above.

1. Clone this project

    ```bash
    git@github.com:marfandy/hospital-management.git
    ```

2. Create `.env` and set your environment variables

    ```bash
   python -m venv venv
    ```

3. Install packages

    ```bash
    pip install -r requirements.txt
    ```

4. Start project!

    ```bash
    flask run
    ```

### Working with Docker

Prerequisites:

- git
- docker
- docker-compose

1. Clone this project

    ```bash
    git@github.com:marfandy/hospital-management.git
    ```

2. Create temporary directories

    ```bash
    mkdir -p tmp/{postgres}
    ```

4. Copy `.env.copy` to `.env` and set your environment variables

    ```bash
    cp .env.copy .env
    ```

4. Start project!

    ```bash
    docker-compose up -d
    ```