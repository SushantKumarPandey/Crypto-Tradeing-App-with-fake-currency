# SWE II Boilerplate

This is a boilerplate project for SWE II, containing a simple client-server setup using Docker and Docker Compose.

## Project Structure

```
.gitlab-ci.yml
docker-compose.yml
README.md
client/
  Dockerfile
  index.html
server/
  Dockerfile
```

## Services

### Client

The client service is a simple Nginx server serving static files from the `client` directory.

- **Dockerfile**: [client/Dockerfile](client/Dockerfile)
- **Index File**: [client/index.html](client/index.html)

### Server

The server service is an Nginx server that serves a static image from `https://http.cat/200.jpg`.

- **Dockerfile**: [server/Dockerfile](server/Dockerfile)

## Docker Compose

The `docker-compose.yml` file defines the services and their configurations.

- **File**: [docker-compose.yml](docker-compose.yml)

## GitLab CI/CD

The `.gitlab-ci.yml` file defines the CI/CD pipeline for building and deploying the services.

- **File**: [.gitlab-ci.yml](.gitlab-ci.yml)

## Usage

### Running Locally

To run the project locally, use Docker Compose:

```sh
docker-compose up
```

- The client will be available at [http://localhost](http://localhost)
- The server will be available at [http://localhost:81](http://localhost:81)

### Building and Pushing Images

The GitLab CI/CD pipeline will automatically build and push Docker images to the GitLab registry.


& "C:\Program Files\Git\bin\bash.exe" run-checks.sh
