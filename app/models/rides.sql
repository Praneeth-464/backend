-- Rides table schema
CREATE TABLE IF NOT EXISTS rides (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  rider_id UUID REFERENCES riders(id),
  driver_id UUID REFERENCES drivers(id),
  algorithm TEXT,
  start_time TIMESTAMPTZ,
  end_time TIMESTAMPTZ,
  fare NUMERIC,
  utility NUMERIC,
  status TEXT DEFAULT 'assigned',
  ride_group_id UUID REFERENCES ride_groups(id) -- For shared rides
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_rides_user_id ON rides(user_id);
CREATE INDEX IF NOT EXISTS idx_rides_rider_id ON rides(rider_id);
CREATE INDEX IF NOT EXISTS idx_rides_driver_id ON rides(driver_id);
CREATE INDEX IF NOT EXISTS idx_rides_ride_group_id ON rides(ride_group_id);