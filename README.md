# UploadAndQueryService

This repository contains a Flask application for handling CSV upload, querying data from ClickHouse, and authentication using JWT.

## Setup

### Docker Setup

You can pull the Docker image and run the application locally:

```bash
docker pull narendramaurya/segwise-flask-app:latest
```
```bash
docker run -p 5000:5000 narendramaurya/segwise-flask-app:latest
```
## Running on AWS EC2
### The application is deployed on AWS EC2 and can be accessed through:

# Testing Endpoints

You can test the endpoints using Postman or any HTTP client:

## 1. Login

**Endpoint:** 
  ```bash
  http://13.48.82.89/auth/login
  ````

- **Method:** POST
- **Body:**
  ```json
  {
    "username": "shobhit",
    "password": "shobhit@segwise"
  }
    ```
- **Response:**
 ```bash
    {
      "token": "<generated_jwt_token>"
    }
- ```

## 2. Uplpad CSV

**Endpoint:**
  ```bash
  http://13.48.82.89/main/upload_csv
  ````
- **Method:** POST
- **Header**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }
  ```
- **Body:**
  ```json
  {
  "csv_url": "https://drive.google.com/uc?export=download&id=18450NWcYxXZoEVrwwjwfIfDgLUUZPJPQ"
  }

    ```

- **Response:**
 ```bash
  {
      "message": "CSV upload and processing completed."
  }
- ```
## 3. Get Numerical Fields

**Endpoint:** 
  ```bash
  http://13.48.82.89/query/query?Required_age=17
  ```
- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }

## 4. Query using Names

**Endpoint:**
```bash
http://13.48.82.89/query/query?Name=Tele
```
- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }```
  
## 5. Get by Release Date

**Endpoint:** 
```bash
http://13.48.82.89/query/query?Release_date=2020-02-03 
```

- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }
  ```
  
## 6. Aggregate Search

**Endpoint:** 
```bash
http://13.48.82.89/query/query?aggregate_field=Price&aggregate_type=sum
 
```
- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }

## 7. Range-Based Date Search

**Endpoint:**
```bash
http://13.48.82.89/query/query?start_date=2020-02-03&end_date=2024-01-01
```
- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }

### Replace `<generated_jwt_token>` with the actual token obtained from the login endpoint response.
