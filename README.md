# 🚗 OfficinaSma - Smart Workshop Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docs.docker.com/compose/)

## 📋 Indice

- [Panoramica](#-panoramica)
- [Caratteristiche](#-caratteristiche)
- [Stack Tecnologico](#-stack-tecnologico)
- [Architettura](#-architettura)
- [Installazione](#-installazione)
- [Configurazione](#-configurazione)
- [Utilizzo](#-utilizzo)
- [API Documentation](#-api-documentation)
- [Sviluppo](#-sviluppo)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contributi](#-contributi)
- [Licenza](#-licenza)

## 🎯 Panoramica

**OfficinaSma** è un sistema di gestione intelligente per officine meccaniche che combina tecnologie moderne con funzionalità avanzate di AI per automatizzare e ottimizzare i processi di gestione dell'officina.

Il sistema offre:
- **Dashboard intelligente** con KPI in tempo reale
- **Gestione completa** di clienti, veicoli e appuntamenti
- **Riconoscimento automatico** delle targhe con AI
- **Check-in/check-out automatico** dei veicoli
- **Fatturazione automatica** con generazione PDF
- **Notifiche email/SMS** per appuntamenti e aggiornamenti
- **Analytics avanzati** per l'ottimizzazione del business

## ✨ Caratteristiche

### 🎛️ Core Features
- **Gestione Clienti**: Database completo con storico veicoli e servizi
- **Gestione Veicoli**: Registrazione, manutenzione e storico completo
- **Appuntamenti**: Calendario digitale con gestione conflitti
- **Servizi**: Catalogo servizi con prezzi e tempi stimati
- **Fatturazione**: Generazione automatica fatture PDF
- **Check-in/Check-out**: Sistema automatico con riconoscimento targhe

### 🤖 AI & Automation
- **Riconoscimento Targhe**: EasyOCR + OpenCV per rilevamento automatico
- **Streaming Video**: Elaborazione in tempo reale da telecamere
- **Matching Veicoli**: Correlazione automatica targhe-veicoli
- **Notifiche Intelligenti**: Email e SMS automatici

### 📊 Analytics & Reporting
- **Dashboard KPI**: Metriche in tempo reale
- **Report Fatturato**: Analisi periodiche e trend
- **Statistiche Servizi**: Performance e popolarità servizi
- **Monitoraggio Occupazione**: Utilizzo officina e tempi

### 🔐 User Management & Security
- **Autenticazione JWT**: Sistema sicuro di login
- **Ruoli e Permessi**: Admin, Manager, Meccanico, Receptionist
- **Audit Log**: Tracciamento completo delle azioni
- **Password Hashing**: Sicurezza avanzata

## 🛠️ Stack Tecnologico

### Backend
- **Python 3.11+** con FastAPI
- **SQLAlchemy** ORM
- **PostgreSQL 15** database
- **Redis** caching
- **EasyOCR + OpenCV** AI recognition
- **SendGrid** email service
- **Twilio** SMS service
- **ReportLab** PDF generation

### Frontend
- **React 18** con TypeScript
- **Material-UI** component library
- **Tailwind CSS** styling
- **React Router** navigation
- **Axios** HTTP client

### Infrastructure
- **Docker** containerization
- **Docker Compose** orchestration
- **Nginx** reverse proxy (opzionale)
- **Prometheus** monitoring

## 🏗️ Architettura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   React App     │◄──►│   FastAPI       │◄──►│   PostgreSQL    │
│   (Port 3000)   │    │   (Port 8000)   │    │   (Port 5433)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Port 6380)   │
                       └─────────────────┘
```

## 🚀 Installazione

### Prerequisiti
- Docker e Docker Compose
- Git
- 4GB RAM disponibile
- 10GB spazio disco

### Installazione Rapida

1. **Clona il repository**
```bash
git clone <repository-url>
cd officinaSma
```

2. **Avvia il sistema**
```bash
chmod +x start.sh
./start.sh
```

3. **Accedi al sistema**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Installazione Manuale

1. **Configura l'ambiente**
```bash
cp .env.example .env
# Modifica le variabili in .env
```

2. **Avvia i servizi**
```bash
docker-compose up -d --build
```

3. **Inizializza il database**
```bash
docker exec smart-garage-postgres psql -U admin -d smartgarage -f /docker-entrypoint-initdb.d/init.sql
```

## ⚙️ Configurazione

### Variabili d'Ambiente (.env)

```bash
# Database
DATABASE_URL=postgresql://admin:password123@postgres:5432/smartgarage
REDIS_URL=redis://redis:6379

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Email (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key

# SMS (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Camera
CAMERA_URL=rtsp://admin:password@192.168.1.100:554/stream1
```

### Configurazione Camera
1. Imposta l'URL della telecamera in `CAMERA_URL`
2. Assicurati che la telecamera sia accessibile dalla rete
3. Testa la connessione: `curl -I $CAMERA_URL`

### Servizi Esterni
- **SendGrid**: Registrati su sendgrid.com per email
- **Twilio**: Registrati su twilio.com per SMS

## 👥 Utenti di Default

Il sistema viene inizializzato con i seguenti utenti:

### 🔑 Credenziali di Accesso

| Ruolo | Email | Password | Descrizione |
|-------|-------|----------|-------------|
| **Admin** | `admin@smartgarage.com` | `password123` | Accesso completo a tutte le funzionalità |
| **Manager** | `manager@smartgarage.com` | `password123` | Gestione operativa dell'officina |
| **Meccanico** | `mechanic@smartgarage.com` | `password123` | Gestione servizi e veicoli |
| **Receptionist** | `reception@smartgarage.com` | `password123` | Gestione appuntamenti e clienti |

### 🔐 Ruoli e Permessi

- **Admin**: Accesso completo, gestione utenti, configurazioni
- **Manager**: Gestione completa operativa, report, analytics
- **Meccanico**: Gestione servizi, veicoli, check-in/out
- **Receptionist**: Gestione clienti, appuntamenti, fatturazione

## 📱 Utilizzo

### Accesso al Sistema
1. Apri http://localhost:3000
2. Inserisci le credenziali di uno degli utenti sopra
3. Accedi al dashboard principale

### Dashboard Principale
- **KPI Cards**: Metriche in tempo reale
- **Azioni Rapide**: Accesso veloce alle funzioni principali
- **Attività Recenti**: Timeline delle ultime operazioni

### Gestione Operativa
- **Clienti**: Registrazione e gestione anagrafica
- **Veicoli**: Registrazione e storico manutenzione
- **Appuntamenti**: Pianificazione e gestione calendario
- **Check-in**: Registrazione arrivo veicoli
- **Fatturazione**: Generazione e invio fatture

## 🔌 API Documentation

### Endpoints Principali

#### Autenticazione
```bash
POST /api/v1/auth/login
POST /api/v1/auth/register
```

#### Clienti
```bash
GET    /api/v1/customers
POST   /api/v1/customers
GET    /api/v1/customers/{id}
PUT    /api/v1/customers/{id}
DELETE /api/v1/customers/{id}
```

#### Veicoli
```bash
GET    /api/v1/vehicles
POST   /api/v1/vehicles
GET    /api/v1/vehicles/{id}
PUT    /api/v1/vehicles/{id}
DELETE /api/v1/vehicles/{id}
```

#### Appuntamenti
```bash
GET    /api/v1/appointments
POST   /api/v1/appointments
GET    /api/v1/appointments/{id}
PUT    /api/v1/appointments/{id}
DELETE /api/v1/appointments/{id}
```

#### AI Detection
```bash
GET    /api/v1/ai/detections
POST   /api/v1/ai/detect
PUT    /api/v1/ai/detections/{id}
```

### Swagger UI
Documentazione completa disponibile su: http://localhost:8000/docs

## 🛠️ Sviluppo

### Struttura del Progetto
```
officinaSma/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   ├── core/
│   │   ├── services/
│   │   └── schemas/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── contexts/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

### Comandi di Sviluppo

```bash
# Backend development
docker-compose up backend -d
docker-compose logs -f backend

# Frontend development
docker-compose up frontend -d
docker-compose logs -f frontend

# Database access
docker exec -it smart-garage-postgres psql -U admin -d smartgarage

# Redis access
docker exec -it smart-garage-redis redis-cli
```

### Testing
```bash
# Backend tests
docker exec smart-garage-backend pytest

# Frontend tests
docker exec smart-garage-frontend npm test
```

## 🚀 Deployment

### Produzione
1. Modifica le variabili d'ambiente per la produzione
2. Configura SSL/TLS
3. Imposta backup automatici del database
4. Configura monitoring e alerting

### Docker Compose Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes
```bash
kubectl apply -f k8s/
```

## 🔧 Troubleshooting

### Problemi Comuni

#### Backend non si avvia
```bash
# Controlla i log
docker-compose logs backend

# Verifica la connessione database
docker exec smart-garage-backend python -c "from app.core.database import engine; print(engine.execute('SELECT 1').scalar())"
```

#### Frontend non si carica
```bash
# Controlla i log
docker-compose logs frontend

# Verifica la connessione API
curl http://localhost:8000/health
```

#### Problemi di Login
```bash
# Verifica utenti nel database
docker exec smart-garage-postgres psql -U admin -d smartgarage -c "SELECT email, role FROM users;"

# Reset password admin
docker exec smart-garage-postgres psql -U admin -d smartgarage -c "UPDATE users SET hashed_password = '\$2b\$12\$tY/OnqzrLki2EYN09f4kb.NAxi.R3k.UOAAh9/rbrLbzDPk2HokLC' WHERE email = 'admin@smartgarage.com';"
```

#### Problemi di Connessione Database
```bash
# Verifica stato container
docker-compose ps

# Riavvia database
docker-compose restart postgres

# Verifica connessione
docker exec smart-garage-postgres pg_isready -U admin -d smartgarage
```

### Log Files
```bash
# Tutti i servizi
docker-compose logs

# Servizio specifico
docker-compose logs [service_name]

# Log in tempo reale
docker-compose logs -f [service_name]
```

## 🗺️ Roadmap

### v1.1 - Miglioramenti UI/UX
- [ ] Dashboard personalizzabile
- [ ] Tema scuro/chiaro
- [ ] Notifiche push in tempo reale
- [ ] Mobile app responsive

### v1.2 - Funzionalità Avanzate
- [ ] Integrazione POS
- [ ] Gestione magazzino
- [ ] Report avanzati
- [ ] Integrazione contabilità

### v1.3 - AI Enhancement
- [ ] Diagnostica veicoli AI
- [ ] Previsione manutenzione
- [ ] Chatbot assistente
- [ ] Analisi sentiment clienti

### v2.0 - Multi-tenancy
- [ ] Supporto multi-officina
- [ ] Franchising management
- [ ] API marketplace
- [ ] Integrazione terze parti

## 🤝 Contributi

1. Fork il progetto
2. Crea un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

### Guidelines
- Segui le convenzioni di codice
- Aggiungi test per nuove funzionalità
- Aggiorna la documentazione
- Verifica che tutto funzioni con Docker

## 📄 Licenza

Questo progetto è rilasciato sotto la licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## 🆘 Supporto

- **Documentazione**: [Wiki del progetto](link-to-wiki)
- **Issues**: [GitHub Issues](link-to-issues)
- **Email**: support@officinasma.com
- **Telegram**: [@OfficinaSmaSupport](link-to-telegram)

## 🙏 Ringraziamenti

- **FastAPI** per l'eccezionale framework backend
- **React** per la libreria frontend
- **Material-UI** per i componenti UI
- **EasyOCR** per il riconoscimento targhe
- **Docker** per la containerizzazione

---

**OfficinaSma** - Trasformando la gestione delle officine con l'intelligenza artificiale 🚗⚙️✨
