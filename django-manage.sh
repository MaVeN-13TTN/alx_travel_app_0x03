#!/bin/bash

# ALX Travel App - Django Management Script
# This script helps run Django commands from the root directory

set -e

PROJECT_ROOT="/home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03"
DJANGO_DIR="$PROJECT_ROOT/alx_travel_app"
VENV_PATH="$PROJECT_ROOT/venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
check_venv() {
    if [ ! -d "$VENV_PATH" ]; then
        log_error "Virtual environment not found at $VENV_PATH"
        exit 1
    fi
}

# Function to activate venv and run Django command
run_django_command() {
    check_venv
    cd "$DJANGO_DIR"
    log_info "Running: python manage.py $*"
    source "$VENV_PATH/bin/activate" && python manage.py "$@"
}

# Function to start development server
start_server() {
    local port=${1:-8000}
    log_info "Starting Django development server on port $port..."
    run_django_command runserver "$port"
}

# Function to run migrations
migrate() {
    log_info "Running database migrations..."
    run_django_command migrate
    log_success "Migrations completed!"
}

# Function to create superuser
create_superuser() {
    log_info "Creating Django superuser..."
    run_django_command createsuperuser
}

# Function to run tests
run_tests() {
    if [ $# -eq 0 ]; then
        log_info "Running all tests..."
        run_django_command test
    else
        log_info "Running tests for: $*"
        run_django_command test "$@"
    fi
}

# Function to collect static files
collect_static() {
    log_info "Collecting static files..."
    run_django_command collectstatic --noinput
    log_success "Static files collected!"
}

# Function to check Django configuration
check_config() {
    log_info "Checking Django configuration..."
    run_django_command check
    log_success "Configuration check passed!"
}

# Function to show help
show_help() {
    echo "ALX Travel App - Django Management Script"
    echo
    echo "Usage: $0 [COMMAND] [ARGS]"
    echo
    echo "Commands:"
    echo "  server [PORT]         Start development server (default port: 8000)"
    echo "  migrate              Run database migrations"
    echo "  superuser            Create superuser"
    echo "  test [APP...]        Run tests (all tests if no app specified)"
    echo "  collectstatic        Collect static files"
    echo "  check                Check Django configuration"
    echo "  shell                Open Django shell"
    echo "  seed                 Run seed command (if available)"
    echo "  manage [COMMAND]     Run any Django management command"
    echo "  help                 Show this help message"
    echo
    echo "Examples:"
    echo "  $0 server 8001"
    echo "  $0 migrate"
    echo "  $0 test listings"
    echo "  $0 manage showmigrations"
}

# Main script logic
main() {
    case "${1:-help}" in
        server)
            start_server "${2:-8000}"
            ;;
        migrate)
            migrate
            ;;
        superuser)
            create_superuser
            ;;
        test)
            shift
            run_tests "$@"
            ;;
        collectstatic)
            collect_static
            ;;
        check)
            check_config
            ;;
        shell)
            run_django_command shell
            ;;
        seed)
            run_django_command seed "${@:2}"
            ;;
        manage)
            shift
            run_django_command "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
