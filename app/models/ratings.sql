-- Ratings table schema
CREATE TABLE IF NOT EXISTS ratings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  ride_id UUID REFERENCES rides(id),
  rider_id UUID REFERENCES riders(id),
  driver_id UUID REFERENCES drivers(id),
  rating INTEGER CHECK (rating >= 1 AND rating <= 5),
  review TEXT,
  tip NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW()
);