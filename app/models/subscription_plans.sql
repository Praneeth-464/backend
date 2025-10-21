







-- Subscription plans table schema
CREATE TABLE IF NOT EXISTS subscription_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  price NUMERIC NOT NULL, -- Monthly price
  billing_cycle TEXT NOT NULL, -- 'monthly', 'annual'
  ride_limit INTEGER, -- Number of rides per billing cycle (NULL for unlimited)
  priority_booking BOOLEAN DEFAULT FALSE, -- Priority booking access
  discount_percentage NUMERIC(5,2) DEFAULT 0.00, -- Discount on regular rides
  cancellation_fee_waiver BOOLEAN DEFAULT FALSE, -- Waive cancellation fees
  customer_support_priority TEXT DEFAULT 'standard', -- 'standard', 'priority', 'dedicated'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User subscriptions table schema
CREATE TABLE IF NOT EXISTS user_subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  plan_id UUID REFERENCES subscription_plans(id),
  status TEXT DEFAULT 'active', -- 'active', 'cancelled', 'expired', 'suspended'
  start_date TIMESTAMPTZ NOT NULL,
  end_date TIMESTAMPTZ, -- NULL for ongoing subscriptions
  auto_renew BOOLEAN DEFAULT TRUE,
  payment_method_id TEXT, -- Reference to payment method
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Recurring rides table schema
CREATE TABLE IF NOT EXISTS recurring_rides (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  origin_lat NUMERIC NOT NULL,
  origin_lon NUMERIC NOT NULL,
  destination_lat NUMERIC NOT NULL,
  destination_lon NUMERIC NOT NULL,
  frequency TEXT NOT NULL, -- 'daily', 'weekly', 'monthly'
  days_of_week INTEGER[], -- Array of days (0=Sunday, 1=Monday, etc.) for weekly
  day_of_month INTEGER, -- Day of month for monthly (1-31)
  start_time TIME NOT NULL, -- Time of day for the ride
  end_date TIMESTAMPTZ, -- When to stop creating rides (NULL for indefinite)
  status TEXT DEFAULT 'active', -- 'active', 'paused', 'cancelled'
  preferences JSONB, -- Ride preferences
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Generated scheduled rides from recurring rides
CREATE TABLE IF NOT EXISTS generated_scheduled_rides (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  recurring_ride_id UUID REFERENCES recurring_rides(id) ON DELETE CASCADE,
  scheduled_ride_id UUID REFERENCES scheduled_rides(id) ON DELETE CASCADE,
  generation_date TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_subscription_plans_name ON subscription_plans(name);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_status ON user_subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_recurring_rides_user_id ON recurring_rides(user_id);
CREATE INDEX IF NOT EXISTS idx_recurring_rides_frequency ON recurring_rides(frequency);
CREATE INDEX IF NOT EXISTS idx_recurring_rides_status ON recurring_rides(status);
CREATE INDEX IF NOT EXISTS idx_generated_scheduled_rides_recurring_ride_id ON generated_scheduled_rides(recurring_ride_id);