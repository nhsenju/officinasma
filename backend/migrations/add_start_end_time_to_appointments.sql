-- Migrazione per aggiungere campi ora inizio e ora fine agli appuntamenti
-- Data: 2024-08-27

-- Aggiungi le colonne start_time e end_time
ALTER TABLE appointments 
ADD COLUMN start_time TIME,
ADD COLUMN end_time TIME;

-- Aggiorna i record esistenti con valori di default
-- Per ora, usa l'ora di inizio dall'appointment_date e calcola l'ora di fine
UPDATE appointments 
SET 
    start_time = EXTRACT(HOUR FROM appointment_date)::TEXT || ':' || 
                 LPAD(EXTRACT(MINUTE FROM appointment_date)::TEXT, 2, '0') || ':00',
    end_time = (EXTRACT(HOUR FROM appointment_date) + (estimated_duration / 60))::TEXT || ':' || 
               LPAD(MOD(EXTRACT(MINUTE FROM appointment_date) + MOD(estimated_duration, 60), 60)::TEXT, 2, '0') || ':00';

-- Rendi le colonne NOT NULL dopo aver popolato i dati
ALTER TABLE appointments 
ALTER COLUMN start_time SET NOT NULL,
ALTER COLUMN end_time SET NOT NULL;

-- Aggiungi indici per migliorare le performance delle query
CREATE INDEX idx_appointments_start_time ON appointments(start_time);
CREATE INDEX idx_appointments_end_time ON appointments(end_time);
CREATE INDEX idx_appointments_start_end_time ON appointments(start_time, end_time);
