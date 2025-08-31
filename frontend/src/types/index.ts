export interface Customer {
  id: number;
  full_name: string;
  email: string;
  phone: string;
  address?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Vehicle {
  id: number;
  license_plate: string;
  brand: string;
  model: string;
  year: number;
  color: string;
  vin?: string;
  engine_size?: string;
  fuel_type?: string;
  customer_id: number;
  created_at: string;
  updated_at: string;
}

export interface Service {
  id: number;
  name: string;
  description?: string;
  price: number;
  duration_minutes: number;
  category: string;
  created_at: string;
  updated_at: string;
}

export interface Appointment {
  id: number;
  customer_id: number;
  vehicle_id: number;
  service_id: number;
  appointment_date: string;
  start_time: string;
  end_time: string;
  estimated_duration: number;
  notes?: string;
  status: 'scheduled' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled';
  created_at: string;
  updated_at: string;
  customer?: Customer;
  vehicle?: Vehicle;
  service?: Service;
}

export interface AppointmentCreate {
  customer_id: number;
  vehicle_id: number;
  service_id: number;
  appointment_date: string;
  start_time: string;
  end_time: string;
  estimated_duration: number;
  notes?: string;
}

export interface CustomerCreate {
  full_name: string;
  email: string;
  phone: string;
  address?: string;
  notes?: string;
}

export interface VehicleCreate {
  license_plate: string;
  brand: string;
  model: string;
  year: number;
  color: string;
  vin?: string;
  engine_size?: string;
  fuel_type?: string;
  customer_id: number;
}
