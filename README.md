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

## 1. Signup

**Endpoint:** 
  ```bash
  http://13.50.90.158:5000/auth/signup
  ````

- **Method:** POST
- **Body:**
  ```json
    {
      "username": "harshitsingh",
      "password": "pass#101"
    }
    ```
- **Response:**
 ```bash
    {
        "message": "User registered successfully."
    } 
  ```
![image](https://github.com/user-attachments/assets/04f09640-33ce-406c-93f4-987ade41d2ee)


## 2. Login
#### Login using registered username and password

**Endpoint:** 
  ```bash
  http://13.50.90.158:5000/auth/login
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
![image](https://github.com/user-attachments/assets/4d346b96-46fb-4b73-9ec4-7297511b2835)


## 3. Upload CSV

**Endpoint:**
  ```bash
  http://13.50.90.158:5000/main/upload_csv
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
![image](https://github.com/user-attachments/assets/aa7fb447-18a6-48c7-bd39-629a79ff3c43)


## 4. Get Numerical Fields

**Endpoint:** 
  ```bash
  http://13.50.90.158:5000/query/query?Required_age=17
  ```
- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }
  ```
- **Response:**
  ![image](https://github.com/user-attachments/assets/775e3aef-3448-4eee-b77a-9922dd7c8de1)


## 5. Query using Names

**Endpoint:**
```bash
http://13.50.90.158:5000/query/query?Name=Tele
```
- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }
  ```
- **Response:**
![image](https://github.com/user-attachments/assets/6bff507c-fbbb-4c41-8861-29511cc5692e)

  
## 6. Get by Release Date

**Endpoint:** 
```bash
http://13.50.90.158:5000/query/query?Release_date=2020-02-03 
```

- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }
  ```
- **Response:**
![image](https://github.com/user-attachments/assets/47b8cd0d-cbf4-40ec-9705-00682ad10cd7)


  
## 7. Aggregate Search
```bash
    aggregate_field : column name
    aggregate_type  : aggregate function name for e.g. count , sum , avg , min , max , etc
```
**Endpoint:**

```bash
http://13.50.90.158:5000/query/query?aggregate_field=Price&aggregate_type=sum
 
```
- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }
  ```
- **Response:**
![image](https://github.com/user-attachments/assets/63991df5-3d16-4ac3-bd49-b731aaea756c)

## 8. Date Range Search
**Endpoint:**
```bash
http://13.50.90.158:5000/query/query?start_date=2020-02-03&end_date=2020-10-03
```
- **Method:** GET
- **Headers:**
  ```json
  {
    "Content-Type": "application/json",
    "Authorization": "Bearer <generated_jwt_token>"
  }
  ```
- **Response:**
![image](https://github.com/user-attachments/assets/41c25450-8125-41b4-bbe6-3d10123f5ec2)



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
