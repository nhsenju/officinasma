-- Smart Garage Dashboard Database Initialization
-- This script creates the initial database structure and sample data

-- Create database if not exists
-- CREATE DATABASE smartgarage;

-- Connect to the database
-- \c smartgarage;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE user_role AS ENUM ('admin', 'manager', 'mechanic', 'receptionist');
CREATE TYPE appointment_status AS ENUM ('scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled');
CREATE TYPE invoice_status AS ENUM ('draft', 'sent', 'paid', 'overdue', 'cancelled');

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role DEFAULT 'receptionist',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    color VARCHAR(50) NOT NULL,
    vin VARCHAR(17) UNIQUE,
    engine_size VARCHAR(20),
    fuel_type VARCHAR(20),
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    duration_minutes INTEGER NOT NULL,
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    service_id INTEGER NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    appointment_date TIMESTAMP WITH TIME ZONE NOT NULL,
    estimated_duration INTEGER NOT NULL,
    notes TEXT,
    status appointment_status DEFAULT 'scheduled',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS checkins (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    checkin_time TIMESTAMP WITH TIME ZONE NOT NULL,
    checkout_time TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    is_automatic BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
    total_amount DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(10,2) NOT NULL,
    status invoice_status DEFAULT 'draft',
    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_detections (
    id SERIAL PRIMARY KEY,
    license_plate VARCHAR(20) NOT NULL,
    confidence DECIMAL(5,4) NOT NULL,
    image_path VARCHAR(500),
    processed BOOLEAN DEFAULT FALSE,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE SET NULL,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity VARCHAR(100) NOT NULL,
    entity_id INTEGER,
    details JSONB,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_vehicles_license_plate ON vehicles(license_plate);
CREATE INDEX IF NOT EXISTS idx_vehicles_customer_id ON vehicles(customer_id);
CREATE INDEX IF NOT EXISTS idx_appointments_customer_id ON appointments(customer_id);
CREATE INDEX IF NOT EXISTS idx_appointments_vehicle_id ON appointments(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);
CREATE INDEX IF NOT EXISTS idx_checkins_vehicle_id ON checkins(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_checkins_checkin_time ON checkins(checkin_time);
CREATE INDEX IF NOT EXISTS idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_ai_detections_license_plate ON ai_detections(license_plate);
CREATE INDEX IF NOT EXISTS idx_ai_detections_processed ON ai_detections(processed);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);

-- Insert sample data

-- Sample users
INSERT INTO users (email, full_name, hashed_password, role) VALUES
('admin@smartgarage.com', 'Amministratore Sistema', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'admin'),
('manager@smartgarage.com', 'Manager Officina', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'manager'),
('mechanic@smartgarage.com', 'Meccanico', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'mechanic'),
('reception@smartgarage.com', 'Receptionist', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'receptionist')
ON CONFLICT (email) DO NOTHING;

-- Sample customers
INSERT INTO customers (full_name, email, phone, address) VALUES
('Mario Rossi', 'mario.rossi@email.com', '+39 333 1234567', 'Via Roma 123, Milano'),
('Giulia Bianchi', 'giulia.bianchi@email.com', '+39 333 2345678', 'Via Garibaldi 45, Roma'),
('Luca Verdi', 'luca.verdi@email.com', '+39 333 3456789', 'Via Napoli 67, Napoli'),
('Anna Neri', 'anna.neri@email.com', '+39 333 4567890', 'Via Firenze 89, Firenze')
ON CONFLICT DO NOTHING;

-- Sample vehicles
INSERT INTO vehicles (license_plate, brand, model, year, color, vin, engine_size, fuel_type, customer_id) VALUES
('AB123CD', 'Fiat', 'Panda', 2020, 'Bianco', 'ZFA22300005556777', '1.2', 'Benzina', 1),
('EF456GH', 'Renault', 'Clio', 2019, 'Grigio', 'VF1RFA00001234567', '1.0', 'Benzina', 2),
('IJ789KL', 'Volkswagen', 'Golf', 2021, 'Nero', 'WVWZZZ1KZAW123456', '1.5', 'Diesel', 3),
('MN012PQ', 'Toyota', 'Yaris', 2018, 'Rosso', 'JTDKN3DU0E1234567', '1.0', 'Ibrido', 4)
ON CONFLICT (license_plate) DO NOTHING;

-- Sample services
INSERT INTO services (name, description, price, duration_minutes, category) VALUES
('Cambio Olio', 'Cambio olio motore e filtro olio', 45.00, 60, 'Manutenzione'),
('Revisione', 'Revisione completa del veicolo', 120.00, 120, 'Manutenzione'),
('Sostituzione Freni', 'Sostituzione pastiglie e dischi freni', 180.00, 90, 'Freni'),
('Diagnosi Elettronica', 'Controllo centralina e diagnostica', 80.00, 45, 'Diagnostica'),
('Sostituzione Batteria', 'Sostituzione batteria auto', 95.00, 30, 'Elettrico'),
('Pulizia Filtro Aria', 'Pulizia e sostituzione filtro aria', 25.00, 30, 'Manutenzione')
ON CONFLICT DO NOTHING;

-- Sample appointments
INSERT INTO appointments (customer_id, vehicle_id, service_id, appointment_date, estimated_duration, status) VALUES
(1, 1, 1, CURRENT_TIMESTAMP + INTERVAL '1 day', 60, 'scheduled'),
(2, 2, 2, CURRENT_TIMESTAMP + INTERVAL '2 days', 120, 'scheduled'),
(3, 3, 3, CURRENT_TIMESTAMP + INTERVAL '3 hours', 90, 'confirmed'),
(4, 4, 4, CURRENT_TIMESTAMP - INTERVAL '2 hours', 45, 'completed')
ON CONFLICT DO NOTHING;

-- Sample check-ins
INSERT INTO checkins (vehicle_id, checkin_time, is_automatic) VALUES
(3, CURRENT_TIMESTAMP - INTERVAL '1 hour', TRUE),
(4, CURRENT_TIMESTAMP - INTERVAL '3 hours', FALSE)
ON CONFLICT DO NOTHING;

-- Sample AI detections
INSERT INTO ai_detections (license_plate, confidence, processed, vehicle_id) VALUES
('IJ789KL', 0.95, TRUE, 3),
('MN012PQ', 0.87, TRUE, 4),
('XY999ZZ', 0.92, FALSE, NULL)
ON CONFLICT DO NOTHING;

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_vehicles_updated_at BEFORE UPDATE ON vehicles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_services_updated_at BEFORE UPDATE ON services FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_checkins_updated_at BEFORE UPDATE ON checkins FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ai_detections_updated_at BEFORE UPDATE ON ai_detections FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO admin;

-- Set default password for all users (change in production!)
-- Default password is 'password123'
