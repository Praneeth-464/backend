# FairRide API Documentation

A preference-driven ride scheduling system with fairness-optimized algorithms.

## Overview

FairRide is a ride-matching system that uses fairness-optimized scheduling algorithms instead of plain nearest-driver matching. The system supports three distinct but related entities:

- **Users**: Basic accounts that can sign up and authenticate. A user is the fundamental account type in the system.
- **Riders**: Users who request rides with specific preferences. A rider is a specialized profile that a user can create.
- **Drivers**: Users who provide rides to riders. A driver is a specialized profile that a user can create.

The relationship between these entities is:
1. A **User** creates an account with basic authentication credentials
2. A **User** can then create either a **Rider** profile or a **Driver** profile (or both)
3. **Riders** request rides with preferences
4. **Drivers** fulfill ride requests
5. The matching system pairs riders with drivers using fairness-optimized algorithms

This documentation covers all API endpoints. For driver-specific endpoints, see [apidriverdocs.md](apidriverdocs.md).

## Table of Contents
1. [Authentication](#authentication)
2. [Riders](#riders)
3. [Drivers](#drivers)
4. [Rides](#rides)
5. [Matching](#matching)
6. [Schedule Management](#schedule-management)
7. [Pricing & Fare Estimation](#pricing--fare-estimation)
8. [Scheduled Rides](#scheduled-rides)
9. [Wallet System](#wallet-system)
10. [Loyalty Program](#loyalty-program)
11. [Analytics](#analytics)
12. [Real-time Tracking](#real-time-tracking)
13. [Ratings and Reviews](#ratings-and-reviews)
14. [Notifications](#notifications)

## Base URL
```
http://localhost:8000
```

## Authentication

### Sign Up User
Register a new user account.

**Endpoint:** `POST /auth/signup/user`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "user",
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Sign Up Rider
Register a new rider with preference information linked to the current user.

**Endpoint:** `POST /auth/signup/rider`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**

Get the profile of the currently authenticated user.

**Endpoint:** `GET /auth/profile`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "user",
  "email_verified": true,
  "created_at": "2025-10-16T10:00:00+05:30",
  "last_login": "2025-10-16T14:30:00+05:30"
}
```

### Update User Profile
Update the profile of the currently authenticated user.

**Endpoint:** `PUT /auth/profile`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body (application/json):**
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com"
}
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "role": "user",
  "email_verified": true,
  "created_at": "2025-10-16T10:00:00+05:30",
  "last_login": "2025-10-16T14:30:00+05:30"
}
```

**Error Responses:**
- `400 Bad Request`: Email already registered
  ```json
  {
    "detail": "Email already registered"
  }
  ```
  
- `404 Not Found`: User not found
  ```json
  {
    "detail": "User not found"
  }
  ```
  
- `500 Internal Server Error`: Error updating profile
  ```json
  {
    "detail": "Error updating user profile: [error message]"
  }
  ```

### Verify Email
Verify a user's email address using the verification token sent via email.

**Endpoint:** `GET /auth/verify-email`

**Query Parameters:**
```
token: verification_token_received_via_email
```

**Response:**
```json
{
  "message": "Email verified successfully. You can now log in to your account."
}
```

### Resend Verification Email
Resend the email verification link to a user's email address.

**Endpoint:** `POST /auth/resend-verification`

**Request Body:**
```json
{
  "email": "john.doe@example.com"
}
```

**Response:**
```json
{
  "message": "Verification email sent successfully"
}
```

### Request OTP
Request a one-time password (OTP) for login verification.

**Endpoint:** `POST /auth/request-otp`

**Request Body:**
```json
{
  "email": "john.doe@example.com"
}
```

**Response:**
```json
{
  "message": "OTP sent successfully to your email"
}
```

### Verify OTP
Verify the one-time password (OTP) for login.

**Endpoint:** `POST /auth/verify-otp`

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "otp": "123456"
}
```

**Response:**
```json
{
  "message": "OTP verified successfully",
  "email": "john.doe@example.com"
}
```

## Riders

Riders are users who request rides with specific preferences. The relationship between users and riders is:

1. A **User** creates an account with basic authentication credentials
2. A **User** can then create either a **Rider** profile or a **Driver** profile (or both)
3. **Riders** request rides with preferences
4. **Drivers** fulfill ride requests
5. The matching system pairs riders with drivers using fairness-optimized algorithms

### Sign Up Rider
Register a new rider with preference information.

**Endpoint:** `POST /auth/signup/rider`

**Request Body:**
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

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T08:30:00+05:30",
  "preferred_arrival": "2025-10-16T09:00:00+05:30",
  "beta": 0.7,
  "id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "status": "waiting",
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

**Note:** No JWT token is required for this endpoint.

### Register Rider
Register a new rider profile. Validates that the email exists in the users table.

**Endpoint:** `POST /riders/`

**Request Body:**
```json
{
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.5
}
```

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.5,
  "id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "status": "waiting",
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

**Note:** No JWT token is required for this endpoint. The system will automatically update the user's role to 'rider' upon successful registration.

### Request Ride
Submit a new ride request with preferences. After submitting a ride request, the system automatically runs the RGA++ matching algorithm to pair the rider with an available driver.

**Endpoint:** `POST /riders/request`

**Request Body:**
```json
{
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.5
}
```

**Response (Success - Driver Matched):**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.5,
  "id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "status": "waiting",
  "created_at": "2025-10-16T12:00:00+05:30",
  "matched_driver": {
    "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "name": "John Smith",
    "email": "john.smith@example.com",
    "current_lat": 12.9710,
    "current_lon": 77.5940,
    "available": true,
    "rating": 4.8,
    "id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "background_check_status": "completed",
    "safety_training_completed": true,
    "total_incidents": 0,
    "performance_score": 98.5,
    "license_number": "DL1234567890",
    "license_expiry_date": "2026-12-31T00:00:00+05:30",
    "vehicle_make": "Toyota",
    "vehicle_model": "Camry",
    "vehicle_year": 2020,
    "vehicle_registration": "KA01AB1234",
    "vehicle_insurance_expiry": "2026-06-30T00:00:00+05:30"
  },
  "match_details": {
    "algorithm": "RGA++",
    "utility": 0.85,
    "metrics": {
      "gini_index": 0.25,
      "social_welfare": 0.85,
      "execution_time": 0.05
    }
  }
}
```

**Response (Success - No Driver Matched):**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.5,
  "id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "status": "waiting",
  "created_at": "2025-10-16T12:00:00+05:30",
  "matched_driver": null,
  "match_details": null
}
```

**Error Response (No Drivers Available):**
```json
{
  "detail": "No drivers available at the moment. Please try again later."
}
```

**Error Responses:**
- `400 Bad Request`: Email not found in users table
  ```json
  {
    "detail": "Email not found in users table. Please register as a user first."
  }
  ```

- `400 Bad Request`: Failed to create or update rider profile
  ```json
  {
    "detail": "Failed to create or update rider profile"
  }
  ```

**Process:**
1. System first checks for available drivers before creating ride request
2. If no drivers are available, returns error response
3. If drivers are available, creates rider profile (if needed) and ride request
4. Runs RGA++ matching algorithm to pair rider with driver
5. Returns rider information with matched driver details (if match found) or null values (if no match)

**Response Fields:**
- All rider fields as described in the RiderResponse schema
- `matched_driver`: Driver information if a match was found (null if no match)
- `match_details`: Information about the matching process including:
  - `algorithm`: The matching algorithm used (RGA++)
  - `utility`: Utility score for this pairing (higher is better)
  - `metrics`: Fairness and efficiency metrics
    - `gini_index`: Gini coefficient measuring fairness (0 = perfectly fair, 1 = perfectly unfair)
    - `social_welfare`: Overall system efficiency (higher is better)
    - `execution_time`: Time taken to run the algorithm in seconds

**Process:**
1. Riders submit ride requests using `POST /riders/request`
2. Drivers update their availability using `POST /drivers/{driver_id}/location`
3. The system automatically runs the RGA++ matching algorithm when a ride is requested
4. If a match is found, both rider and driver are notified
5. Rides are created in the system with "assigned" status
6. Drivers and riders can track ride status using the rides endpoints

### Get All Riders
    "destination_lon": 77.5970,
    "preferred_departure": "2025-10-16T14:00:00+05:30",
    "preferred_arrival": "2025-10-16T14:30:00+05:30",
    "beta": 0.5,
    "id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "status": "waiting",
    "created_at": "2025-10-16T12:00:00+05:30"
  }
]
```

### Get Rider by ID
Retrieve a specific rider by ID.

**Endpoint:** `GET /riders/{rider_id}`

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.5,
  "id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "status": "waiting",
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

### Get Current Rider
Retrieve the rider profile for the currently authenticated user.

**Endpoint:** `GET /riders/me`

**Headers:**
```json

Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.5,
  "id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "status": "waiting",
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

### Update Current Rider
Update the rider profile for the currently authenticated user.

**Endpoint:** `PUT /riders/me`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.7
}
```

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "preferred_arrival": "2025-10-16T14:30:00+05:30",
  "beta": 0.7,
  "id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "status": "waiting",
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

### Delete Current Rider
Delete the rider profile for the currently authenticated user.

**Endpoint:** `DELETE /riders/me`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "Ride request deleted successfully"
}
```

### Get Current Rider Ride History
Get all rides for the currently authenticated user.

**Endpoint:** `GET /riders/me/rides`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json

[
  {
    "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "algorithm": "RGA++",
    "start_time": "2025-10-16T14:15:00+05:30",
    "end_time": "2025-10-16T14:45:00+05:30",
    "fare": 125.50,
    "utility": 0.85,
    "status": "completed",
    "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0"
  }
]
```

### Cancel Current Rider Ride
Cancel an active ride request for the currently authenticated user.

**Endpoint:** `POST /riders/me/rides/{ride_id}/cancel`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "Ride cancelled successfully"
}
```

### Rate Driver
Rate a driver after completing a ride for the currently authenticated user.

**Endpoint:** `POST /riders/me/rides/{ride_id}/rate`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "rating": 5,
  "review": "Great driver, very polite and safe",
  "tip": 20.0
}
```

**Response:**
```json
{
  "id": "r4t1n2g3-5678-9012-a3b4-c5d6e7f8g9h0",
  "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rating": 5,
  "review": "Great driver, very polite and safe",
  "tip": 20.0,
  "created_at": "2025-10-16T15:00:00+05:30"
}
```

### Get Rider Notifications
Get notifications for a specific rider.

**Endpoint:** `GET /riders/{rider_id}/notifications`

**Response:**
```json
[
  {
    "id": "n1o2t3i4-5678-9012-a3b4-c5d6e7f8g9h0",
    "user_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "title": "Ride Assigned",
    "message": "Your ride has been assigned to driver John Smith",
    "type": "ride_assignment",
    "read": false,
    "created_at": "2025-10-16T14:10:00+05:30"
  }
]
```

### Mark Notification as Read
Mark a notification as read.

**Endpoint:** `POST /riders/{rider_id}/notifications/{notification_id}/read`

**Response:**
```json
{
  "id": "n1o2t3i4-5678-9012-a3b4-c5d6e7f8g9h0",
  "user_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "title": "Ride Assigned",
  "message": "Your ride has been assigned to driver John Smith",
  "type": "ride_assignment",
  "read": true,
  "created_at": "2025-10-16T14:10:00+05:30"
}
```

## Drivers

Drivers are users who provide rides to riders. A user must first create a basic account before creating a driver profile.

For detailed driver-specific endpoints and functionality, see [apidriverdocs.md](apidriverdocs.md).

### Register Driver
Register a new driver linked to the current user.

**Endpoint:** `POST /drivers/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "name": "Bob Wilson",
  "email": "bob.wilson@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 4.9
}
```

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Bob Wilson",
  "email": "bob.wilson@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 4.9,
  "id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8"
}
```

### Register Driver
Register a new driver linked to the current user.

**Endpoint:** `POST /drivers/`

**Request Body:**
```json
{
  "name": "Bob Wilson",
  "email": "bob.wilson@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 4.9
}
```

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Bob Wilson",
  "email": "bob.wilson@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 4.9,
  "id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8"
}
```

**Note:** No JWT token is required for this endpoint. The system will automatically update the user's role to 'driver' upon successful registration.

### Get All Drivers
Retrieve all drivers.

**Endpoint:** `GET /drivers/`

**Response:**
```json
[
  {
    "name": "Bob Wilson",
    "email": "bob.wilson@example.com",
    "current_lat": 12.9716,
    "current_lon": 77.5946,
    "available": true,
    "rating": 4.9,
    "id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8"
  }
]
```

### Get Current Driver
Retrieve the driver profile for the currently authenticated user.

**Endpoint:** `GET /drivers/me`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Bob Wilson",
  "email": "bob.wilson@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 4.9,
  "id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8"
}
```

### Update Current Driver
Update the driver profile for the currently authenticated user.

**Endpoint:** `PUT /drivers/me`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "name": "Bob Wilson",
  "email": "bob.wilson@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 5.0
}
```

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "name": "Bob Wilson",
  "email": "bob.wilson@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 5.0,
  "id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8"
}
```

### Delete Current Driver
Delete the driver profile for the currently authenticated user.

**Endpoint:** `DELETE /drivers/me`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "Driver deleted successfully"
}
```

### Update Driver Location
Update a driver's current location and availability. Requires authentication.

**Endpoint:** `POST /drivers/{driver_id}/location`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "current_lat": 13.0358,
  "current_lon": 77.5970,
  "available": true
}
```

**Response:**
```json
{
  "message": "Location updated successfully"
}
```

### Get Current Driver Ride History
Get all rides for the currently authenticated user.

**Endpoint:** `GET /drivers/me/rides`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "user_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
    "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "driver_id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8",
    "algorithm": "RGA++",
    "start_time": "2025-10-16T14:15:00+05:30",
    "end_time": "2025-10-16T14:45:00+05:30",
    "fare": 125.50,
    "utility": 0.85,
    "status": "completed",
    "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0"
  }
]
```

### Get Current Driver Earnings
Retrieve earnings and statistics for the currently authenticated user.

**Endpoint:** `GET /drivers/me/earnings`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "driver_id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8",
  "total_earnings": 1250.75,
  "total_rides": 42,
  "average_rating": 4.8,
  "hours_online": 28.5,
  "timestamp": "2025-10-16T10:00:00+05:30"
}
```

### Get Current Driver Ratings
Get ratings and reviews for the currently authenticated user.

**Endpoint:** `GET /drivers/me/ratings`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "driver_id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8",
  "average_rating": 4.8,
  "total_ratings": 127,
  "reviews": [
    {
      "id": "r4t1n2g3-5678-9012-a3b4-c5d6e7f8g9h0",
      "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
      "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
      "driver_id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8",
      "rating": 5,
      "review": "Great driver, very polite and safe",
      "tip": 20.0,
      "created_at": "2025-10-16T15:00:00+05:30"
    }
  ]
}
```

### Get Driver Notifications
Get notifications for a specific driver.

**Endpoint:** `GET /drivers/{driver_id}/notifications`

**Response:**
```json
[
  {
    "id": "n1o2t3i4-5678-9012-a3b4-c5d6e7f8g9h0",
    "user_id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8",
    "title": "New Ride Request",
    "message": "You have a new ride request from Alice Johnson",
    "type": "ride_request",
    "read": false,
    "created_at": "2025-10-16T14:10:00+05:30"
  }
]
```

### Mark Notification as Read
Mark a notification as read.

**Endpoint:** `POST /drivers/{driver_id}/notifications/{notification_id}/read`

**Response:**
```json
{
  "id": "n1o2t3i4-5678-9012-a3b4-c5d6e7f8g9h0",
  "user_id": "p5o4n3m2-l1k0-9876-j5h4-g3f2e1d0c9b8",
  "title": "New Ride Request",
  "message": "You have a new ride request from Alice Johnson",
  "type": "ride_request",
  "read": true,
  "created_at": "2025-10-16T14:10:00+05:30"
}
```

### Accept Ride Request
Accept a ride assignment from the matching algorithm.

**Endpoint:** `POST /drivers/{driver_id}/rides/{ride_id}/accept`

**Response:**
```json
{
  "message": "Ride accepted successfully",
  "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rider_name": "Alice Johnson",
  "pickup_location": {
    "lat": 12.9716,
    "lon": 77.5946
  },
  "dropoff_location": {
    "lat": 13.0358,
    "lon": 77.5970
  }
}
```

### Start Ride
Mark a ride as started (driver has picked up the rider).

**Endpoint:** `POST /drivers/{driver_id}/rides/{ride_id}/start`

**Response:**
```json
{
  "message": "Ride started successfully",
  "start_time": "2025-10-16T14:15:00+05:30"
}
```

### End Ride
Mark a ride as completed and calculate fare.

**Endpoint:** `POST /drivers/{driver_id}/rides/{ride_id}/end`

**Response:**
```json
{
  "message": "Ride completed successfully",
  "end_time": "2025-10-16T14:45:00+05:30",
  "fare": 125.50,
  "distance": 8.2
}
```

## Rides

### Get All Rides
Retrieve all ride records for the authenticated user. Requires authentication.

**Endpoint:** `GET /rides/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
    "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "algorithm": "RGA++",
    "start_time": "2025-10-16T14:15:00+05:30",
    "end_time": "2025-10-16T14:45:00+05:30",
    "fare": 125.50,
    "utility": 0.85,
    "status": "completed"
  }
]
```

### Get Rider Rides
Get all rides for a specific rider by rider ID.

**Endpoint:** `GET /riders/{rider_id}/rides`

**Response:**
```json
[
  {
    "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
    "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "algorithm": "RGA++",
    "start_time": "2025-10-16T14:15:00+05:30",
    "end_time": "2025-10-16T14:45:00+05:30",
    "fare": 125.50,
    "utility": 0.85,
    "status": "completed"
  }
]
```

### Get Ride by ID
Retrieve a specific ride by ID.

**Endpoint:** `GET /rides/{ride_id}`

**Response:**
```json
{
  "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
}

### Get Current Rider Ride History
Get all rides for the currently authenticated user.

**Endpoint:** `GET /riders/me/rides`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "algorithm": "RGA++",
    "start_time": "2025-10-16T14:15:00+05:30",
    "end_time": "2025-10-16T14:45:00+05:30",
    "fare": 125.50,
    "utility": 0.85,
    "status": "completed",
    "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0"
  }
]
```


  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "algorithm": "RGA++",
  "start_time": "2025-10-16T14:15:00+05:30",
  "end_time": "2025-10-16T14:45:00+05:30",
  "fare": 125.50,
  "utility": 0.85,
  "status": "completed"
}
```

### Create Ride
Create a new ride request for the authenticated user. Requires authentication.

**Endpoint:** `POST /rides/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "algorithm": "RGA++",
  "status": "requested"
}
```

**Response:**
```json
{
  "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rider_id": "r1i2d3e4-r5i6-d7e8-r9i0-d1e2r3i4d5e6",
  "algorithm": "RGA++",
  "status": "requested",
  "created_at": "2025-10-16T14:15:00+05:30"
}
```

## Matching

The matching system pairs riders with drivers using fairness-optimized algorithms. After a rider submits a ride request, you need to run a matching algorithm to create assignments between riders and drivers.

### Run Matching Algorithm
Execute a ride matching algorithm to pair riders with drivers. Requires authentication. This endpoint will find available drivers and match them with waiting riders based on the selected algorithm.

**Endpoint:** `POST /match/run`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "algorithm": "RGA++"
}
```

**Response:**
```json
{
  "algorithm": "RGA++",
  "assignments": [
    {
      "rider_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
      "driver_id": "z9y8x7w6-v5u4-3210-t9s8-r7q6p5o4n3m2",
      "utility": 0.85
    }
  ],
  "metrics": {
    "gini_index": 0.25,
    "social_welfare": 0.85,
    "execution_time": 0.05
  }
}
```

**Response Fields:**
- `algorithm`: The matching algorithm used
- `assignments`: Array of rider-driver pairings
  - `rider_id`: ID of the rider
  - `driver_id`: ID of the assigned driver
  - `utility`: Utility score for this pairing (higher is better)
- `metrics`: Fairness and efficiency metrics
  - `gini_index`: Gini coefficient measuring fairness (0 = perfectly fair, 1 = perfectly unfair)
  - `social_welfare`: Overall system efficiency (higher is better)
  - `execution_time`: Time taken to run the algorithm in seconds

**Process:**
1. Riders submit ride requests using `POST /riders/request`
2. Drivers update their availability using `POST /drivers/{driver_id}/location`
3. An administrator or system runs this matching algorithm
4. The algorithm creates assignments and sends notifications to both riders and drivers
5. Rides are created in the system with "assigned" status
6. Drivers and riders can track ride status using the rides endpoints

### Get Matching Algorithms
Retrieve available matching algorithms.

**Endpoint:** `GET /match/algorithms`

**Response:**
```json
{
  "algorithms": [
    {
      "name": "RGA",
      "description": "Randomized Greedy Algorithm - Basic randomized greedy approach"
    },
    {
      "name": "RGA++",
      "description": "Enhanced Randomized Greedy Algorithm - Fairness-enhanced version"
    },
    {
      "name": "IV",
      "description": "Iterative Voting - Consensus-based scheduling with voting rules"
    }
  ]
}
```

## Schedule Management

### Run Scheduling Algorithm
Execute a ride matching algorithm and store the results as a schedule. Requires authentication.

**Endpoint:** `POST /schedules/run`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "algorithm": "RGA++"
}
```

**Response:**
```json
{
  "algorithm": "RGA++",
  "assignments": [
    {
      "rider_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
      "driver_id": "z9y8x7w6-v5u4-3210-t9s8-r7q6p5o4n3m2",
      "utility": 0.85
    }
  ],
  "metrics": {
    "gini": 0.25,
    "social_welfare": 0.85
  },
  "schedule_id": "s1c2h3e4-d5u6-7890-l1m2-n3o4p5q6r7s8"
}
```

### Get All Schedules
Retrieve all stored schedules. Requires authentication.

**Endpoint:** `GET /schedules/`

**Headers:**
```

```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "s1c2h3e4-d5u6-7890-l1m2-n3o4p5q6r7s8",
    "algorithm": "RGA++",
    "metadata": {
      "assignments": [
        {
          "rider_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
          "driver_id": "z9y8x7w6-v5u4-3210-t9s8-r7q6p5o4n3m2",
          "utility": 0.85
        }
      ],
      "metrics": {
        "gini": 0.25,
        "social_welfare": 0.85
      }
    },
    "created_at": "2025-10-16T10:00:00+05:30"
  }
]
```

### Get Schedule by ID
Retrieve a specific schedule by ID. Requires authentication.

**Endpoint:** `GET /schedules/{schedule_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": "s1c2h3e4-d5u6-7890-l1m2-n3o4p5q6r7s8",
  "algorithm": "RGA++",
  "metadata": {
    "assignments": [
      {
        "rider_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
        "driver_id": "z9y8x7w6-v5u4-3210-t9s8-r7q6p5o4n3m2",
        "utility": 0.85
      }
    ],
    "metrics": {
      "gini": 0.25,
      "social_welfare": 0.85
    }
  },
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Delete Schedule
Delete a specific schedule by ID. Requires authentication.

**Endpoint:** `DELETE /schedules/{schedule_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "Schedule deleted successfully"
}
```

## Pricing & Fare Estimation

### Estimate Fare
Estimate the fare for a ride based on origin, destination, and other factors.

**Endpoint:** `POST /pricing/estimate`

**Request Body:**
```json
{
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "rider_beta": 0.7,
  "traffic_multiplier": 1.2
}
```

**Response:**
```json
{
  "estimated_fare": 15.75,
  "distance_km": 8.2,
  "estimated_duration_minutes": 16.4,
  "base_fare": 2.5,
  "distance_fare": 10.25,
  "time_fare": 8.2,
  "surge_multiplier": 1.25
}
```

### Estimate Fare by Algorithm
Estimate the fare for a ride based on origin, destination, and a specific matching algorithm. This endpoint also provides algorithm-specific metrics and utility values.

**Endpoint:** `POST /pricing/estimate/algorithm`

**Request Body:**
```json
{
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "rider_beta": 0.7,
  "traffic_multiplier": 1.2,
  "algorithm": "RGA++"
}
```

**Response:**
```json
{
  "algorithm": "RGA++",
  "estimated_fare": 15.75,
  "distance_km": 8.2,
  "estimated_duration_minutes": 16.4,
  "base_fare": 2.5,
  "distance_fare": 10.25,
  "time_fare": 8.2,
  "surge_multiplier": 1.25,
  "utility": 0.85,
  "metrics": {
    "gini": 0.25,
    "social_welfare": 0.78
  }
}
```

## Scheduled Rides

### Schedule Ride
Schedule a ride for a future time. Requires authentication.

**Endpoint:** `POST /scheduled-rides/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "scheduled_time": "2025-10-16T14:00:00+05:30",
  "preferences": {
    "min_driver_rating": 4.5,
    "ride_type": "solo",
    "accessibility_needs": ["wheelchair"]
  }
}
```

**Response:**
```json
{
  "id": "s1c2h3e4-d5u6-7890-l1m2-n3o4p5q6r7s8",
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "scheduled_time": "2025-10-16T14:00:00+05:30",
  "status": "scheduled",
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

### Get Scheduled Rides
Get all scheduled rides for the authenticated user. Requires authentication.

**Endpoint:** `GET /scheduled-rides/rider`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "s1c2h3e4-d5u6-7890-l1m2-n3o4p5q6r7s8",
    "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "origin_lat": 12.9716,
    "origin_lon": 77.5946,
    "destination_lat": 13.0358,
    "destination_lon": 77.5970,
    "scheduled_time": "2025-10-16T14:00:00+05:30",
    "status": "scheduled",
    "created_at": "2025-10-16T12:00:00+05:30"
  }
]
```

### Update Scheduled Ride Status
Update the status of a scheduled ride. Requires authentication.

**Endpoint:** `PUT /scheduled-rides/{ride_id}/status/{status}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": "s1c2h3e4-d5u6-7890-l1m2-n3o4p5q6r7s8",
  "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "scheduled_time": "2025-10-16T14:00:00+05:30",
  "status": "confirmed",
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

## Wallet System

### Get Wallet Balance
Get the wallet balance for the authenticated user. Requires authentication.

**Endpoint:** `GET /wallet/balance`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "balance": 125.50
}
```

### Create Wallet Transaction
Create a wallet transaction (credit or debit) for the authenticated user. Requires authentication. The user_id is optional and will default to the authenticated user's ID. The balance_after field is calculated by the system and returned in the response.

**Endpoint:** `POST /wallet/transaction`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0", // Optional - defaults to authenticated user
  "amount": 50.0,
  "transaction_type": "credit",
  "description": "Promotional credit"
}
```

**Response:**
```json
{
  "id": "t1r2a3n4-5678-9012-a3b4-c5d6e7f8g9h0",
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "amount": 50.0,
  "transaction_type": "credit",
  "description": "Promotional credit",
  "balance_after": 175.50,
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

### Get Transaction History
Get transaction history for the authenticated user. Requires authentication.

**Endpoint:** `GET /wallet/transactions`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "t1r2a3n4-5678-9012-a3b4-c5d6e7f8g9h0",
    "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "amount": 50.0,
    "transaction_type": "credit",
    "description": "Promotional credit",
    "balance_after": 175.50,
    "created_at": "2025-10-16T12:00:00+05:30"
  }
]
```

## Loyalty Program

### Get Loyalty Info
Get loyalty information for the authenticated user. Requires authentication.

**Endpoint:** `GET /loyalty/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "points": 250,
  "level": "gold",
  "next_level_points": 750
}
```

### Update Loyalty Points
Update loyalty points for the authenticated user (add or subtract). Requires authentication.

**Endpoint:** `POST /loyalty/points`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters:**
```
points: integer
```

**Response:**
```json
{
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "points": 300,
  "level": "gold",
  "next_level_points": 700
}
```

## Analytics

### Get User Analytics
Get analytics for the authenticated user. Requires authentication.

**Endpoint:** `GET /analytics-simple/user`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "total_rides": 25,
  "total_spent": 875.50,
  "average_rating": 4.7,
  "favorite_destinations": [
    {
      "location": "13.0358,77.5970",
      "count": 8
    }
  ],
  "spending_patterns": {
    "total_spent": 875.50,
    "average_ride_cost": 35.02,
    "rides_count": 25
  },
  "ride_history": []
}
```

### Get User Analytics with Filters
Get analytics for the authenticated user with date filters. Requires authentication.

**Endpoint:** `POST /analytics-simple/user`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "start_date": "2025-10-01T00:00:00+05:30",
  "end_date": "2025-10-31T23:59:59+05:30",
  "metrics": ["spending", "rides", "ratings"]
}
```

## Authentication

### Reset Password
Reset password for a user with an empty password hash.

**Endpoint:** `POST /auth/reset-password`

**Request Body (application/json):**
```json
{
  "email": "john.doe3@example.com",
  "new_password": "newsecurepassword123"
}
```

**Response:**
```json
{
  "message": "Password reset successfully. You can now log in with your new password."
}
```

**Error Responses:**
- `404 Not Found`: User not found
  ```json
  {
    "detail": "User not found"
  }
  ```
  
- `400 Bad Request`: Password reset not allowed
  ```json
  {
    "detail": "Password reset is only allowed for accounts with empty password hashes. Use the regular password change process instead."
  }
  ```


**Response:**
```json
{
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "total_rides": 25,
  "total_spent": 875.50,
  "average_rating": 4.7,
  "favorite_destinations": [
    {
      "location": "13.0358,77.5970",
      "count": 8
    }
  ],
  "spending_patterns": {
    "total_spent": 875.50,
    "average_ride_cost": 35.02,
    "rides_count": 25
  },
  "ride_history": []
}
```

## Real-time Tracking

### Get Ride Tracking
Get real-time tracking information for an active ride. Requires authentication.

**Endpoint:** `GET /tracking/rides/{ride_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "driver_location": {
    "lat": 12.9850,
    "lon": 77.6000
  },
  "estimated_arrival": "2025-10-16T14:10:00+05:30",
  "distance_to_pickup": 1.2,
  "eta_dropoff": "2025-10-16T14:45:00+05:30"
}
```

### Update Driver Location (Real-time)
Update driver location for real-time tracking. Requires authentication.

**Endpoint:** `POST /tracking/drivers/{driver_id}/location`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "lat": 12.9850,
  "lon": 77.6000,
  "speed": 30.5,
  "heading": 45.0
}
```

**Response:**
```json
{
  "message": "Location updated successfully",
  "timestamp": "2025-10-16T14:10:00+05:30",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "location": {
    "lat": 12.9850,
    "lon": 77.6000,
    "speed": 30.5,
    "heading": 45.0
  }
}
```

## Ratings and Reviews

### Submit Ride Rating
Submit a rating and review for a completed ride. Requires authentication.

**Endpoint:** `POST /ratings/rides/{ride_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "rating": 5,
  "review": "Great service, very professional driver!",
  "tip": 20.0
}
```

**Response:**
```json
{
  "message": "Rating submitted successfully"
}
```

### Get Driver Ratings
Retrieve ratings and reviews for a specific driver.

**Endpoint:** `GET /ratings/drivers/{driver_id}`

**Response:**
```json
{
  "driver_id": "z9y8x7w6-v5u4-3210-t9s8-r7q6p5o4n3m2",
  "average_rating": 4.8,
  "total_ratings": 127,
  "reviews": [
    {
      "rating": 5,
      "review": "Excellent service!",
      "date": "2025-10-15T10:30:00+05:30"
    }
  ]
}
```

## Notifications

### Get User Notifications
Retrieve notifications for the authenticated user. Requires authentication.

**Endpoint:** `GET /notifications/user`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "n1o2t3i4-f5i6-c7a8-t9i0-o1n2s3t4a5n6",
    "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "title": "Ride Confirmed",
    "message": "Your ride has been confirmed with driver Jane Smith",
    "type": "ride_confirmation",
    "read": false,
    "created_at": "2025-10-16T14:05:00+05:30"
  }
]
```

### Mark Notification as Read
Mark a notification as read. Requires authentication.

**Endpoint:** `POST /notifications/{notification_id}/read`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "Notification marked as read",
  "notification": {
    "id": "n1o2t3i4-f5i6-c7a8-t9i0-o1n2s3t4a5n6",
    "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "title": "Ride Confirmed",
    "message": "Your ride has been confirmed with driver Jane Smith",
    "type": "ride_confirmation",
    "read": true,
    "created_at": "2025-10-16T14:05:00+05:30"
  }
}
```

### Create Notification
Create a new notification for the authenticated user. Requires authentication.

**Endpoint:** `POST /notifications/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "title": "New Message",
  "message": "You have a new message from your driver",
  "type": "chat"
}
```

**Response:**
```json
{
  "id": "n1o2t3i4-f5i6-c7a8-t9i0-o1n2s3t4a5n6",
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "title": "New Message",
  "message": "You have a new message from your driver",
  "type": "chat",
  "read": false,
  "created_at": "2025-10-16T14:05:00+05:30"
}
```

## Data Models

### UserCreate
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

### UserResponse
```json
{
  "id": "uuid",
  "name": "string",
  "email": "string",
  "role": "string",
  "email_verified": false,
  "email_verification_token": "string",
  "email_verification_sent_at": "2025-10-16T10:00:00+05:30",
  "created_at": "2025-10-16T10:00:00+05:30",
  "last_login": "2025-10-16T10:00:00+05:30"
}
```

### RiderCreate
```json
{
  "name": "string",
  "email": "string",
  "origin_lat": 0,
  "origin_lon": 0,
  "destination_lat": 0,
  "destination_lon": 0,
  "preferred_departure": "2025-10-16T08:30:00+05:30",
  "preferred_arrival": "2025-10-16T09:00:00+05:30",
  "beta": 0.5
}
```

### RiderResponse
```json
{
  "name": "string",
  "email": "string",
  "origin_lat": 0,
  "origin_lon": 0,
  "destination_lat": 0,
  "destination_lon": 0,
  "preferred_departure": "2025-10-16T08:30:00+05:30",
  "preferred_arrival": "2025-10-16T09:00:00+05:30",
  "beta": 0.5,
  "id": "uuid",
  "status": "string",
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### DriverCreate
```json
{
  "name": "string",
  "email": "string",
  "current_lat": 0,
  "current_lon": 0,
  "available": true,
  "rating": 5.0
}
```

### DriverResponse
```json
{
  "name": "string",
  "email": "string",
  "current_lat": 0,
  "current_lon": 0,
  "available": true,
  "rating": 5.0,
  "id": "uuid"
}
```

### DriverUpdateLocation
```json
{
  "current_lat": 0,
  "current_lon": 0,
  "available": true
}
```

### RideCreate
```json
{
  "rider_id": "uuid",
  "driver_id": "uuid",
  "algorithm": "string",
  "start_time": "2025-10-16T14:15:00+05:30",
  "end_time": "2025-10-16T14:45:00+05:30",
  "fare": 0,
  "utility": 0,
  "status": "string"
}
```

### RideResponse
```json
{
  "rider_id": "uuid",
  "driver_id": "uuid",
  "algorithm": "string",
  "start_time": "2025-10-16T14:15:00+05:30",
  "end_time": "2025-10-16T14:45:00+05:30",
  "fare": 0,
  "utility": 0,
  "status": "string",
  "id": "uuid"
}
```

### MatchRequest
```json
{
  "algorithm": "RGA" // Options: "RGA", "RGA++", "IV"
}
```

### Assignment
```json
{
  "rider_id": "uuid",
  "driver_id": "uuid",
  "utility": 0
}
```

### MatchResponse
```json
{
  "algorithm": "string",
  "assignments": [
    {
      "rider_id": "uuid",
      "driver_id": "uuid",
      "utility": 0
    }
  ],
  "metrics": {
    "gini_index": 0,
    "social_welfare": 0,
    "execution_time": 0
  }
}
```

### NotificationCreate
```json
{
  "user_id": "uuid",
  "title": "string",
  "message": "string",
  "type": "string"
}
```

### NotificationResponse
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "string",
  "message": "string",
  "type": "string",
  "read": false,
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### RatingCreate
```json
{
  "rating": 5,
  "review": "string",
  "tip": 0
}
```

### RatingResponse
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "driver_id": "uuid",
  "rating": 5,
  "review": "string",
  "date": "2025-10-16T10:00:00+05:30"
}
```

### VerifyEmailRequest
```json
{
  "token": "string"
}
```

### ResendVerificationRequest
```json
{
  "email": "string"
}
```

### OTPRequest
```json
{
  "email": "string"
}
```

### OTPVerifyRequest
```json
{
  "email": "string",
  "otp": "string"
}
```

### DriverRatingsResponse
```json
{
  "driver_id": "uuid",
  "average_rating": 4.8,
  "total_ratings": 127,
  "reviews": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "driver_id": "uuid",
      "rating": 5,
      "review": "string",
      "date": "2025-10-16T10:00:00+05:30"
    }
  ]
}
```

### SystemMetrics
```json
{
  "total_rides": 1250,
  "active_riders": 42,
  "active_drivers": 28,
  "average_wait_time": 5.2,
  "completion_rate": 98.5,
  "average_rating": 4.7,
  "timestamp": "2025-10-16T10:00:00+05:30"
}
```

### AlgorithmPerformance
```json
{
  "name": "string",
  "gini_index": 0.25,
  "social_welfare": 0.85,
  "execution_time": 0.12,
  "usage_count": 450
}
```

### UserAnalytics
```json
{
  "user_id": "uuid",
  "total_rides": 25,
  "total_spent": 875.50,
  "favorite_destinations": [
    {
      "location": "string",
      "count": 8
    }
  ],
  "preferred_time": "string",
  "timestamp": "2025-10-16T10:00:00+05:30"
}
```

### DriverEarnings
```json
{
  "driver_id": "uuid",
  "total_earnings": 1250.75,
  "total_rides": 42,
  "average_rating": 4.8,
  "hours_online": 28.5,
  "timestamp": "2025-10-16T10:00:00+05:30"
}
```

## Driver Safety and Verification

### Create Driver Verification
Create a new driver verification record.

**Endpoint:** `POST /driver-safety/verifications`

**Request Body:**
```json
{
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "verification_type": "background_check",
  "document_url": "https://example.com/documents/background_check_123.pdf",
  "notes": "Background check completed with no issues",
  "verified_by": "a1d2m3i4-5678-9012-a3b4-c5d6e7f8g9h0"
}
```

**Response:**
```json
{
  "id": "v1e2r3i4-f5i6-c7a8-t9i0-o1n2s3t4a5n6",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "verification_type": "background_check",
  "status": "pending",
  "document_url": "https://example.com/documents/background_check_123.pdf",
  "notes": "Background check completed with no issues",
  "verified_by": "a1d2m3i4-5678-9012-a3b4-c5d6e7f8g9h0",
  "verified_at": null,
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T10:00:00+05:30"
}
```

### Get Driver Verifications
Get all verifications for a driver.

**Endpoint:** `GET /driver-safety/verifications/{driver_id}`

**Response:**
```json
[
  {
    "id": "v1e2r3i4-f5i6-c7a8-t9i0-o1n2s3t4a5n6",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "verification_type": "background_check",
    "status": "approved",
    "document_url": "https://example.com/documents/background_check_123.pdf",
    "notes": "Background check completed with no issues",
    "verified_by": "a1d2m3i4-5678-9012-a3b4-c5d6e7f8g9h0",
    "verified_at": "2025-10-16T11:00:00+05:30",
    "created_at": "2025-10-16T10:00:00+05:30",
    "updated_at": "2025-10-16T11:00:00+05:30"
  }
]
```

### Update Driver Verification
Update a driver verification record.

**Endpoint:** `PUT /driver-safety/verifications/{verification_id}`

**Request Body:**
```json
{
  "status": "approved",
  "notes": "Verification approved after review",
  "verified_by": "a1d2m3i4-5678-9012-a3b4-c5d6e7f8g9h0"
}
```

**Response:**
```json
{
  "id": "v1e2r3i4-f5i6-c7a8-t9i0-o1n2s3t4a5n6",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "verification_type": "background_check",
  "status": "approved",
  "document_url": "https://example.com/documents/background_check_123.pdf",
  "notes": "Verification approved after review",
  "verified_by": "a1d2m3i4-5678-9012-a3b4-c5d6e7f8g9h0",
  "verified_at": "2025-10-16T11:30:00+05:30",
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T11:30:00+05:30"
}
```

### Get Pending Driver Verifications
Get all pending driver verifications.

**Endpoint:** `GET /driver-safety/verifications/pending`

**Response:**
```json
[
  {
    "id": "v1e2r3i4-f5i6-c7a8-t9i0-o1n2s3t4a5n6",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "verification_type": "vehicle_inspection",
    "status": "pending",
    "document_url": null,
    "notes": "Awaiting vehicle inspection",
    "verified_by": null,
    "verified_at": null,
    "created_at": "2025-10-16T10:00:00+05:30",
    "updated_at": "2025-10-16T10:00:00+05:30"
  }
]
```

## Driver Training Modules

### Create Driver Training Module
Create a new driver training module.

**Endpoint:** `POST /driver-safety/training-modules`

**Request Body:**
```json
{
  "title": "Defensive Driving Course",
  "description": "Comprehensive defensive driving techniques and safety practices",
  "duration_minutes": 120,
  "content_url": "https://example.com/training/defensive_driving",
  "is_mandatory": true
}
```

**Response:**
```json
{
  "id": "t1r2a3i4-n5i6-n7g8-m9o0-d1u2l3e4s5",
  "title": "Defensive Driving Course",
  "description": "Comprehensive defensive driving techniques and safety practices",
  "duration_minutes": 120,
  "content_url": "https://example.com/training/defensive_driving",
  "is_mandatory": true,
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T10:00:00+05:30"
}
```

### Get Driver Training Modules
Get all driver training modules.

**Endpoint:** `GET /driver-safety/training-modules`

**Response:**
```json
[
  {
    "id": "t1r2a3i4-n5i6-n7g8-m9o0-d1u2l3e4s5",
    "title": "Defensive Driving Course",
    "description": "Comprehensive defensive driving techniques and safety practices",
    "duration_minutes": 120,
    "content_url": "https://example.com/training/defensive_driving",
    "is_mandatory": true,
    "created_at": "2025-10-16T10:00:00+05:30",
    "updated_at": "2025-10-16T10:00:00+05:30"
  }
]
```

### Get Driver Training Module
Get a specific driver training module.

**Endpoint:** `GET /driver-safety/training-modules/{module_id}`

**Response:**
```json
{
  "id": "t1r2a3i4-n5i6-n7g8-m9o0-d1u2l3e4s5",
  "title": "Defensive Driving Course",
  "description": "Comprehensive defensive driving techniques and safety practices",
  "duration_minutes": 120,
  "content_url": "https://example.com/training/defensive_driving",
  "is_mandatory": true,
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T10:00:00+05:30"
}
```

### Update Driver Training Module
Update a driver training module.

**Endpoint:** `PUT /driver-safety/training-modules/{module_id}`

**Request Body:**
```json
{
  "title": "Advanced Defensive Driving Course",
  "description": "Advanced defensive driving techniques and safety practices",
  "duration_minutes": 180
}
```

**Response:**
```json
{
  "id": "t1r2a3i4-n5i6-n7g8-m9o0-d1u2l3e4s5",
  "title": "Advanced Defensive Driving Course",
  "description": "Advanced defensive driving techniques and safety practices",
  "duration_minutes": 180,
  "content_url": "https://example.com/training/defensive_driving",
  "is_mandatory": true,
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T11:00:00+05:30"
}
```

### Delete Driver Training Module
Delete a driver training module.

**Endpoint:** `DELETE /driver-safety/training-modules/{module_id}`

**Response:**
```json
{
  "message": "Driver training module deleted successfully"
}
```

## Driver Training Completions

### Create Driver Training Completion
Record a driver's completion of a training module.

**Endpoint:** `POST /driver-safety/training-completions`

**Request Body:**
```json
{
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "training_module_id": "t1r2a3i4-n5i6-n7g8-m9o0-d1u2l3e4s5",
  "score": 95.5,
  "certificate_url": "https://example.com/certificates/defensive_driving_123.pdf"
}
```

**Response:**
```json
{
  "id": "c1o2m3p4-l5e6-t7i8-o9n0-s1c2o3r4e5",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "training_module_id": "t1r2a3i4-n5i6-n7g8-m9o0-d1u2l3e4s5",
  "score": 95.5,
  "certificate_url": "https://example.com/certificates/defensive_driving_123.pdf",
  "completed_at": "2025-10-16T12:00:00+05:30",
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

### Get Driver Training Completions
Get all training completions for a driver.

**Endpoint:** `GET /driver-safety/training-completions/{driver_id}`

**Response:**
```json
[
  {
    "id": "c1o2m3p4-l5e6-t7i8-o9n0-s1c2o3r4e5",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "training_module_id": "t1r2a3i4-n5i6-n7g8-m9o0-d1u2l3e4s5",
    "score": 95.5,
    "certificate_url": "https://example.com/certificates/defensive_driving_123.pdf",
    "completed_at": "2025-10-16T12:00:00+05:30",
    "created_at": "2025-10-16T12:00:00+05:30"
  }
]
```

## Driver Incidents

### Create Driver Incident
Create a new driver incident report.

**Endpoint:** `POST /driver-safety/incidents`

**Request Body:**
```json
{
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "reporter_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "incident_type": "accident",
  "description": "Minor fender bender at intersection",
  "severity": "low"
}
```

**Response:**
```json
{
  "id": "i1n2c3i4-d5e6-n7t8-9012-r3p4o5r6t7",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "reporter_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "incident_type": "accident",
  "description": "Minor fender bender at intersection",
  "severity": "low",
  "status": "reported",
  "resolution_notes": null,
  "resolved_by": null,
  "resolved_at": null,
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T10:00:00+05:30"
}
```

### Get Driver Incidents
Get all incidents for a driver.

**Endpoint:** `GET /driver-safety/incidents/{driver_id}`

**Response:**
```json
[
  {
    "id": "i1n2c3i4-d5e6-n7t8-9012-r3p4o5r6t7",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "reporter_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "incident_type": "accident",
    "description": "Minor fender bender at intersection",
    "severity": "low",
    "status": "resolved",
    "resolution_notes": "Driver completed additional safety training",
    "resolved_by": "a1d2m3i4-5678-9012-a3b4-c5d6e7f8g9h0",
    "resolved_at": "2025-10-16T12:00:00+05:30",
    "created_at": "2025-10-16T10:00:00+05:30",
    "updated_at": "2025-10-16T12:00:00+05:30"
  }
]
```

### Get Pending Driver Incidents
Get all pending driver incidents.

**Endpoint:** `GET /driver-safety/incidents/pending`

**Response:**
```json
[
  {
    "id": "i1n2c3i4-d5e6-n7t8-9012-r3p4o5r6t7",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "reporter_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "incident_type": "complaint",
    "description": "Passenger complaint about driver behavior",
    "severity": "medium",
    "status": "reported",
    "resolution_notes": null,
    "resolved_by": null,
    "resolved_at": null,
    "created_at": "2025-10-16T10:00:00+05:30",
    "updated_at": "2025-10-16T10:00:00+05:30"
  }
]
```

### Update Driver Incident
Update a driver incident report.

**Endpoint:** `PUT /driver-safety/incidents/{incident_id}`

**Request Body:**
```json
{
  "status": "resolved",
  "resolution_notes": "Incident investigated and resolved with driver counseling",
  "resolved_by": "a1d2m3i4-5678-9012-a3b4-c5d6e7f8g9h0"
}
```

**Response:**
```json
{
  "id": "i1n2c3i4-d5e6-n7t8-9012-r3p4o5r6t7",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "reporter_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "incident_type": "complaint",
  "description": "Passenger complaint about driver behavior",
  "severity": "medium",
  "status": "resolved",
  "resolution_notes": "Incident investigated and resolved with driver counseling",
  "resolved_by": "a1d2m3i4-5678-9012-a3b4-c5d6e7f8g9h0",
  "resolved_at": "2025-10-16T11:00:00+05:30",
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T11:00:00+05:30"
}
```

## Driver Performance Metrics

### Create Driver Performance Metric
Create a new driver performance metric.

**Endpoint:** `POST /driver-safety/performance-metrics`

**Request Body:**
```json
{
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "metric_type": "punctuality",
  "score": 92.5,
  "period_start": "2025-10-01T00:00:00+05:30",
  "period_end": "2025-10-31T23:59:59+05:30",
  "notes": "Excellent punctuality record for October"
}
```

**Response:**
```json
{
  "id": "p1e2r3f4-o5r6-m7a8-n9c0-e1m2e3t4r5",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "metric_type": "punctuality",
  "score": 92.5,
  "period_start": "2025-10-01T00:00:00+05:30",
  "period_end": "2025-10-31T23:59:59+05:30",
  "notes": "Excellent punctuality record for October",
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Get Driver Performance Metrics
Get all performance metrics for a driver.

**Endpoint:** `GET /driver-safety/performance-metrics/{driver_id}`

**Response:**
```json
[
  {
    "id": "p1e2r3f4-o5r6-m7a8-n9c0-e1m2e3t4r5",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "metric_type": "punctuality",
    "score": 92.5,
    "period_start": "2025-10-01T00:00:00+05:30",
    "period_end": "2025-10-31T23:59:59+05:30",
    "notes": "Excellent punctuality record for October",
    "created_at": "2025-10-16T10:00:00+05:30"
  }
]
```

### Get Drivers by Performance Score
Get drivers within a performance score range.

**Endpoint:** `GET /driver-safety/performance-metrics/drivers/{min_score}/{max_score}`

**Response:**
```json
[
  {
    "id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "name": "John Smith",
    "email": "john.smith@example.com",
    "current_lat": 12.9716,
    "current_lon": 77.5946,
    "available": true,
    "rating": 4.8,
    "license_number": "DL123456789",
    "license_expiry_date": "2026-10-16T00:00:00+05:30",
    "vehicle_make": "Toyota",
    "vehicle_model": "Camry",
    "vehicle_year": 2020,
    "vehicle_registration": "KA01AB1234",
    "vehicle_insurance_expiry": "2026-05-16T00:00:00+05:30",
    "background_check_status": "approved",
    "safety_training_completed": true,
    "total_incidents": 0,
    "performance_score": 95.5
  }
]
```

## Ride Groups

### Create Ride Group
Create a new ride group for shared rides. Requires authentication.

**Endpoint:** `POST /ride-groups/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "name": "Office Commute Group",
  "estimated_fare": 25.50
}
```

**Response:**
```json
{
  "id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
  "name": "Office Commute Group",
  "creator_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "estimated_fare": 25.50,
  "status": "pending",
  "final_fare": null,
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T10:00:00+05:30"
}
```

### Get Ride Group
Get a ride group by ID. Requires authentication.

**Endpoint:** `GET /ride-groups/{group_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
  "name": "Office Commute Group",
  "creator_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "estimated_fare": 25.50,
  "status": "pending",
  "final_fare": null,
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T10:00:00+05:30"
}
```

### Update Ride Group
Update a ride group. Requires authentication.

**Endpoint:** `PUT /ride-groups/{group_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "name": "Updated Group Name",
  "status": "confirmed",
  "final_fare": 27.50
}
```

**Response:**
```json
{
  "id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
  "name": "Updated Group Name",
  "creator_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "estimated_fare": 25.50,
  "status": "confirmed",
  "final_fare": 27.50,
  "created_at": "2025-10-16T10:00:00+05:30",
  "updated_at": "2025-10-16T11:00:00+05:30"
}
```

### Delete Ride Group
Delete a ride group. Requires authentication.

**Endpoint:** `DELETE /ride-groups/{group_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "Ride group deleted successfully"
}
```

### Get User Ride Groups
Get all ride groups for the authenticated user. Requires authentication.

**Endpoint:** `GET /ride-groups/user`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
    "name": "Office Commute Group",
    "creator_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "estimated_fare": 25.50,
    "status": "pending",
    "final_fare": null,
    "created_at": "2025-10-16T10:00:00+05:30",
    "updated_at": "2025-10-16T10:00:00+05:30"
  }
]
```

## Ride Group Members

### Add Ride Group Member
Add a member to a ride group. Requires authentication.

**Endpoint:** `POST /ride-groups/members`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "ride_group_id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
  "user_id": "u2s3e4r5-6789-0123-b4c5-d6e7f8g9h0i1",
  "role": "member",
  "fare_share_percentage": 50
}
```

**Response:**
```json
{
  "id": "m1e2m3b4-e5r6-7890-g1h2-i3j4k5l6m7n8",
  "ride_group_id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
  "user_id": "u2s3e4r5-6789-0123-b4c5-d6e7f8g9h0i1",
  "role": "member",
  "fare_share_percentage": 50,
  "status": "invited",
  "invited_at": "2025-10-16T10:00:00+05:30",
  "accepted_at": null,
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Get Ride Group Members
Get all members of a ride group. Requires authentication.

**Endpoint:** `GET /ride-groups/members/{group_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "m1e2m3b4-e5r6-7890-g1h2-i3j4k5l6m7n8",
    "ride_group_id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
    "user_id": "u2s3e4r5-6789-0123-b4c5-d6e7f8g9h0i1",
    "role": "member",
    "fare_share_percentage": 50,
    "status": "invited",
    "invited_at": "2025-10-16T10:00:00+05:30",
    "accepted_at": null,
    "created_at": "2025-10-16T10:00:00+05:30"
  }
]
```

### Get Ride Group Member
Get a specific ride group member by ID. Requires authentication.

**Endpoint:** `GET /ride-groups/members/detail/{member_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": "m1e2m3b4-e5r6-7890-g1h2-i3j4k5l6m7n8",
  "ride_group_id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
  "user_id": "u2s3e4r5-6789-0123-b4c5-d6e7f8g9h0i1",
  "role": "member",
  "fare_share_percentage": 50,
  "status": "invited",
  "invited_at": "2025-10-16T10:00:00+05:30",
  "accepted_at": null,
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Update Ride Group Member
Update a ride group member. Requires authentication.

**Endpoint:** `PUT /ride-groups/members/{member_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "status": "accepted",
  "fare_share_percentage": 50
}
```

**Response:**
```json
{
  "id": "m1e2m3b4-e5r6-7890-g1h2-i3j4k5l6m7n8",
  "ride_group_id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
  "user_id": "u2s3e4r5-6789-0123-b4c5-d6e7f8g9h0i1",
  "role": "member",
  "fare_share_percentage": 50,
  "status": "accepted",
  "invited_at": "2025-10-16T10:00:00+05:30",
  "accepted_at": "2025-10-16T11:00:00+05:30",
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Remove Ride Group Member
Remove a member from a ride group. Requires authentication.

**Endpoint:** `DELETE /ride-groups/members/{member_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "Ride group member removed successfully"
}
```

### Get User Pending Invitations
Get all pending invitations for the authenticated user. Requires authentication.

**Endpoint:** `GET /ride-groups/invitations`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "m1e2m3b4-e5r6-7890-g1h2-i3j4k5l6m7n8",
    "ride_group_id": "r1i2d3e4-g5r6-o7u8-p9g1-r2o3u4p5s6i7",
    "user_id": "u2s3e4r5-6789-0123-b4c5-d6e7f8g9h0i1",
    "role": "member",
    "fare_share_percentage": 50,
    "status": "invited",
    "invited_at": "2025-10-16T10:00:00+05:30",
    "accepted_at": null,
    "created_at": "2025-10-16T10:00:00+05:30"
  }
]
```

## Emergency Contacts

### Create Emergency Contact
Create a new emergency contact for the authenticated user. Requires authentication.

**Endpoint:** `POST /emergency-contacts/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "+1234567890",
  "relationship": "Brother",
  "is_primary": true
}
```

**Response:**
```json
{
  "id": "e1m2e3r4-g5e6-n7c8-o9n0-t1a2c3t4s5u6",
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "name": "John Doe",
  "phone": "+1234567890",
  "relationship": "Brother",
  "is_primary": true,
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Get User Emergency Contacts
Get all emergency contacts for the authenticated user. Requires authentication.

**Endpoint:** `GET /emergency-contacts/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "e1m2e3r4-g5e6-n7c8-o9n0-t1a2c3t4s5u6",
    "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "name": "John Doe",
    "phone": "+1234567890",
    "relationship": "Brother",
    "is_primary": true,
    "created_at": "2025-10-16T10:00:00+05:30"
  }
]
```

### Get Primary Emergency Contact
Get the primary emergency contact for the authenticated user. Requires authentication.

**Endpoint:** `GET /emergency-contacts/primary`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": "e1m2e3r4-g5e6-n7c8-o9n0-t1a2c3t4s5u6",
  "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "name": "John Doe",
  "phone": "+1234567890",
  "relationship": "Brother",
  "is_primary": true,
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

## Referrals

### Create Referral
Create a referral for the authenticated user. Requires authentication.

**Endpoint:** `POST /referrals/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "referee_email": "friend@example.com"
}
```

**Response:**
```json
{
  "id": "r1e2f3e4-r5a6-l7s8-9012-r3f4e5r6r7a8",
  "referrer_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "referee_id": null,
  "referral_code": "ABC123DE",
  "status": "pending",
  "reward_points": 50,
  "created_at": "2025-10-16T10:00:00+05:30",
  "completed_at": null
}
```

### Get User Referrals
Get all referrals for the authenticated user. Requires authentication.

**Endpoint:** `GET /referrals/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "r1e2f3e4-r5a6-l7s8-9012-r3f4e5r6r7a8",
    "referrer_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "referee_id": null,
    "referral_code": "ABC123DE",
    "status": "pending",
    "reward_points": 50,
    "created_at": "2025-10-16T10:00:00+05:30",
    "completed_at": null
  }
]
```

### Get Referral by Code
Get a referral by its code.

**Endpoint:** `GET /referrals/code/{referral_code}`

**Response:**
```json
{
  "id": "r1e2f3e4-r5a6-l7s8-9012-r3f4e5r6r7a8",
  "referrer_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "referee_id": null,
  "referral_code": "ABC123DE",
  "status": "pending",
  "reward_points": 50,
  "created_at": "2025-10-16T10:00:00+05:30",
  "completed_at": null
}
```

### Complete Referral
Mark a referral as completed. Requires authentication.

**Endpoint:** `POST /referrals/{referral_id}/complete/{referee_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": "r1e2f3e4-r5a6-l7s8-9012-r3f4e5r6r7a8",
  "referrer_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "referee_id": "f1r2i3e4-5678-9012-a3b4-n5d6e7f8g9h0",
  "referral_code": "ABC123DE",
  "status": "completed",
  "reward_points": 50,
  "created_at": "2025-10-16T10:00:00+05:30",
  "completed_at": "2025-10-16T11:00:00+05:30"
}
```

## Chat

### Create Chat Message
Create a chat message for the authenticated user. Requires authentication.

**Endpoint:** `POST /chat/`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "message": "Hi, I'm at the pickup location"
}
```

**Response:**
```json
{
  "id": "c1h2a3t4-5678-9012-a3b4-m5e6s7s8a9g0",
  "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "sender_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "sender_type": "rider",
  "message": "Hi, I'm at the pickup location",
  "is_read": false,
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Get Chat Messages
Get all chat messages for a ride. Requires authentication.

**Endpoint:** `GET /chat/{ride_id}`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "c1h2a3t4-5678-9012-a3b4-m5e6s7s8a9g0",
    "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
    "sender_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "sender_type": "rider",
    "message": "Hi, I'm at the pickup location",
    "is_read": false,
    "created_at": "2025-10-16T10:00:00+05:30"
  }
]
```

### Mark Message as Read
Mark a chat message as read. Requires authentication.

**Endpoint:** `POST /chat/{message_id}/read`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": "c1h2a3t4-5678-9012-a3b4-m5e6s7s8a9g0",
  "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "sender_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "sender_type": "rider",
  "message": "Hi, I'm at the pickup location",
  "is_read": true,
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

## Emergency SOS

### Trigger Emergency SOS
Trigger an emergency SOS for the authenticated user. Requires authentication.

**Endpoint:** `POST /sos/trigger`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "ride_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "message": "Emergency! Need help immediately."
}
```

**Response:**
```json
{
  "message": "Emergency SOS triggered successfully",
  "emergency_contact_notified": true,
  "location_shared": true
}
```


}