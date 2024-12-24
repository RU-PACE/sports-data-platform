# Sports-Data-Platform
A comprehensive sports data application aims to be a comprehensive platform for managing various sports, their leagues, major tournaments, and historical data regarding winners, built with FastAPI and MySQL, allowing for CRUD operations and data ingestion via CSV files.

<img src="./data/Project_Diagram.drawio.svg">

# ER Diagram documentation
## Summary

- [Introduction](#introduction)
- [Database Type](#database-type)
- [Table Structure](#table-structure)
	- [Sport](#Sport)
	- [TournamentType](#TournamentType)
	- [Tournament](#Tournament)
	- [Stat](#Stat)
- [Relationships](#relationships)
- [Database Diagram](#database-Diagram)

## Introduction

It is a database schema using SQLAlchemy for managing sports data. It organizes relationships between sports, tournament types, tournaments, and stats. Below is a breakdown of the classes and relationships


## Database type

- **Database system:** Generic
It is not designed for a specific application or domain. Instead, it provides a flexible framework that can be adapted to various data storage and retrieval needs.
## Table structure

### Sport

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INT | 🔑 PK, not null , unique, autoincrement |  |Primary Key |
| **name** | VARCHAR(50) | not null , unique |  | | 


### TournamentType

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INT | 🔑 PK, not null , unique, autoincrement |  | |
| **sport_id** | INT | not null  | Sport_id_fk | |
| **gender** | VARCHAR(10) | not null  |  | |
| **format** | VARCHAR(50) | not null  |  | | 


### Tournament

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INT | 🔑 PK, not null , unique, autoincrement |  | |
| **tournament_type_id** | INT | not null  | TournamentType_id_fk | |
| **tournament_id** | VARCHAR(50) | not null  |  | |
| **host** | VARCHAR(50) | not null  |  | |
| **venue** | VARCHAR(100) | not null  |  | |
| **winner** | VARCHAR(50) | not null  |  | |
| **runner_up** | VARCHAR(50) | not null  |  | |
| **player_of_the_match** | VARCHAR(100) | not null  |  | | 


### Stat

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INT | 🔑 PK, not null , unique, autoincrement |  | |
| **tournament_id** | INT | not null  | Tournament_id_fk | |
| **key** | VARCHAR(50) | not null  |  | |
| **value** | VARCHAR(100) | not null  |  | | 


## Relationships

- **TournamentType to Sport**: many_to_one
- **Tournament to TournamentType**: many_to_one
- **Stat to Tournament**: many_to_one

## Database Diagram

```mermaid
erDiagram
	TournamentType ||--o{ Sport : references
	Tournament ||--o{ TournamentType : references
	Stat ||--o{ Tournament : references

	Sport {
		INT id
		VARCHAR(50) name
	}

	TournamentType {
		INT id
		INT sport_id
		VARCHAR(10) gender
		VARCHAR(50) format
	}

	Tournament {
		INT id
		INT tournament_type_id
		VARCHAR(50) tournament_id
		VARCHAR(50) host
		VARCHAR(100) venue
		VARCHAR(50) winner
		VARCHAR(50) runner_up
		VARCHAR(100) player_of_the_match
	}

	Stat {
		INT id
		INT tournament_id
		VARCHAR(50) key
		VARCHAR(100) value
	}
```
---

# How can you access this project

This project is a simple sports data platform that uses **FastAPI** for the backend and **MySQL** for the database. The setup uses **Docker** and **Docker Compose** for containerization and deployment.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

You will also need:
- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to clone the repository.

## Cloning the Repository

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/RU-PACE/sports-data-platform.git
cd sports-data-platform
```

## Project Structure

Here’s an overview of the project structure:

```
sports-data-platform/
├── app/
│   ├── Dockerfile               # Dockerfile for FastAPI
│   ├── wait-for-db.sh           # Script to wait for MySQL to be ready
│   ├── main.py                  # FastAPI application entry point
│   ├── docker-compose.yml       # Docker Compose configuration file
│   └── ...                      # Other application files
└── README.md                    # This readme file
```

## Setting Up the Application

### Step 1: Pull Docker Images

The `docker-compose.yml` file defines two services:

- **MySQL**: Uses the official `mysql:9.1.0` image.
- **FastAPI**: Uses a custom image (`rupeshkr/myrepo:latest`) which you have built and pushed to Docker Hub.

You don’t need to build these images yourself as they will be pulled automatically.

### Step 2: Run Docker Compose

Since the `docker-compose.yml` file is inside the `app/` directory, you will need to navigate to the `app/` folder before running Docker Compose.

```bash
cd app
docker-compose up
```

This will:

- Pull the required images (`mysql:9.1.0` and `rupeshkr/myrepo:latest`).
- Set up the MySQL and FastAPI containers.
- Start the services.

### Step 3: Verify Application

Once the containers are up and running, you can access the FastAPI application at:

```
http://localhost:8000/docs
```

## How It Works

### 1. **MySQL Service**
The MySQL container is created using the official `mysql:9.1.0` image. It initializes with the following environment variables:

- `MYSQL_ROOT_PASSWORD`: Set to `password` (this is the root password for the MySQL database).
- `MYSQL_DATABASE`: Set to `test` (this is the name of the database created at startup).

The MySQL service will be accessible from the FastAPI application via the following database URL:

```
mysql+pymysql://root:password@mysql:3306/test
```

Here, the `mysql` part refers to the service name defined in the `docker-compose.yml` file. Docker Compose automatically resolves this to the correct container address.

### 2. **FastAPI Service**
The FastAPI service uses the Docker image `rupeshkr/myrepo:latest`, which contains your FastAPI application. The service waits for the MySQL database to be ready before starting using the `wait-for-db.sh` script.

- The FastAPI app will listen on port `8000` by default.
- The app connects to MySQL using the `DATABASE_URL` environment variable.

### 3. **Volumes**
- The MySQL data is persisted in the Docker volume `mysql_data`, ensuring data is not lost when the container is stopped or restarted.
- The FastAPI code is mounted as a volume to allow live code changes without rebuilding the container.

## Stopping the Application

To stop the application and remove the containers, run:

```bash
docker-compose down
```

This will stop and remove all containers, networks, and volumes defined in the `docker-compose.yml` file.

## Rebuilding the Images

If you need to rebuild the FastAPI image (for example, after making changes to the code), run the following:

```bash
docker-compose build fastapi
docker-compose up
```

This will rebuild only the FastAPI container and restart the services.

## Troubleshooting

### 1. **MySQL Connection Issues**
If the FastAPI application cannot connect to MySQL, ensure that:
- MySQL is running (`docker ps` to check active containers).
- The MySQL service is ready before FastAPI starts. This is handled by the `wait-for-db.sh` script, which waits for MySQL to be up and running before starting FastAPI.

### 2. **Port Conflicts**
Ensure that port `8000` (for FastAPI) and port `3306` (for MySQL) are not already in use on your machine. If they are, you can change the ports in the `docker-compose.yml` file under the `ports` section.

Example:

```yaml
ports:
  - "8080:8000"   # FastAPI service running on port 8080
  - "3307:3306"   # MySQL service running on port 3307
```

### 3. **Docker Hub Authentication Issues**
If you face issues with Docker Hub authentication, make sure you're logged into Docker Hub by running:

```bash
docker login
```

Here is a rule set for handling pull requests and a corresponding `README.md` file to guide contributors on how to create and review pull requests effectively.

---

## Pull Request Rule Set

#### 1. **General Guidelines**
- Each pull request (PR) should be tied to an issue or a specific task.
- Ensure that the PR title clearly describes the change.
- Include a detailed description of the changes in the PR body.
- Break large changes into smaller, logical PRs.

#### 2. **Branch Naming**
- Use descriptive branch names to indicate the purpose of the changes.
  Examples:
  - `feature/add-login-api`
  - `bugfix/fix-db-connection`
  - `chore/update-docs`

#### 3. **Commit Messages**
- Write clear and concise commit messages.
  Examples:
  - ✅ **Add user authentication API**
  - ✅ **Fix timeout issue in DB connection**
  - ❌ **Fix stuff**
- Use the imperative mood (e.g., "Add" instead of "Added" or "Adds").

#### 4. **Code Review Process**
- All PRs must be reviewed and approved first.
- Ensure code is properly linted and follows good coding standards.
- Include relevant tests (unit, integration, or end-to-end) for new or updated functionality , currently it does not have tests .
- Verify that all checks (CI/CD pipeline) pass before merging.

#### 5. **Testing Requirements**
- Run all tests locally and ensure they pass before creating a PR.
- Add new tests for any newly implemented features or bug fixes.
- Ensure high test coverage (if applicable).

#### 6. **Conflict Resolution**
- Keep the branch up-to-date with the main branch to avoid merge conflicts.
- Resolve conflicts locally and test thoroughly before updating the PR.

#### 7. **Documentation**
- Update the documentation (e.g., `README.md`, API docs) to reflect any new features or changes.
- Ensure any changes affecting external usage are documented clearly.

#### 8. **Labels and Tags**
- Add appropriate labels to the PR, such as:
  - `enhancement`
  - `bug`
  - `documentation`
  - `urgent`
- Use tags like `WIP` (Work in Progress) if the PR is not ready for review.

#### 9. **Merging**
- Use **Squash and Merge** for a clean commit history.
- Avoid merging your own PR unless explicitly allowed.

#### 10. **Closing Issues**
- Use keywords like `Fixes #123` or `Closes #123` in the PR description to automatically close the associated issue upon merging.

---

[//]: # (### `README.md` for Pull Requests)

[//]: # ()
[//]: # (```markdown)

[//]: # (# Pull Request Guidelines)

[//]: # ()
[//]: # (Thank you for contributing to this project! Please follow these guidelines when submitting a pull request.)

[//]: # ()
[//]: # (---)

[//]: # ()
[//]: # (## Steps to Create a Pull Request)

[//]: # ()
[//]: # (1. **Create a Branch**  )

[//]: # (   Create a new branch for your changes. Use a descriptive name:)

[//]: # (   ```bash)

[//]: # (   git checkout -b feature/add-new-api)

[//]: # (   ```)

[//]: # ()
[//]: # (2. **Write Code and Tests**  )

[//]: # (   - Implement the required changes.)

[//]: # (   - Add tests to validate the new functionality or bug fixes.)

[//]: # (   - Run tests locally to ensure everything works:)

[//]: # (     ```bash)

[//]: # (     pytest)

[//]: # (     ```)

[//]: # ()
[//]: # (3. **Commit Your Changes**  )

[//]: # (   Write clear and descriptive commit messages:)

[//]: # (   ```bash)

[//]: # (   git commit -m "Add user authentication API")

[//]: # (   ```)

[//]: # ()
[//]: # (4. **Push Your Branch**  )

[//]: # (   Push your branch to the remote repository:)

[//]: # (   ```bash)

[//]: # (   git push origin feature/add-new-api)

[//]: # (   ```)

[//]: # ()
[//]: # (5. **Create a Pull Request**  )

[//]: # (   - Go to the GitHub repository.)

[//]: # (   - Click **New Pull Request** and select your branch.)

[//]: # (   - Add a clear title and description.)

[//]: # (   - Link any related issues &#40;e.g., `Fixes #123`&#41;.)

[//]: # ()
[//]: # (---)

## Pull Request Review Process

1. **Submit the PR**  
   Once submitted, the CI/CD pipeline will run automatically to validate your changes.

2. **Respond to Feedback**  
   - Reviewers may request changes or provide suggestions.
   - Update your branch as needed:
     ```bash
     git add .
     git commit -m "Address review comments"
     git push origin feature/add-new-api
     ```

3. **Get Approval**  
   Ensure at least one reviewer approves the PR before merging.

4. **Merge the PR**  
   Once approved and CI/CD checks pass, the PR can be merged.

---

## Best Practices

- **Keep PRs Small**: Focus on a single feature or bug fix per PR.
- **Add Tests**: Cover your changes with appropriate tests.
- **Write Documentation**: Update any relevant documentation.
- **Resolve Conflicts**: Rebase or merge the main branch into your feature branch as needed:
  ```bash
  git fetch origin
  git rebase origin/main
  ```

---

## Labels and Tags

Use appropriate labels to categorize your PR:
- `enhancement`: For new features.
- `bug`: For bug fixes.
- `documentation`: For updates to documentation.
- `urgent`: For critical changes.

If your PR is not ready for review, mark it as a draft or add `[WIP]` to the title.

---

## Example Pull Request Template

When creating a PR, use the following template:

```markdown
### Description
Briefly describe the changes made in this PR.

### Related Issues
- Fixes #123
- Related to #456

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass locally

### Checklist
- [ ] Code adheres to project standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Ready for review
```

---


This `README.md` file provides clear, actionable instructions for contributing to the repository, submitting pull requests, and ensuring quality and consistency in the codebase.

## Conclusion

This project provides a simple setup for deploying a FastAPI backend with a MySQL database using Docker and Docker Compose. By following the steps in this README, you should be able to easily run the application on any machine.

If you have any issues or suggestions, feel free to open an issue on the GitHub repository!


