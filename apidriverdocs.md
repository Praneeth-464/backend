# FairRide Driver API Documentation

A preference-driven ride scheduling system with fairness-optimized algorithms - Driver Endpoints.

## Overview

In the FairRide system, there are three distinct user roles:
- **Users**: Basic accounts that can sign up and authenticate
- **Riders**: Users who request rides with specific preferences
- **Drivers**: Users who provide rides to riders

This documentation focuses on the API endpoints available to drivers. Drivers must first register as users, then create a driver profile to access driver-specific functionality.

The relationship between these entities is:
1. A **User** creates an account with basic authentication credentials
2. A **User** can then create either a **Rider** profile or a **Driver** profile (or both)
3. **Riders** request rides with preferences
4. **Drivers** fulfill ride requests
5. The matching system pairs riders with drivers using fairness-optimized algorithms

## How Matching Works

The FairRide system uses fairness-optimized algorithms to match riders with drivers:

1. **Rider Requests a Ride**: A rider submits a request with preferences (origin, destination, timing)
2. **Driver Availability**: Drivers update their location and availability status
3. **Automatic Matching**: When a rider requests a ride, the system automatically runs a matching algorithm
4. **Assignment Creation**: The algorithm creates assignments based on factors like distance, timing preferences, and fairness metrics
5. **Notification**: Both rider and driver are notified of their match

Drivers will receive notifications when they are assigned to a ride. They can then accept the ride and proceed with pickup and dropoff.

## Authentication

Most driver endpoints require authentication using JWT tokens. To authenticate:

1. Sign up as a user using `POST /auth/signup/user`
2. Log in using `POST /auth/login` to obtain a JWT token
3. Include the token in the Authorization header for subsequent requests:
   ```
   Authorization: Bearer <JWT_TOKEN>
   ```

## Driver Registration & Profile Management

### Register Driver
Register a new driver profile. Validates that the email exists in the users table.

**Endpoint:** `POST /drivers/`

**Request Body:**
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "license_number": "DL1234567890",
  "vehicle_make": "Toyota",
  "vehicle_model": "Camry",
  "vehicle_year": 2020,
  "vehicle_registration": "KA01AB1234"
}
```

**Response:**
```json
{
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 5.0,
  "id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "background_check_status": "pending",
  "safety_training_completed": false,
  "total_incidents": 0,
  "performance_score": 100.0,
  "license_number": "DL1234567890",
  "license_expiry_date": null,
  "vehicle_make": "Toyota",
  "vehicle_model": "Camry",
  "vehicle_year": 2020,
  "vehicle_registration": "KA01AB1234",
  "vehicle_insurance_expiry": null
}
```

**Note:** No JWT token is required for this endpoint. The system will automatically update the user's role to 'driver' upon successful registration.

### Get Driver by ID
Retrieve a specific driver by ID.

**Endpoint:** `GET /drivers/{driver_id}`

**Response:**
```json
{
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
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
}
```

### Get Current Driver Profile
Retrieve the driver profile for the currently authenticated user.

**Endpoint:** `GET /drivers/me`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
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
}
```

### Update Current Driver Profile
Update the driver profile for the currently authenticated user.

**Endpoint:** `PUT /drivers/me`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "license_number": "DL1234567890",
  "vehicle_make": "Toyota",
  "vehicle_model": "Camry",
  "vehicle_year": 2020,
  "vehicle_registration": "KA01AB1234"
}
```

**Response:**
```json
{
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
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
}
```

### Delete Current Driver Profile
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

## Driver Location Management

### Update Driver Location
Update driver's current location and availability status.

**Endpoint:** `POST /drivers/{driver_id}/location`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true
}
```

**Response:**
```json
{
  "message": "Location updated successfully"
}
```

## Ride Management

### Get Driver Rides
Retrieve all rides for the authenticated driver.

**Endpoint:** `GET /drivers/me/rides`

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
    "algorithm": "RGA",
    "start_time": "2025-10-16T14:15:00+05:30",
    "end_time": "2025-10-16T14:45:00+05:30",
    "fare": 125.50,
    "utility": 0.85,
    "status": "completed"
  }
]
```

### Get Rides by Driver ID
Get all rides for a specific driver by driver ID.

**Endpoint:** `GET /drivers/{driver_id}/rides`

**Response:**
```json
[
  {
    "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
    "user_id": "u1s2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
    "rider_id": "m8n7k6j5-i4h3-2109-g8f7-e6d5c4b3a2z1",
    "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "algorithm": "RGA",
    "start_time": "2025-10-16T14:15:00+05:30",
    "end_time": "2025-10-16T14:45:00+05:30",
    "fare": 125.50,
    "utility": 0.85,
    "status": "completed"
  }
]
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

## Earnings & Ratings

### Get Driver Earnings
Retrieve earnings information for the authenticated driver.

**Endpoint:** `GET /drivers/me/earnings`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "total_earnings": 1250.75,
  "total_rides": 25,
  "average_earnings_per_ride": 50.03,
  "this_month_earnings": 420.50,
  "this_week_earnings": 150.25
}
```

### Get Driver Ratings
Retrieve ratings and reviews for the authenticated driver.

**Endpoint:** `GET /drivers/me/ratings`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "average_rating": 4.8,
  "total_ratings": 25,
  "reviews": [
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
  ]
}
```

## Notifications

### Get Current Driver Notifications
Get notifications for the currently authenticated driver.

**Endpoint:** `GET /drivers/me/notifications`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
[
  {
    "id": "n1o2t3i4-5678-9012-a3b4-c5d6e7f8g9h0",
    "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
    "title": "Ride Assigned",
    "message": "Your ride has been assigned to rider Alice Johnson",
    "type": "ride_assignment",
    "read": false,
    "created_at": "2025-10-16T14:10:00+05:30"
  }
]
```

### Mark Current Driver Notification as Read
Mark a notification as read for the currently authenticated driver.

**Endpoint:** `POST /drivers/me/notifications/{notification_id}/read`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": "n1o2t3i4-5678-9012-a3b4-c5d6e7f8g9h0",
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "title": "Ride Assigned",
  "message": "Your ride has been assigned to rider Alice Johnson",
  "type": "ride_assignment",
  "read": true,
  "created_at": "2025-10-16T14:10:00+05:30"
}
```

### Accept Ride Assignment
Accept a ride assignment as the currently authenticated driver.

**Endpoint:** `POST /drivers/me/rides/{ride_id}/accept`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rider_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "algorithm": "RGA++",
  "start_time": "2025-10-16T14:15:00+05:30",
  "end_time": "2025-10-16T14:45:00+05:30",
  "fare": 125.50,
  "utility": 0.85,
  "status": "accepted",
  "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0"
}
```

### Reject Ride Assignment
Reject a ride assignment as the currently authenticated driver.

**Endpoint:** `POST /drivers/me/rides/{ride_id}/reject`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rider_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "algorithm": "RGA++",
  "start_time": "2025-10-16T14:15:00+05:30",
  "end_time": "2025-10-16T14:45:00+05:30",
  "fare": 125.50,
  "utility": 0.85,
  "status": "rejected",
  "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0"
}
```

### Start Ride
Start a ride as the currently authenticated driver. This endpoint can only be called for rides that have been accepted.

**Endpoint:** `POST /drivers/me/rides/{ride_id}/start`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "rider_id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "algorithm": "RGA++",
  "start_time": "2025-10-16T14:15:00+05:30",
  "end_time": "2025-10-16T14:45:00+05:30",
  "fare": 125.50,
  "utility": 0.85,
  "status": "started",
  "id": "r1i2d3e4-5678-9012-a3b4-c5d6e7f8g9h0"
}
```

### Get Notifications by Driver ID
Get notifications for a specific driver by driver ID.

**Endpoint:** `GET /drivers/{driver_id}/notifications`

**Response:**
```json
[
  {
    "id": "n1o2t3i4-5678-9012-a3b4-c5d6e7f8g9h0",
    "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
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

**Endpoint:** `POST /drivers/me/notifications/{notification_id}/read`

**Response:**
```json
{
  "id": "n1o2t3i4-5678-9012-a3b4-c5d6e7f8g9h0",
  "user_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "title": "New Ride Request",
  "message": "You have a new ride request from Alice Johnson",
  "type": "ride_request",
  "read": true,
  "created_at": "2025-10-16T14:10:00+05:30"
}
```

## Safety Features

### Add Emergency Contact
Add an emergency contact for the driver.

**Endpoint:** `POST /drivers/me/safety/emergency-contact`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**
```json
{
  "name": "Jane Smith",
  "phone": "+1234567890",
  "relationship": "Spouse"
}
```

**Response:**
```json
{
  "id": "e1m2e3r4-5678-9012-a3b4-c5d6e7f8g9h0",
  "driver_id": "d1r2i3v4-5678-9012-a3b4-c5d6e7f8g9h0",
  "name": "Jane Smith",
  "phone": "+1234567890",
  "relationship": "Spouse",
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### Trigger SOS
Trigger an SOS alert to emergency contacts and authorities.

**Endpoint:** `POST /drivers/me/safety/sos`

**Headers:**
```json
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "SOS alert sent successfully",
  "alert_id": "s1o2s3a4-5678-9012-a3b4-c5d6e7f8g9h0"
}