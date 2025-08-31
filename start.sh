#!/bin/bash

echo "🚗 Smart Garage Dashboard - Setup Script"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker non è installato. Installa Docker prima di continuare."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose non è installato. Installa Docker Compose prima di continuare."
    exit 1
fi

echo "✅ Docker e Docker Compose sono installati"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creazione file .env..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://admin:password123@postgres:5432/smartgarage
REDIS_URL=redis://redis:6379

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Email Configuration (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key

# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Camera Configuration
CAMERA_URL=rtsp://admin:password@192.168.1.100:554/stream1

# AI Service Configuration
BACKEND_URL=http://localhost:8000
EOF
    echo "✅ File .env creato. Modifica le configurazioni se necessario."
else
    echo "✅ File .env già esistente"
fi

# Create uploads directory
echo "📁 Creazione directory uploads..."
mkdir -p uploads

# Build and start services
echo "🔨 Avvio dei servizi Docker..."
docker-compose up -d --build

echo ""
echo "⏳ Attendo che i servizi siano pronti..."
sleep 30

# Check if services are running
echo "🔍 Verifica stato servizi..."

if docker-compose ps | grep -q "Up"; then
    echo "✅ Tutti i servizi sono attivi!"
else
    echo "❌ Alcuni servizi non sono attivi. Controlla i log:"
    echo "   docker-compose logs"
    exit 1
fi

echo ""
echo "🎉 Setup completato!"
echo ""
echo "📱 Accesso alle applicazioni:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • Swagger UI: http://localhost:8000/docs"
echo ""
echo "🔧 Comandi utili:"
echo "   • Logs: docker-compose logs"
echo "   • Stop: docker-compose down"
echo "   • Restart: docker-compose restart"
echo "   • Database: docker-compose exec postgres psql -U admin -d smartgarage"
echo ""
echo "🚀 Il sistema Smart Garage Dashboard è pronto per l'uso!"
