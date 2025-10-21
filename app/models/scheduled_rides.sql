-- Scheduled rides table schema
CREATE TABLE IF NOT EXISTS scheduled_rides (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  rider_id UUID REFERENCES riders(id),
  origin_lat NUMERIC NOT NULL,
  origin_lon NUMERIC NOT NULL,
  destination_lat NUMERIC NOT NULL,
  destination_lon NUMERIC NOT NULL,
  scheduled_time TIMESTAMPTZ NOT NULL,
  status TEXT DEFAULT 'scheduled', -- 'scheduled', 'confirmed', 'completed', 'cancelled'
  preferences JSONB,
  subscription_id UUID REFERENCES user_subscriptions(id), -- For subscription-based rides
  recurring_ride_id UUID REFERENCES recurring_rides(id), -- For recurring rides
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_scheduled_rides_rider_id ON scheduled_rides(rider_id);
CREATE INDEX IF NOT EXISTS idx_scheduled_rides_scheduled_time ON scheduled_rides(scheduled_time);
CREATE INDEX IF NOT EXISTS idx_scheduled_rides_status ON scheduled_rides(status);
CREATE INDEX IF NOT EXISTS idx_scheduled_rides_subscription_id ON scheduled_rides(subscription_id);
CREATE INDEX IF NOT EXISTS idx_scheduled_rides_recurring_ride_id ON scheduled_rides(recurring_ride_id);