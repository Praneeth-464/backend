# FairRide – A Preference-Driven Ride Scheduling System

## Overview

FairRide is a ride-matching system that uses fairness-optimized scheduling algorithms instead of plain nearest-driver matching. Built with FastAPI, Supabase, and SendGrid.

## Features

- **Auth Service**: Handles login/signup with JWT token authentication
- **Rider Service**: Riders submit ride requests + preferences
- **Driver Service**: Drivers share availability + location
- **Matching Service**: Runs RGA/RGA++/IV algorithms to assign riders ↔ drivers
- **Schedule Management**: Store and retrieve historical scheduling results
- **Metrics Service**: Calculates fairness & efficiency metrics (Gini, SW)
- **Notifications Service**: Sends emails via SendGrid for booking confirmations
- **JWT Authentication**: Secure API access with JSON Web Tokens
- **Real-time Tracking**: Live ride tracking capabilities
- **Ratings and Reviews**: Driver rating system
- **Analytics**: Comprehensive system and user analytics
- **Dynamic Pricing**: Real-time fare estimation with surge pricing
- **Scheduled Rides**: Book future rides in advance
- **Wallet System**: In-app credits and transactions
- **Loyalty Program**: Points and rewards for frequent users
- **Safety Features**: Emergency contacts and SOS functionality
- **Communication**: In-app chat between riders and drivers
- **Shared Rides**: Split rides with fare distribution algorithms
- **Driver Safety**: Background checks, vehicle inspection, and safety training
- **Incident Management**: Reporting and resolution system
- **Performance Monitoring**: Driver performance tracking and feedback

## Tech Stack

- Backend: FastAPI
- Database: Supabase (PostgreSQL)
- Authentication: Supabase Auth
- Email Service: SendGrid
- Location Services: Google Maps / OpenStreetMap

## Algorithms

- **RGA (Randomized Greedy Algorithm)**: Basic randomized greedy approach
- **RGA++**: Enhanced version of RGA with improved fairness
- **Iterative Voting (IV)**: Consensus-based matching algorithm

## Getting Started

### Prerequisites

- Python 3.8+
- Supabase account
- SendGrid account

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fairride.git
   cd fairride
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
fairride/
├── app/
│   ├── algorithms/     # Fairness-optimized matching algorithms
│   ├── routes/         # API endpoint routers
│   ├── models/         # Database schema definitions
│   ├── schemas/        # Pydantic data models
│   ├── crud.py         # Database operations
│   ├── database.py     # Supabase client initialization
│   ├── sendgrid_client.py  # Email service integration
│   └── utils/          # Utility functions
├── tests/              # Unit and integration tests
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Project Link: [https://github.com/yourusername/fairride](https://github.com/yourusername/fairride)