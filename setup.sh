#!/bin/bash

# Circular Economy Marketplace - Setup Script
# This script sets up and starts the complete platform

set -e

echo "🌍 Circular Economy Marketplace - Setup Script"
echo "=============================================="
echo ""

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✓ Docker found"

# Check for Docker Compose
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker Compose found"
echo ""

# Create environment files if they don't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env from example..."
    cp backend/.env.example backend/.env
    echo "✓ Backend .env created"
else
    echo "✓ Backend .env already exists"
fi

if [ ! -f frontend/.env ]; then
    echo "📝 Creating frontend/.env from example..."
    cp frontend/.env.example frontend/.env
    echo "✓ Frontend .env created"
else
    echo "✓ Frontend .env already exists"
fi

echo ""
echo "🚀 Starting services with Docker Compose..."
echo ""

# Build and start all services
docker compose up -d --build

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker compose ps

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo "   ReDoc:     http://localhost:8000/redoc"
echo ""
echo "📚 View logs:"
echo "   All:       docker compose logs -f"
echo "   Backend:   docker compose logs -f backend"
echo "   Frontend:  docker compose logs -f frontend"
echo ""
echo "🛑 Stop services:"
echo "   docker compose down"
echo ""
echo "💡 Default admin credentials:"
echo "   You'll need to register a user first with role 'admin'"
echo ""
