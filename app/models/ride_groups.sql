-- Ride groups table schema for shared rides
CREATE TABLE IF NOT EXISTS ride_groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  creator_id UUID REFERENCES users(id),
  status TEXT DEFAULT 'pending', -- 'pending', 'confirmed', 'in_progress', 'completed', 'cancelled'
  estimated_fare NUMERIC,
  final_fare NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ride group members table schema
CREATE TABLE IF NOT EXISTS ride_group_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ride_group_id UUID REFERENCES ride_groups(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  role TEXT DEFAULT 'member', -- 'creator', 'member'
  status TEXT DEFAULT 'invited', -- 'invited', 'accepted', 'declined', 'left'
  fare_share_percentage NUMERIC DEFAULT 0, -- Percentage of fare this member will pay
  invited_at TIMESTAMPTZ DEFAULT NOW(),
  accepted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_ride_groups_creator_id ON ride_groups(creator_id);
CREATE INDEX IF NOT EXISTS idx_ride_group_members_ride_group_id ON ride_group_members(ride_group_id);
CREATE INDEX IF NOT EXISTS idx_ride_group_members_user_id ON ride_group_members(user_id);