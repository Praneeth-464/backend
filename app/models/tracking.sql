-- Tracking table schema for real-time driver location updates
CREATE TABLE IF NOT EXISTS tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  driver_id UUID REFERENCES drivers(id),
  lat NUMERIC NOT NULL,
  lon NUMERIC NOT NULL,
  speed NUMERIC DEFAULT 0,
  heading NUMERIC DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);