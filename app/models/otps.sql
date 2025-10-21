-- OTP table schema for storing one-time passwords
CREATE TABLE IF NOT EXISTS otps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL,
  otp TEXT NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  used BOOLEAN DEFAULT FALSE
);

-- Index for faster lookups by email
CREATE INDEX IF NOT EXISTS idx_otps_email ON otps(email);

-- Index for cleaning up expired OTPs
CREATE INDEX IF NOT EXISTS idx_otps_expires_at ON otps(expires_at);