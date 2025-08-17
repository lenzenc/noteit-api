# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a minimal infrastructure setup for a note-taking API, focusing on image storage and processing services. The project contains only a Docker Compose configuration that sets up:

- **MinIO**: S3-compatible object storage for images
- **ImgProxy**: Image processing and optimization service
- **MinIO Setup**: Automated bucket creation and policy configuration

## Development Commands

All development tasks are managed through a comprehensive Makefile. Run `make help` to see all available commands.

### Quick Start
```bash
# Complete setup for new developers
make quickstart

# Run development server
make dev

# Start infrastructure and development server together
make up
```

### Common Commands
```bash
# Setup and Installation
make install          # Install dependencies with Poetry
make setup            # Complete project setup (install deps + create .env)

# Development
make dev              # Run development server with auto-reload
make dev-debug        # Run with debug logging

# Testing
make test             # Run tests
make test-cov         # Run tests with coverage report
make test-watch       # Run tests in watch mode

# Code Quality
make format           # Format code with black and isort
make lint             # Run linting (flake8)
make type-check       # Run type checking with mypy
make quality          # Run all code quality checks

# Infrastructure Management
make infra-up         # Start infrastructure services (MinIO, ImgProxy)
make infra-down       # Stop infrastructure services
make infra-logs       # View infrastructure logs
make infra-clean      # Stop services and remove volumes

# Cleanup
make clean            # Clean up temporary files and caches
make clean-all        # Clean everything including Docker volumes
```

## Architecture

### Infrastructure
The system uses a microservices approach with three Docker containers:

1. **MinIO** (Port 9000/9001): Object storage with web console
   - API endpoint: http://localhost:9000
   - Console: http://localhost:9001
   - Default credentials: minioadmin/minioadmin123

2. **ImgProxy** (Port 8080): Image processing service
   - Processes images stored in MinIO S3 bucket
   - Supports WebP conversion and quality optimization
   - Uses signed URLs for security

3. **MinIO Setup**: One-time initialization container
   - Creates 'images' bucket
   - Sets public read policy
   - Runs on startup only

### FastAPI Application
The API follows a layered architecture with clear separation of concerns:

```
src/noteit_api/
├── main.py              # FastAPI app entry point
├── core/
│   ├── config.py        # Settings and configuration
├── api/
│   └── v1/
│       ├── router.py    # API v1 router
│       └── endpoints/   # Route handlers
├── schemas/             # Pydantic models for request/response
├── models/              # Database models (future)
└── services/            # Business logic layer
```

- **API Layer**: Route handlers in `api/v1/endpoints/`
- **Schema Layer**: Pydantic models for validation in `schemas/`
- **Service Layer**: Business logic in `services/`
- **Configuration**: Environment-based settings using python-dotenv

## Configuration

### Environment Variables
All configuration is managed through environment variables loaded from a `.env` file:

1. Copy `.env.example` to `.env`: `cp .env.example .env`
2. Modify values as needed for your environment
3. Configuration is automatically loaded via python-dotenv

### Key Settings
- **API Configuration**: Project name, version, API prefix, CORS origins
- **Server Configuration**: Host and port settings
- **MinIO Configuration**: S3-compatible storage credentials and settings
- **ImgProxy Configuration**: Image processing service URL and security keys

### Infrastructure
- MinIO stores data in persistent `minio_data` volume
- ImgProxy is configured with security keys and S3 integration
- All services communicate via `app-network` bridge
- Image bucket is publicly accessible for serving processed images

## Service Dependencies

Services start in order: MinIO → MinIO Setup → ImgProxy, ensuring proper initialization and bucket availability.