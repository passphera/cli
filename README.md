# passphera cli

A robust command-line interface tool for generating and managing strong passwords using cryptographic algorithms.

## Features

- 🔐 Strong password generation with customizable encryption settings
- 🔄 Multiple cipher algorithms support
- 👤 User authentication system
- 📦 Local password vault
- ☁️ Cloud sync capabilities
- 🛠️ Extensive configuration options

## Installation

[Download from this link](https://github.com/passphera/cli/releases/)

## Quick Start

1. Sign up for an account:
```bash
passphera auth signup -e your@email.com -n username -p your_password
```

2. Log in:
```bash
passphera auth login -e your@email.com -p your_password
```

3. Generate a password:
```bash
passphera passwords generate -t "base_text" -c "password_context"
```

4. Retrieve a saved password:
```bash
passphera vault get "password_context"
```

## Command Groups

### Authentication Commands (`auth`)
- `login` - Log in with email and password
- `logout` - Log out from the current session
- `signup` - Create a new account
- `whoami` - Display current user credentials

### Generator Commands (`generator`)
Configure password generation settings:
- Change encryption algorithm: `set-algorithm <algorithm>`
- Set encryption key: `set-key <key>`
- Adjust shift amount: `set-shift <amount>`
- Set multiplier: `set-multiplier <value>`
- Add prefix/postfix: `set-prefix/set-postfix <text>`
- Character replacements: `set-replacement <char> <replacement>`

All settings can be reset to defaults using corresponding `reset-*` commands.

### Password Management (`passwords`)
- `generate` - Create new passwords
- `update` - Modify existing passwords
- `delete` - Remove passwords

### Vault Operations (`vault`)
- `get` - Retrieve a specific password
- `get-all` - List all saved passwords
- `clear` - Remove all saved passwords
- `sync` - Synchronize with cloud storage

## Configuration Examples

### Basic Password Generation
```bash
# Generate a password for GitHub account
passphera passwords generate -t "github 1234 master" -c "github"

# Retrieve the password later
passphera vault get "github"
```

### Custom Encryption Settings
```bash
# Configure custom encryption settings
passphera generator set-algorithm "playfair"
passphera generator set-key "my_secret_key"
passphera generator set-shift 5
passphera generator set-multiplier 3
passphera generator set-prefix "prefix_"
passphera generator set-postfix "_suffix"

# Apply character replacements
passphera generator set-character "a" "4@"
passphera generator set-character "e" "3*e1"
```

### Cloud Synchronization
```bash
# Sync generator settings
passphera generator sync

# Sync vault data
passphera vault sync
```

## Options

Global options available for all commands:
- `-h, --help` - Show help message

## Security Best Practices

1. Always use a strong master password for your account
2. Regularly sync your vault if using cloud features
3. Clear your vault data when needed using `vault clear`
4. Avoid sharing your encryption keys
5. Regularly update your saved passwords

## Development

The project is open source and welcomes contributions. Please follow these steps to contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the Apache License, Version 2.0 - see [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or need assistance:

- 📝 [Open an issue](https://github.com/passphera/cli/issues) on our GitHub repository
- 📧 Contact maintainers at: [passphera@gmail.com]
