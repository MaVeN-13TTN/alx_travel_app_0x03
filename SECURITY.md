# Security Configuration Guide

## Environment Variables

This project uses `django-environ` to manage configuration through environment variables, following 12-factor app methodology for security.

### ⚠️ IMPORTANT SECURITY NOTES

1. **NEVER commit `.env` files to version control**
2. **NEVER put sensitive data as default values in code**
3. **ALWAYS use environment variables for sensitive configuration**

### Setup Instructions

1. **Copy the example environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Generate a new SECRET_KEY:**

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Fill in your actual values in `.env`:**
   - Replace `your-secret-key-here-generate-a-new-one` with the generated key
   - Update database credentials with your actual MySQL details
   - Set appropriate CORS origins for your frontend

### Required Environment Variables

| Variable               | Description                  | Example                              |
| ---------------------- | ---------------------------- | ------------------------------------ |
| `SECRET_KEY`           | Django secret key (required) | `django-insecure-abc123...`          |
| `DEBUG`                | Debug mode (default: False)  | `True` or `False`                    |
| `ALLOWED_HOSTS`        | Allowed hosts (required)     | `localhost,127.0.0.1,yourdomain.com` |
| `DB_NAME`              | Database name (required)     | `alxtravelapp`                       |
| `DB_USER`              | Database user (required)     | `your_db_user`                       |
| `DB_PASSWORD`          | Database password (required) | `your_secure_password`               |
| `DB_HOST`              | Database host (required)     | `localhost`                          |
| `DB_PORT`              | Database port (required)     | `3306`                               |
| `CORS_ALLOWED_ORIGINS` | CORS origins (required)      | `http://localhost:3000`              |

### Security Best Practices

1. **Production Deployment:**

   - Set `DEBUG=False` in production
   - Use strong, unique SECRET_KEY
   - Restrict ALLOWED_HOSTS to your domain only
   - Use secure database credentials

2. **Environment Files:**

   - `.env` - Your actual configuration (NEVER commit)
   - `.env.example` - Template file (safe to commit)

3. **Database Security:**
   - Use strong passwords
   - Limit database user permissions
   - Use SSL connections in production

### Error Handling

If you see `ImproperlyConfigured` errors, it means required environment variables are missing. Check that:

1. Your `.env` file exists
2. All required variables are set
3. No typos in variable names
4. Values are properly formatted (no quotes for simple strings)

### Development vs Production

**Development (.env):**

```bash
DEBUG=True
SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Production:**

```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Additional Security Measures

1. **Backup your `.env` file securely**
2. **Rotate secrets regularly**
3. **Monitor for environment variable leaks**
4. **Use different credentials for different environments**
