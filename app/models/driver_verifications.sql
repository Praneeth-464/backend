-- Driver verifications table schema
CREATE TABLE IF NOT EXISTS driver_verifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  driver_id UUID REFERENCES drivers(id) ON DELETE CASCADE,
  verification_type TEXT NOT NULL, -- 'background_check', 'vehicle_inspection', 'safety_training'
  status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
  document_url TEXT, -- URL to stored verification document
  notes TEXT,
  verified_by UUID REFERENCES users(id), -- Admin user who verified
  verified_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Driver safety training modules table schema
CREATE TABLE IF NOT EXISTS driver_training_modules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  duration_minutes INTEGER,
  content_url TEXT, -- URL to training content
  is_mandatory BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Driver training completions table schema
CREATE TABLE IF NOT EXISTS driver_training_completions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  driver_id UUID REFERENCES drivers(id) ON DELETE CASCADE,
  training_module_id UUID REFERENCES driver_training_modules(id) ON DELETE CASCADE,
  completed_at TIMESTAMPTZ,
  score NUMERIC(5,2), -- Percentage score
  certificate_url TEXT, -- URL to completion certificate
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Driver incident reports table schema
CREATE TABLE IF NOT EXISTS driver_incidents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  driver_id UUID REFERENCES drivers(id) ON DELETE CASCADE,
  reporter_id UUID REFERENCES users(id), -- Who reported the incident
  incident_type TEXT, -- 'accident', 'complaint', 'violation'
  description TEXT,
  severity TEXT, -- 'low', 'medium', 'high', 'critical'
  status TEXT DEFAULT 'reported', -- 'reported', 'investigating', 'resolved', 'dismissed'
  resolution_notes TEXT,
  resolved_by UUID REFERENCES users(id), -- Admin who resolved
  resolved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Driver performance metrics table schema
CREATE TABLE IF NOT EXISTS driver_performance_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  driver_id UUID REFERENCES drivers(id) ON DELETE CASCADE,
  metric_type TEXT, -- 'punctuality', 'safety', 'customer_service', 'vehicle_maintenance'
  score NUMERIC(5,2), -- Percentage score
  period_start TIMESTAMPTZ,
  period_end TIMESTAMPTZ,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_driver_verifications_driver_id ON driver_verifications(driver_id);
CREATE INDEX IF NOT EXISTS idx_driver_verifications_type ON driver_verifications(verification_type);
CREATE INDEX IF NOT EXISTS idx_driver_verifications_status ON driver_verifications(status);

CREATE INDEX IF NOT EXISTS idx_driver_training_completions_driver_id ON driver_training_completions(driver_id);
CREATE INDEX IF NOT EXISTS idx_driver_training_completions_module_id ON driver_training_completions(training_module_id);

CREATE INDEX IF NOT EXISTS idx_driver_incidents_driver_id ON driver_incidents(driver_id);
CREATE INDEX IF NOT EXISTS idx_driver_incidents_status ON driver_incidents(status);
CREATE INDEX IF NOT EXISTS idx_driver_incidents_type ON driver_incidents(incident_type);

CREATE INDEX IF NOT EXISTS idx_driver_performance_metrics_driver_id ON driver_performance_metrics(driver_id);
CREATE INDEX IF NOT EXISTS idx_driver_performance_metrics_type ON driver_performance_metrics(metric_type);