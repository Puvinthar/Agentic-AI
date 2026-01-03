# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Security vulnerabilities should not be disclosed publicly until fixed.

### 2. Report Privately

Email security details to: **your.email@example.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Time

- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Fix timeline**: Varies based on severity

### 4. Disclosure

Once fixed, we will:
1. Release a security patch
2. Credit you (if desired)
3. Publish a security advisory

## Security Best Practices

### Environment Variables

- Never commit `.env` files
- Use strong database passwords
- Rotate API keys regularly
- Use secrets management in production

### API Keys

- Keep API keys private
- Use environment variables
- Implement rate limiting
- Monitor API usage

### Database

- Use strong passwords
- Enable SSL for connections
- Regular backups
- Limit database permissions

### Deployment

- Use HTTPS in production
- Enable CORS properly
- Implement authentication
- Regular security audits
- Keep dependencies updated

## Known Security Considerations

1. **File Uploads**: Limited to 50MB, specific file types only
2. **API Rate Limiting**: Implement in production
3. **Input Validation**: All inputs are validated
4. **SQL Injection**: Using ORM (SQLAlchemy) for protection
5. **XSS Protection**: Input sanitization enabled

## Dependencies

We regularly update dependencies to patch security vulnerabilities:

```bash
pip install --upgrade -r requirements.txt
```

## Security Updates

Subscribe to security advisories:
- Watch this repository
- Enable GitHub security alerts
- Check releases regularly

Thank you for helping keep Agentic AI secure! 🔒
