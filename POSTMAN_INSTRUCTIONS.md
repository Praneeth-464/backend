# FairRide API - Postman Instructions

This guide will help you use Postman to interact with the FairRide API, specifically for registering users and riders.

## Setup

1. **Install Postman** if you haven't already: https://www.postman.com/downloads/
2. **Start the FairRide API server**:
   ```bash
   uvicorn app.main:app --reload
   ```
3. **Open Postman** and create a new request collection for FairRide API

## Registering a User as a Rider

The process involves two steps:
1. Register as a user
2. Register as a rider

### Step 1: Register as a User

1. **Create a new POST request** in Postman
2. **Set the URL** to: `http://localhost:8000/auth/signup/user`
3. **Set Headers**:
   - Key: `Content-Type`
   - Value: `application/json`
4. **Set Body** (select "raw" and "JSON"):
   ```json
   {
     "name": "John Doe",
     "email": "john.doe@example.com",
     "password": "securepassword123"
   }
   ```
5. **Send the request**
6. **Expected Response**:
   ```json
   {
     "id": "uuid-here",
     "name": "John Doe",
     "email": "john.doe@example.com",
     "role": "user",
     "created_at": "2025-10-16T10:00:00+05:30"
   }
   ```

### Step 2: Register as a Rider

1. **Create a new POST request** in Postman
2. **Set the URL** to: `http://localhost:8000/auth/signup/rider`
3. **Set Headers**:
   - Key: `Content-Type`
   - Value: `application/json`
4. **Set Body** (select "raw" and "JSON"):
   ```json
   {
     "name": "John Doe",
     "email": "john.doe@example.com",
     "origin_lat": 12.9716,
     "origin_lon": 77.5946,
     "destination_lat": 13.0358,
     "destination_lon": 77.5970,
     "preferred_departure": "2025-10-16T08:30:00+05:30",
     "preferred_arrival": "2025-10-16T09:00:00+05:30",
     "beta": 0.7
   }
   ```
5. **Send the request**
6. **Expected Response**:
   ```json
   {
     "name": "John Doe",
     "email": "john.doe@example.com",
     "origin_lat": 12.9716,
     "origin_lon": 77.5946,
     "destination_lat": 13.0358,
     "destination_lon": 77.5970,
     "preferred_departure": "2025-10-16T08:30:00+05:30",
     "preferred_arrival": "2025-10-16T09:00:00+05:30",
     "beta": 0.7,
     "id": "uuid-here",
     "status": "waiting",
     "created_at": "2025-10-16T10:00:00+05:30"
   }
   ```

## User Authentication (Optional but Recommended)

After registering, you'll receive an email with a verification link. Click this link to verify your email address before logging in.

If you don't receive the verification email, you can request a new one:

1. **Create a new POST request** in Postman
2. **Set the URL** to: `http://localhost:8000/auth/resend-verification`
3. **Set Headers**:
   - Key: `Content-Type`
   - Value: `application/json`
4. **Set Body** (select "raw" and "JSON"):
   ```json
   {
     "email": "john.doe@example.com"
   }
   ```
5. **Send the request**

After verifying your email, you can request an OTP for additional security:

1. **Create a new POST request** in Postman
2. **Set the URL** to: `http://localhost:8000/auth/request-otp`
3. **Set Headers**:
   - Key: `Content-Type`
   - Value: `application/json`
4. **Set Body** (select "raw" and "JSON"):
   ```json
   {
     "email": "john.doe@example.com"
   }
   ```
5. **Send the request**

Check your email for the OTP code, then verify it:

1. **Create a new POST request** in Postman
2. **Set the URL** to: `http://localhost:8000/auth/verify-otp`
3. **Set Headers**:
   - Key: `Content-Type`
   - Value: `application/json`
4. **Set Body** (select "raw" and "JSON"):
   ```json
   {
     "email": "john.doe@example.com",
     "otp": "123456"
   }
   ```
5. **Send the request**

After verifying the OTP, you can log in to get a JWT token for authenticated requests.

1. **Create a new POST request** in Postman
2. **Set the URL** to: `http://localhost:8000/auth/login`
3. **Set Body** (select "x-www-form-urlencoded"):
   - Key: `username`, Value: `john.doe@example.com`
   - Key: `password`, Value: `securepassword123`
4. **Send the request**
5. **Expected Response**:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

6. **To use the token for authenticated requests**:
   - Click on the "Authorization" tab
   - Select "Bearer Token" from the TYPE dropdown
   - Paste the access_token value in the "Token" field

## Environment Variables (Optional)

To make requests easier, you can set up environment variables in Postman:

1. Click on the "Environment" quick look icon (eye icon) in the top right
2. Click "Add"
3. Name your environment (e.g., "FairRide Dev")
4. Add variables:
   - Key: `base_url`, Value: `http://localhost:8000`
   - Key: `user_email`, Value: `john.doe@example.com`
   - Key: `user_password`, Value: `securepassword123`
5. Save the environment
6. Select your environment from the dropdown

Now you can use these variables in your requests:
- URL: `{{base_url}}/auth/signup/user`
- In request body: `"email": "{{user_email}}"`

## Common Endpoints Reference

| Method | Endpoint                                              | Description                              |
|--------|-------------------------------------------------------|------------------------------------------|
| POST   | /auth/signup/user                                     | Register a new user                      |
| POST   | /auth/signup/rider                                    | Register a new rider                     |
| POST   | /auth/signup/driver                                   | Register a new driver                    |
| POST   | /auth/login                                           | User login                               |
| GET    | /riders/                                              | Get all riders                           |
| GET    | /riders/{rider_id}                                    | Get specific rider                       |
| PUT    | /riders/{rider_id}                                    | Update rider information                 |
| DELETE | /riders/{rider_id}                                    | Delete rider request                     |
| GET    | /riders/{rider_id}/rides                              | Get rider's ride history                 |
| POST   | /riders/{rider_id}/rides/{ride_id}/cancel             | Cancel a ride request                    |
| POST   | /riders/{rider_id}/rides/{ride_id}/rate               | Rate driver after ride completion        |
| GET    | /riders/{rider_id}/notifications                      | Get rider notifications                  |
| POST   | /riders/{rider_id}/notifications/{notification_id}/read | Mark notification as read              |
| POST   | /drivers/                                             | Register a new driver                    |
| GET    | /drivers/                                             | Get all drivers                          |
| GET    | /drivers/{driver_id}                                  | Get specific driver                      |
| PUT    | /drivers/{driver_id}                                  | Update driver information                |
| DELETE | /drivers/{driver_id}                                  | Delete a driver                          |
| POST   | /drivers/{driver_id}/location                         | Driver updates current GPS               |
| GET    | /drivers/{driver_id}/rides                            | Get driver's ride history                |
| GET    | /drivers/{driver_id}/earnings                         | Get driver earnings information          |
| GET    | /drivers/{driver_id}/ratings                          | Get driver ratings and reviews           |
| GET    | /drivers/{driver_id}/notifications                    | Get driver notifications                 |
| POST   | /drivers/{driver_id}/notifications/{notification_id}/read | Mark notification as read            |
| POST   | /match/run                                            | Run selected algorithm (RGA/RGA++/IV)    |
| GET    | /metrics/latest                                       | Return fairness & efficiency metrics     |
| GET    | /rides/                                               | Get all rides                            |
| GET    | /rides/{ride_id}                                      | Get specific ride                        |
| GET    | /tracking/rides/{ride_id}                             | Get real-time tracking for ride          |
| POST   | /tracking/drivers/{driver_id}/location                | Update driver location                   |
| POST   | /ratings/rides/{ride_id}                              | Submit rating for completed ride         |
| GET    | /ratings/drivers/{driver_id}                          | Get ratings for specific driver          |
| GET    | /notifications/users/{user_id}                        | Get notifications for user               |

## Troubleshooting

1. **"Object of type datetime is not JSON serializable"**:
   - Make sure datetime fields are in ISO 8601 format with timezone (e.g., "2025-10-16T08:30:00+05:30")

2. **"401 Unauthorized"**:
   - Make sure you're including the Bearer token in the Authorization header for protected endpoints
   - Ensure your email is verified before logging in
   - Ensure you've completed the OTP verification process

3. **"400 Bad Request"**:
   - Check that all required fields are provided
   - Verify the JSON format is correct

4. **"User with this email already exists"**:
   - Use a different email address or proceed directly to login

5. **"Please verify your email address before logging in"**:
   - Check your email for the verification link and click it
   - Or use the resend verification endpoint to get a new email

6. **"Invalid or expired OTP"**:
   - Request a new OTP using the request-otp endpoint
   - Remember that OTPs expire after 30 minutes

## Example Collection

You can also import this sample collection into Postman:

```json
{
  "info": {
    "name": "FairRide API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Register User",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"John Doe\",\n  \"email\": \"john.doe@example.com\",\n  \"password\": \"securepassword123\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/auth/signup/user",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["auth", "signup", "user"]
        }
      },
      "response": []
    },
    {
      "name": "Register Rider",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"John Doe\",\n  \"email\": \"john.doe@example.com\",\n  \"origin_lat\": 12.9716,\n  \"origin_lon\": 77.5946,\n  \"destination_lat\": 13.0358,\n  \"destination_lon\": 77.5970,\n  \"preferred_departure\": \"2025-10-16T08:30:00+05:30\",\n  \"preferred_arrival\": \"2025-10-16T09:00:00+05:30\",\n  \"beta\": 0.7\n}"
        },
        "url": {
          "raw": "http://localhost:8000/auth/signup/rider",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["auth", "signup", "rider"]
        }
      },
      "response": []
    }
  ]
}
```

Save this as a `.json` file and import it into Postman using "Import" → "Upload Files".