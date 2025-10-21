from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .routes import (
    auth, riders, drivers, matching, metrics, rides, tracking, ratings, 
    notifications, analytics, schedules, pricing, scheduled_rides, 
    wallet, loyalty, analytics_simple, emergency_contacts, referrals, chat, sos, ride_groups, driver_safety, subscriptions
)
from .utils.jwt_utils import verify_token
from .utils.auth_utils import oauth2_scheme, get_current_user

app = FastAPI(
    title="FairRide API",
    description="""A preference-driven ride scheduling system with fairness-optimized algorithms.

FairRide is a ride-matching system that uses fairness-optimized scheduling algorithms instead of plain nearest-driver matching. Built with FastAPI, Supabase, and SendGrid.

## Features
- **Preference-Driven Matching**: Riders can specify preferred departure and arrival times
- **Fairness-Optimized Algorithms**: Implements RGA, RGA++, and Iterative Voting algorithms
- **Real-time Notifications**: Email notifications for ride assignments
- **Metrics Dashboard**: Monitor fairness and efficiency metrics
- **JWT Authentication**: Secure API access with JSON Web Tokens
- **Real-time Tracking**: Live ride tracking capabilities
- **Ratings and Reviews**: Driver rating system
- **Analytics**: Comprehensive system and user analytics
- **Schedule Management**: Store and retrieve historical scheduling results
- **Dynamic Pricing**: Real-time fare estimation with surge pricing
- **Scheduled Rides**: Book future rides in advance
- **Wallet System**: In-app credits and transactions
- **Loyalty Program**: Points and rewards for frequent users

## API Documentation
For detailed API documentation with request/response examples, see [apidocs.md](../apidocs.md)

## Algorithms
- **RGA (Randomized Greedy Algorithm)**: Basic randomized greedy approach
- **RGA++**: Enhanced version of RGA with improved fairness
- **Iterative Voting (IV)**: Consensus-based matching algorithm

## Getting Started
1. Sign up as a user, rider or driver
2. Submit ride requests with preferences
3. Run matching algorithms to generate assignments
4. View fairness metrics to evaluate system performance""",
    version="1.0.0",
    contact={
        "name": "FairRide Team",
        "url": "https://github.com/fairride",
        "email": "support@fairride.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(riders.router, prefix="/riders", tags=["Riders"])
app.include_router(drivers.router, prefix="/drivers", tags=["Drivers"])
app.include_router(matching.router, prefix="/match", tags=["Matching"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(rides.router, prefix="/rides", tags=["Rides"])
app.include_router(tracking.router, prefix="/tracking", tags=["Real-time Tracking"])
app.include_router(ratings.router, prefix="/ratings", tags=["Ratings and Reviews"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(schedules.router, prefix="/schedules", tags=["Schedule Management"])
app.include_router(pricing.router, prefix="/pricing", tags=["Pricing"])
app.include_router(scheduled_rides.router, prefix="/scheduled-rides", tags=["Scheduled Rides"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(loyalty.router, prefix="/loyalty", tags=["Loyalty Program"])
app.include_router(analytics_simple.router, prefix="/analytics-simple", tags=["Simple Analytics"])
app.include_router(emergency_contacts.router, prefix="/emergency-contacts", tags=["Emergency Contacts"])
app.include_router(referrals.router, prefix="/referrals", tags=["Referrals"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(sos.router, prefix="/sos", tags=["Emergency SOS"])
app.include_router(ride_groups.router, prefix="/ride-groups", tags=["Ride Groups"])
app.include_router(driver_safety.router, prefix="/driver-safety", tags=["Driver Safety"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])

@app.get("/")
async def root():
    """
    Welcome endpoint
    
    Returns a welcome message for the FairRide API.
    
    ## Response
    - **message**: Welcome message string
    """
    return {"message": "Welcome to FairRide API - A fairness-optimized ride scheduling system"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns the health status of the API.
    
    ## Response
    - **status**: Health status string ("healthy" when operational)
    """
    return {"status": "healthy"}