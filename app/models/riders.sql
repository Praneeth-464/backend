-- Riders table schema
CREATE TABLE IF NOT EXISTS riders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  email TEXT NOT NULL,
  origin_lat NUMERIC,
  origin_lon NUMERIC,
  destination_lat NUMERIC,
  destination_lon NUMERIC,
  preferred_departure TIMESTAMPTZ,
  preferred_arrival TIMESTAMPTZ,
  beta NUMERIC(4,3) DEFAULT 0.5, -- patience factor
  status TEXT DEFAULT 'waiting',
  created_at TIMESTAMPTZ DEFAULT NOW()
);