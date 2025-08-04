#!/bin/bash

# ALX Travel App - Docker Management Script

set -e

PROJECT_NAME="alx_travel_app_0x03"
MYSQL_CONTAINER="alx_travel_mysql"

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

# Check if docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
}

# Function to start MySQL container
start_mysql() {
    log_info "Starting MySQL container..."
    docker compose up -d mysql
    
    # Wait for MySQL to be ready
    log_info "Waiting for MySQL to be ready..."
    sleep 10
    
    # Test connection
    if mysql -h 127.0.0.1 -P 3308 -u travel_user -ptravel_password -e "SELECT 'Ready!' as status;" &> /dev/null; then
        log_success "MySQL container is ready!"
    else
        log_warning "MySQL container started but may not be fully ready yet. Please wait a moment and try again."
    fi
}

# Function to stop MySQL container
stop_mysql() {
    log_info "Stopping MySQL container..."
    docker compose down
    log_success "MySQL container stopped"
}

# Function to reset database
reset_database() {
    log_warning "This will PERMANENTLY DELETE all data in the database!"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Resetting database..."
        docker compose down -v
        docker compose up -d mysql
        log_info "Waiting for MySQL to initialize..."
        sleep 15
        log_success "Database reset complete. Don't forget to run migrations!"
        log_info "Run: python manage.py migrate"
    else
        log_info "Database reset cancelled"
    fi
}

# Function to show container status
show_status() {
    log_info "Container status:"
    docker compose ps
    echo
    log_info "Container logs (last 10 lines):"
    docker logs --tail 10 $MYSQL_CONTAINER 2>/dev/null || log_warning "Container not running or logs unavailable"
}

# Function to access MySQL shell
mysql_shell() {
    log_info "Connecting to MySQL shell..."
    mysql -h 127.0.0.1 -P 3308 -u travel_user -ptravel_password alx_travel_db
}

# Function to backup database
backup_database() {
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    log_info "Creating database backup: $backup_file"
    mysqldump -h 127.0.0.1 -P 3308 -u travel_user -ptravel_password alx_travel_db > "$backup_file"
    log_success "Database backup created: $backup_file"
}

# Function to show help
show_help() {
    echo "ALX Travel App - Docker Management Script"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  start       Start MySQL container"
    echo "  stop        Stop MySQL container"
    echo "  restart     Restart MySQL container"
    echo "  status      Show container status and logs"
    echo "  shell       Access MySQL shell"
    echo "  backup      Create database backup"
    echo "  reset       Reset database (DESTROYS ALL DATA)"
    echo "  help        Show this help message"
    echo
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 status"
    echo "  $0 shell"
}

# Main script logic
main() {
    check_docker
    
    case "${1:-help}" in
        start)
            start_mysql
            ;;
        stop)
            stop_mysql
            ;;
        restart)
            stop_mysql
            sleep 2
            start_mysql
            ;;
        status)
            show_status
            ;;
        shell)
            mysql_shell
            ;;
        backup)
            backup_database
            ;;
        reset)
            reset_database
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
