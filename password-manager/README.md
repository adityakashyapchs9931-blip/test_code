# Password Manager

A command-line password manager that encrypts and stores your credentials
locally using **Fernet (AES-128)** symmetric encryption. Access is protected
by a single master password.

## How it works

- Your master password is never stored. Instead, it's run through **PBKDF2-HMAC-SHA256**
  (390,000 iterations) with a random salt to derive an encryption key.
- All entries (service, username, password) are encrypted together and saved to `vault.json.enc`.
- The salt is stored separately in `vault.salt` (safe to store alongside the vault — it isn't secret).
- Wrong master password = decryption fails, so your data stays protected.

## Features

- Add, retrieve, list, and delete stored credentials.
- Built-in strong password generator (`secrets` module — cryptographically secure).
- Vault encrypted at rest; nothing is stored in plain text.

## Usage

```bash
pip install -r requirements.txt
python password_manager.py
```

You'll be prompted for your master password, then a menu lets you manage entries.

## Important notes

- **Don't lose your master password.** There is no recovery — that's the point of encryption.
- Add `vault.json.enc` and `vault.salt` to `.gitignore` before pushing to GitHub — never commit
  your actual vault to a public repo. (This repo's `.gitignore` already handles that.)
