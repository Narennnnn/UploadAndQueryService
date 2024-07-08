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
  ```
![image](https://github.com/Narennnnn/UploadAndQueryService/assets/120191897/b4cecfb7-b633-432c-a8b5-d46c5dd780b0)

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
  ````
![image](https://github.com/Narennnnn/UploadAndQueryService/assets/120191897/478d41e9-cb0e-4768-85d9-b679fe87d751)


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
  ```
  ![image](https://github.com/Narennnnn/UploadAndQueryService/assets/120191897/d0fe56fb-ede7-4c49-a030-af5778fe4b07)

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
  }
  ```
![image](https://github.com/Narennnnn/UploadAndQueryService/assets/120191897/30af761a-79e8-4a60-8eb8-f9da9aa0e6dc)

  
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
![image](https://github.com/Narennnnn/UploadAndQueryService/assets/120191897/94578a6e-19fd-478f-b9cc-b121ad6aaf49)

  
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
  ```
![image](https://github.com/Narennnnn/UploadAndQueryService/assets/120191897/ea87cfa0-4a7f-4dfd-80d3-9a250013cd6b)
  


### Replace `<generated_jwt_token>` with the actual token obtained from the login endpoint response.
#### Handling Token Expiry
If you receive a response with the following message:
```bash
  {
      "message": "Token has expired!"
  }
```

**Action**
Re-login:
Obtain a new JWT token by logging in again using your credentials.
    
## Cost Estimation for Running EC2 Instance in Production

### Instance Details:
- **Instance Type:** t3.micro instance is in the general purpose family with 2 vCPUs, 1.0 GiB of memory and up to 5 Gibps of bandwidth starting at $0.0108 per hour.
- **Region:** Europe (Stockholm) (eu-north-1)
- **On-Demand Linux Pricing:** $0.0108 USD per Hour

### Operations:
- **Instance Running Time:** 24 hours/day
- **Number of Days:** 30 days
- **File Uploads:** 1 per day
- **Queries:** 100 per day

### Cost Calculation:

1. **Calculate Monthly Hours:**
   - Hours in a day: 24 hours
   - Days in a month: 30 days
   - Total hours per month: 720 hours

2. **Calculate Instance Cost:**
   - Hourly rate: $0.0108 USD
   - Monthly cost: 720 hours * $0.0108 USD/hour = $7.78 USD/month

### Total Estimated Cost:
- **Base EC2 Cost:** $7.78 USD/month

### Free Tier Eligibility:
- The t3.micro instance type is eligible for the AWS Free Tier for new AWS accounts. 
- Under the Free Tier, you can use 750 hours of t3.micro instance per month for the first 12 months after sign-up
