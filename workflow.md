# FairRide Mobile App Integration Workflow

A comprehensive guide for mobile app developers to integrate with the FairRide backend API and design an intuitive user interface.

## Table of Contents
1. [Overview](#overview)
2. [User Registration & Authentication Flow](#user-registration--authentication-flow)
3. [Rider App Workflow](#rider-app-workflow)
4. [Driver App Workflow](#driver-app-workflow)
5. [Core Features Implementation](#core-features-implementation)
6. [Safety & Emergency Features](#safety--emergency-features)
7. [Communication Features](#communication-features)
8. [Shared Rides & Ride Groups](#shared-rides--ride-groups)
9. [Driver Safety & Verification](#driver-safety--verification)
10. [UI/UX Design Guidelines](#uiux-design-guidelines)
11. [API Integration Patterns](#api-integration-patterns)
12. [Error Handling & Offline Support](#error-handling--offline-support)
13. [Push Notifications](#push-notifications)
14. [Security Considerations](#security-considerations)

## Overview

The FairRide mobile app provides a comprehensive ride-sharing experience with fairness-optimized algorithms. The app consists of two main components:
- **Rider App**: For users requesting rides
- **Driver App**: For drivers accepting and completing rides

Both apps share common features like authentication, notifications, and analytics, but have distinct workflows tailored to their respective roles.

## User Registration & Authentication Flow

### 1. User Registration
```
Mobile App Action: User taps "Sign Up"
API Endpoint: POST /auth/signup/user
Request Body:
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
Expected Response:
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "user",
  "created_at": "2025-10-16T10:00:00+05:30"
}
```

### 2. Email Verification
```
Mobile App Action: User receives verification email and clicks link
API Endpoint: GET /auth/verify-email?token={verification_token}
Expected Response:
{
  "message": "Email verified successfully. You can now log in to your account."
}
```

### 3. User Login
```
Mobile App Action: User enters credentials and taps "Login"
API Endpoint: POST /auth/login
Request Body (form-urlencoded):
username: john.doe@example.com
password: securepassword123
Expected Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4. Get User Profile
```
Mobile App Action: App retrieves user profile after login
API Endpoint: GET /auth/profile
Headers:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Expected Response:
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

### 5. Logout
```
Mobile App Action: User taps "Logout"
API Endpoint: POST /auth/logout
Headers:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Expected Response:
{
  "message": "Successfully logged out"
}
```

## Rider App Workflow

### 1. Home Screen
**UI Elements:**
- Current location display with address
- Destination input field with autocomplete
- Quick destination buttons (Home, Work, etc.)
- Ride preferences panel
- "Book Ride" button

**API Integration:**
```
On App Start:
GET /riders/{rider_id}
Purpose: Load rider profile and preferences

On Location Change:
POST /riders/request (if booking)
Purpose: Submit ride request with current location
```

### 2. Ride Request Flow

**Step 1: Set Pickup/Dropoff**
```
Mobile App Action: User sets pickup and destination
API Endpoint: POST /pricing/estimate
Request Body:
{
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "rider_beta": 0.7
}
Expected Response:
{
  "estimated_fare": 15.75,
  "distance_km": 8.2,
  "estimated_duration_minutes": 16.4
}
```

**Step 2: Set Preferences**
```
Mobile App UI: Preference selection panel
Options:
- Driver rating threshold
- Ride type (solo, shared, premium)
- Accessibility needs
- Preferred departure/arrival times
```

**Step 3: Confirm Booking**
```
Mobile App Action: User confirms ride
API Endpoint: POST /riders/request
Request Body:
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "origin_lat": 12.9716,
  "origin_lon": 77.5946,
  "destination_lat": 13.0358,
  "destination_lon": 77.5970,
  "preferred_departure": "2025-10-16T14:00:00+05:30",
  "beta": 0.7
}
Expected Response:
{
  "id": "rider_uuid",
  "status": "waiting",
  "created_at": "2025-10-16T12:00:00+05:30"
}
```

### 3. Ride Tracking
```
Mobile App Action: Real-time ride tracking
API Endpoint: GET /tracking/rides/{ride_id}
Expected Response:
{
  "ride_id": "ride_uuid",
  "driver_location": {
    "lat": 12.9716,
    "lon": 77.5946
  },
  "estimated_arrival": "2025-10-16T14:15:00+05:30",
  "distance_to_pickup": 1.2,
  "eta_dropoff": "2025-10-16T14:45:00+05:30"
}

Background Updates:
WebSocket or polling every 10 seconds
```

### 4. Ride Completion & Rating
```
Mobile App Action: Ride completed
API Endpoint: POST /riders/{rider_id}/rides/{ride_id}/rate
Request Body:
{
  "rating": 5,
  "review": "Great driver!",
  "tip": 10.0
}
Expected Response:
{
  "id": "rating_uuid",
  "rating": 5,
  "review": "Great driver!",
  "tip": 10.0
}
```

## Driver App Workflow

### 1. Driver Registration
```
Mobile App Action: New driver signs up
API Endpoint: POST /auth/signup/driver
Request Body:
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 4.8
}
Expected Response:
{
  "id": "driver_uuid",
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true,
  "rating": 4.8
}
```

### 2. Driver Availability Management
```
Mobile App Action: Toggle availability
API Endpoint: POST /drivers/{driver_id}/location
Request Body:
{
  "current_lat": 12.9716,
  "current_lon": 77.5946,
  "available": true
}
Expected Response:
{
  "message": "Location updated successfully"
}
```

### 3. Ride Assignment Notification
```
Mobile App Action: Receive ride assignment
API Endpoint: GET /drivers/{driver_id}/notifications
Expected Response:
[
  {
    "id": "notification_uuid",
    "title": "New Ride Request",
    "message": "You have a new ride request from John Doe",
    "type": "ride_request",
    "read": false
  }
]

Mobile App Action: Accept ride
API Endpoint: Not directly available - handled by matching algorithm
Next Step: Start tracking ride
```

### 4. Ride Tracking & Navigation
```
Mobile App Action: Track ride progress
API Endpoint: GET /tracking/rides/{ride_id}
Purpose: Show rider location and ETA

Mobile App Action: Update location
API Endpoint: POST /tracking/drivers/{driver_id}/location
Request Body:
{
  "lat": 12.9716,
  "lon": 77.5946,
  "speed": 30.5,
  "heading": 45.0
}
Expected Response:
{
  "message": "Location updated successfully"
}
```

### 5. Ride Completion
```
Mobile App Action: Mark ride as completed
API Endpoint: Not directly available - handled by system
Next Step: Receive rating from rider
```

## Core Features Implementation

### 1. Dynamic Pricing
```
Mobile App Integration:
- Show fare estimate before booking
- Display surge pricing notifications
- Explain pricing factors to users

API Endpoint: POST /pricing/estimate
UI Display: 
- Base fare breakdown
- Distance/time components
- Surge multiplier indicator
```

### 2. Scheduled Rides
```
Mobile App Integration:
- Calendar view for scheduling
- Recurring ride setup
- Reminder notifications

API Endpoints:
POST /scheduled-rides/ - Create scheduled ride
GET /scheduled-rides/rider/{rider_id} - List scheduled rides
PUT /scheduled-rides/{ride_id}/status/{status} - Update status
```

### 3. Wallet System
```
Mobile App Integration:
- Wallet balance display
- Transaction history
- In-app credit purchases

API Endpoints:
GET /wallet/balance/{user_id} - Get balance
POST /wallet/transaction - Add/remove funds
GET /wallet/transactions/{user_id} - Get history
```

### 4. Loyalty Program
```
Mobile App Integration:
- Points balance display
- Level progress indicator
- Rewards catalog

API Endpoints:
GET /loyalty/{user_id} - Get loyalty info
POST /loyalty/points - Update points
```

### 5. Analytics Dashboard
```
Mobile App Integration:
- Personal ride statistics
- Spending patterns
- Favorite destinations

API Endpoints:
GET /analytics-simple/user/{user_id} - Get user analytics
POST /analytics-simple/user - Get filtered analytics
```

## Safety & Emergency Features

### 1. Emergency Contacts
```
Mobile App Integration:
- Add and manage emergency contacts
- Set primary emergency contact
- Quick access to emergency contacts during rides

API Endpoints:
POST /emergency-contacts/ - Create emergency contact
GET /emergency-contacts/{user_id} - Get all emergency contacts
GET /emergency-contacts/{user_id}/primary - Get primary emergency contact
```

### 2. Emergency SOS
```
Mobile App Integration:
- One-touch emergency button
- Automatic notification to emergency contacts
- Real-time location sharing

API Endpoint:
POST /sos/trigger - Trigger emergency SOS
```

### 3. Trip Sharing
```
Mobile App Integration:
- Share trip details with friends/family
- Real-time location tracking
- Estimated arrival notifications

Implementation:
- Generate shareable trip link
- Send notifications to shared contacts
- Update location in real-time
```

## Communication Features

### 1. In-App Chat
```
Mobile App Integration:
- Real-time messaging between rider and driver
- Message history for ongoing rides
- Read status indicators

API Endpoints:
POST /chat/ - Send message
GET /chat/{ride_id} - Get chat history
POST /chat/{message_id}/read - Mark message as read
```

### 2. Contact Masking
```
Mobile App Integration:
- Privacy-protected phone number sharing
- In-app calling without revealing personal numbers
- SMS messaging through the app

Implementation:
- Generate temporary virtual numbers
- Route calls/SMS through the app
- Expire numbers after ride completion
```

### 3. Push Notifications
```
Mobile App Integration:
- Real-time message notifications
- Background message handling
- Notification preferences

Implementation:
- Firebase Cloud Messaging (FCM) for Android
- Apple Push Notification Service (APNs) for iOS
- Custom notification handling
```

## Shared Rides & Ride Groups

### 1. Ride Group Creation
```
Mobile App Integration:
- Create ride groups for shared rides
- Invite friends to join ride groups
- Set fare sharing percentages

API Endpoints:
POST /ride-groups/ - Create ride group
GET /ride-groups/user/{user_id} - Get user's ride groups
PUT /ride-groups/{group_id} - Update ride group
```

### 2. Group Member Management
```
Mobile App Integration:
- Invite members to ride groups
- Accept/decline ride group invitations
- Manage member roles and fare shares

API Endpoints:
POST /ride-groups/members - Add member to ride group
GET /ride-groups/members/{group_id} - Get ride group members
PUT /ride-groups/members/{member_id} - Update member status
DELETE /ride-groups/members/{member_id} - Remove member
GET /ride-groups/invitations/{user_id} - Get pending invitations
```

### 3. Shared Ride Booking
```
Mobile App Integration:
- Book rides for entire ride groups
- Split fare calculations
- Group ride tracking

Implementation:
- Select ride group for booking
- Confirm fare sharing percentages
- Track all group members during ride
```

### 4. Fair Cost Distribution
```
Mobile App Integration:
- Display individual fare shares
- Show total group fare
- Process payments from multiple users

Algorithm Implementation:
- Equal split by default
- Custom percentage splits
- Dynamic adjustment based on distance
```

## Driver Safety & Verification

### 1. Driver Background Checks
```
Admin Panel Integration:
- Submit driver background check requests
- Review and approve/reject background checks
- Maintain driver verification records

API Endpoints:
POST /driver-safety/verifications - Create verification record
GET /driver-safety/verifications/{driver_id} - Get driver verifications
PUT /driver-safety/verifications/{verification_id} - Update verification
GET /driver-safety/verifications/pending - Get pending verifications
```

### 2. Vehicle Inspection Process
```
Admin Panel Integration:
- Schedule vehicle inspections
- Record inspection results
- Track vehicle maintenance status

Implementation:
- Digital inspection forms
- Photo/document upload capabilities
- Automated reminders for upcoming inspections
```

### 3. Driver Safety Training
```
Driver App Integration:
- Access mandatory training modules
- Complete training courses
- View training certificates

Admin Panel Integration:
- Create and manage training modules
- Track driver training completion
- Generate training reports

API Endpoints:
POST /driver-safety/training-modules - Create training module
GET /driver-safety/training-modules - Get all training modules
POST /driver-safety/training-completions - Record training completion
GET /driver-safety/training-completions/{driver_id} - Get driver training history
```

### 4. Incident Reporting and Resolution
```
Driver/Rider App Integration:
- Report incidents through the app
- View incident status and resolution

Admin Panel Integration:
- Review incident reports
- Investigate and resolve incidents
- Maintain incident records

API Endpoints:
POST /driver-safety/incidents - Create incident report
GET /driver-safety/incidents/{driver_id} - Get driver incidents
PUT /driver-safety/incidents/{incident_id} - Update incident status
GET /driver-safety/incidents/pending - Get pending incidents
```

### 5. Driver Performance Monitoring
```
Admin Panel Integration:
- Monitor driver performance metrics
- Identify high-risk drivers
- Provide feedback and coaching

API Endpoints:
POST /driver-safety/performance-metrics - Create performance metric
GET /driver-safety/performance-metrics/{driver_id} - Get driver metrics
GET /driver-safety/performance-metrics/drivers/{min_score}/{max_score} - Get drivers by performance
```

## UI/UX Design Guidelines

### Color Scheme
- **Primary**: #1a73e8 (Blue) - Trust and reliability
- **Secondary**: #34a853 (Green) - Success and safety
- **Accent**: #ea4335 (Red) - Urgency and alerts
- **Background**: #f8f9fa (Light gray) - Clean and modern

### Navigation Patterns
1. **Bottom Navigation Bar** (5 items max)
   - Home
   - Rides
   - Wallet
   - Notifications
   - Profile

2. **Hamburger Menu** (For less frequent actions)
   - Settings
   - Help & Support
   - About
   - Logout

### Key Screens

#### Rider App Screens
1. **Home Screen**
   - Location search with autocomplete
   - Quick destinations
   - Recent rides
   - Current ride status

2. **Ride Booking Screen**
   - Map view with route
   - Fare estimate
   - Preferences panel
   - Schedule options

3. **Ride Tracking Screen**
   - Live map with driver/rider positions
   - ETA countdown
   - Driver info card
   - Emergency button

4. **Ride History Screen**
   - List of past rides
   - Filter by date/rating
   - Detailed ride info

#### Driver App Screens
1. **Dashboard Screen**
   - Availability toggle
   - Current location
   - Earnings summary
   - Active ride status

2. **Ride Assignment Screen**
   - Rider details
   - Pickup/dropoff locations
   - Estimated fare
   - Accept/decline buttons

3. **Navigation Screen**
   - Turn-by-turn directions
   - Rider contact info
   - ETA to pickup/dropoff

4. **Earnings Screen**
   - Daily/weekly/monthly earnings
   - Trip history
   - Payment information

5. **Safety & Verification Screen**
   - Background check status
   - Training completion status
   - Incident history
   - Performance metrics

## API Integration Patterns

### 1. Authentication
```
Implementation:
- Store JWT token in secure storage
- Attach to all API requests in Authorization header
- Handle token expiration with refresh mechanism
- Redirect to login on 401 responses
```

### 2. Real-time Updates
```
Implementation Options:
1. WebSocket connections for tracking updates
2. Polling (10-second intervals) for status changes
3. Push notifications for important events
```

### 3. Data Caching
```
Implementation:
- Cache user profile data
- Store recent locations/searches
- Cache fare estimates
- Offline support for basic functions
```

### 4. Error Handling
```
Implementation:
- Network error detection
- Retry mechanisms with exponential backoff
- User-friendly error messages
- Graceful degradation for offline mode
```

## Error Handling & Offline Support

### Common Error Scenarios
1. **Network Disconnection**
   - Queue requests for retry
   - Show offline indicator
   - Allow limited functionality

2. **API Errors**
   - 400: Bad request - Show validation errors
   - 401: Unauthorized - Redirect to login
   - 404: Not found - Show appropriate message
   - 500: Server error - Show generic error and retry

3. **Location Services Unavailable**
   - Prompt user to enable location
   - Allow manual address entry
   - Use last known location

### Offline Support Features
1. **Rider App**
   - View ride history
   - Access saved locations
   - Modify profile settings
   - Schedule rides for later

2. **Driver App**
   - View earnings history
   - Update profile information
   - Review past ratings
   - Set availability preferences
   - View safety training materials (cached)

## Push Notifications

### Notification Types

#### For Riders
1. **Ride Assigned**
   - Title: "Driver Assigned"
   - Message: "Your ride with [Driver Name] is on the way"
   - Action: Open tracking screen

2. **Driver Arrival**
   - Title: "Driver Arrived"
   - Message: "[Driver Name] has arrived at your pickup location"
   - Action: Open tracking screen

3. **Ride Reminder**
   - Title: "Upcoming Ride"
   - Message: "Your scheduled ride is in 30 minutes"
   - Action: Open ride details

#### For Drivers
1. **New Ride Request**
   - Title: "New Ride Request"
   - Message: "Ride request from [Rider Name]"
   - Action: Open assignment screen

2. **Ride Cancellation**
   - Title: "Ride Cancelled"
   - Message: "Your ride has been cancelled by the rider"
   - Action: Return to dashboard

3. **Payment Received**
   - Title: "Payment Received"
   - Message: "You've received $[amount] for your ride"
   - Action: Open earnings screen

4. **Safety Notifications**
   - Title: "Safety Training Due"
   - Message: "Your mandatory safety training is due"
   - Action: Open training module

5. **Incident Notifications**
   - Title: "Incident Report Filed"
   - Message: "An incident report has been filed regarding your recent ride"
   - Action: Open incident details

### Implementation
```
Mobile App Integration:
- Register for push notifications on app start
- Handle notification taps to navigate to appropriate screens
- Show in-app notification center
- Allow notification preferences in settings
```

## Security Considerations

### 1. Data Protection
- Encrypt sensitive data at rest
- Use HTTPS for all API communications
- Implement proper authentication/authorization
- Sanitize user inputs to prevent injection attacks

### 2. Location Privacy
- Only collect location when necessary
- Provide clear privacy policy
- Allow users to control location sharing
- Anonymize location data in analytics

### 3. Payment Security
- Use secure payment gateways
- Never store payment credentials
- Implement PCI compliance measures
- Provide transaction receipts

### 4. Account Security
- Implement strong password requirements
- Enable two-factor authentication
- Monitor for suspicious activity
- Provide account recovery options

### 5. Document Security
- Secure storage of verification documents
- Access controls for sensitive information
- Audit trails for document access
- Regular security assessments

## Conclusion

This workflow document provides a comprehensive guide for developing the FairRide mobile applications. By following these guidelines, developers can create intuitive, secure, and feature-rich mobile experiences that fully leverage the backend API's capabilities. The modular approach allows for iterative development and easy maintenance while ensuring a consistent user experience across both rider and driver applications.