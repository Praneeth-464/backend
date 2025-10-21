-- Drivers table schema
CREATE TABLE IF NOT EXISTS drivers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  email TEXT,
  current_lat NUMERIC,
  current_lon NUMERIC,
  available BOOLEAN DEFAULT TRUE,
  rating NUMERIC(2,1) DEFAULT 5.0,
  license_number TEXT,
  license_expiry_date TIMESTAMPTZ,
  vehicle_make TEXT,
  vehicle_model TEXT,
  vehicle_year INTEGER,
  vehicle_registration TEXT,
  vehicle_insurance_expiry TIMESTAMPTZ,
  background_check_status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
  safety_training_completed BOOLEAN DEFAULT FALSE,
  total_incidents INTEGER DEFAULT 0,
  performance_score NUMERIC(5,2) DEFAULT 100.00
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_drivers_rating ON drivers(rating);
CREATE INDEX IF NOT EXISTS idx_drivers_available ON drivers(available);
CREATE INDEX IF NOT EXISTS idx_drivers_background_check ON drivers(background_check_status);
CREATE INDEX IF NOT EXISTS idx_drivers_user_id ON drivers(user_id);