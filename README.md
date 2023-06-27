# Keycloak Realm Provisioning Service

## Project Overview

This project involves the creation of a service for provisioning customer tenants (realms) in Keycloak, an open-source Identity and Access Management solution. Docker is used for environment isolation and reproducibility, and Flask for creating a simple HTTP API for realm management.

## Key Accomplishments

1. Set up a Keycloak instance inside a Docker container, with data persistency ensured using Docker volumes.
2. Built a Flask application for interfacing with the Keycloak instance, with an HTTP endpoint for creating new realms. DNS subdomain validity is enforced for the realm names.
3. Containerized the Flask application using Docker, and coordinated both the Flask and Keycloak containers using Docker Compose.
4. Added password policy enforcement during realm creation in the Flask application.
5. Incorporated functionality to list all the created realms.
6. Configured Keycloak to use a PostgreSQL database running in a separate Docker container, which replaced local volume storage.

## Requirements

To replicate this project, you'll need the following software installed on your machine:

- **Docker**: Docker was used to containerize the Keycloak service and the Flask application, ensuring a consistent and reproducible environment. Docker can be downloaded from the [official website](https://www.docker.com/products/docker-desktop).
- **Docker Compose**: Docker Compose is a tool for running multi-container Docker applications. It was instrumental in managing and coordinating the Keycloak and Flask containers. Docker Compose comes pre-installed with Docker Desktop.
## Instructions to Run

1. Clone the repository and navigate to the project directory.
2. Run the following command in your terminal:

   ```shell
   docker-compose up

This command will pull the necessary images, build the Flask application image, and start the Docker containers.
1. Once the services are up, you can interact with the Flask application by sending HTTP requests to http://localhost:5001. For instance, to create a new realm:
    
    ```shell
    curl -X POST -H "Content-Type: application/json" -d '{"realm_name": "matan.test", "password_policy": "length(8) and specialChars(1)"}' http://localhost:5001/create-realm

2. To list all created realms:

    ```shell
    curl -X GET http://localhost:5001/list-realms

## Future Improvements
While the current project accomplishes the primary goal, there are several potential areas for improvement:

   * Security: Implement authentication and access control for the Flask application to secure the realm creation and listing operations.
   * Error handling: Robust error handling for better resilience and debugging.
   * Testing: Adding unit and integration tests to ensure the code behaves as expected.
   * Configuration: Employ environment variables or a configuration file for Keycloak URL and admin credentials.
   * Statelessness: Re-architect the Flask application for stateless operation, enabling easier horizontal scaling.
   * Database: Transition the PostgreSQL database to a managed service for improved resilience and performance.
   * CI/CD: Implementation of a continuous integration/continuous deployment (CI/CD) pipeline for automating the testing and deployment process.
   * Monitoring and Logging: Incorporating a logging framework into the application, along with application monitoring.
   * Front-end Interface: Develop a user-friendly UI on top of the Flask service for easier realm management.
