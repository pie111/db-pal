# dbpal

Your friendly database companion - A powerful tool that uses LLM to help with database operations.

## Installation

### From PyPI
```bash
pip install dbpal
```

### From Source
```bash
git clone https://github.com/yourusername/dbpal.git
cd dbpal
pip install -e .
```

## Usage

### Basic Commands
```bash
# Start dbpal
dbpal

# Configure API key
dbpal --api-key YOUR_API_KEY

# Configure database connection
dbpal --db-host localhost --db-user myuser --db-password mypass --db-name mydb
```

### Configuration
dbpal stores configuration in `~/.dbpal/config.json`. Sensitive data (API keys and database credentials) are encrypted at rest.

## Security Features

- **Encrypted Storage**: All sensitive data (API keys, database credentials) are encrypted using Fernet symmetric encryption
- **Secure File Permissions**: Configuration files and encryption keys are stored with restrictive permissions (600)
- **Input Validation**: All user inputs are validated before being stored
- **Secure Configuration Directory**: The configuration directory is created with restrictive permissions (700)

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
