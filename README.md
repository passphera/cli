# passphera CLI

A minimal yet powerful command-line interface for generating and managing strong passwords, built on top of the **passphera core** philosophy: *"your text becomes your key to secure passwords."*

## Features

* 🔐 Password generation from any text input
* 🔄 Multiple cipher algorithms support (Affine, Hill, Playfair, etc.)
* 🧩 Configurable steps (prefix, postfix, replacements, etc.)
* 📦 Local password vault (TinyDB for CLI)
* 🛠️ Flexible generator settings per user
* 🚀 Fully offline by default

## Installation

[Download the latest release](https://passphera.imfathi.com/)

## Quick Start

1. Generate a password:

```bash
passphera generate -t "my password for twitter" -c "twitter"
```

2. Retrieve it later:

```bash
passphera vault get "twitter"
```

## Command Groups

* `generate` - Alias to `vault add`

### Generator Commands (`generator`)

### Vault Commands (`vault`)

* `add` - Generate a new password and optionally save it to the vault
* `get` - Get saved password from the vault
* `update` - Update password in the vault
* `delete` - Delete saved password from the vault
* `list` -Get all saved passwords from the vault
* `flush` - Flush the vault (delete all passwords)
* `sync` - Sync down from the cloud

Configure password generation:

* `show` - Show generator settings
* `set <prop> <algorithm>` – Set a new value to a property
* `reset <prop> <algorithm>` – Reset a property to its default value
* `set-replacement <char> <replacement>` – Replace a character with a replacement string
* `reset-replacement <char> <replacement>` – Reset a character's replacement
* `sync` – Sync local settings with cloud settings id logged in

### Authentication Commands (`auth`)

* `login` - Login to the app server with email and password
* `logout` - Logout from the app server
* `signup` - Register a new user on the app server
* `whoami` - Get user credentials

## Examples

### Basic

```bash
# Generate and store
passphera generate -t "github personal account" -c "github"  # or passphera vault add

# Retrieve
passphera vault get "github"
```

### Custom Generator Settings

```bash
# Configure generator
passphera generator set algorithm "playfair"
passphera generator set key "secret"
passphera generator set prefix "prefix_"
passphera generator set postfix "_suffix"
passphera generator set-replacement "a" "@25"
```

### Global options


* `-v, --version` – Show version and exit
* `-h, --help` – Show help message and exit

## Development

Open source, contributions welcome!

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

## License

Licensed under Apache License 2.0 – see [LICENSE](LICENSE).

## Support

* 📝 [GitHub Issues](https://github.com/passphera/cli/issues)
* 📧 Contact: \[[passphera@imfathi.com](mailto:passphera@imfathi.com)]
