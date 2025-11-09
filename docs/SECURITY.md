# Security Guide - API Key Management

## Overview

This project uses OpenAI API keys for transcription and summarization. This guide explains how to securely manage your API keys.

## Security Measures Implemented

### 1. ✅ Environment Variables Only
- API keys are **never** hardcoded in source files
- Keys are loaded from environment variables or `.env` file
- All code uses `os.getenv("OPENAI_API_KEY")` - never hardcoded values

### 2. ✅ .env File Support
- `.env` file is in `.gitignore` - **never committed to git**
- `.env.example` template provided (safe to commit)
- `python-dotenv` automatically loads `.env` if present
- Falls back to system environment variables if `.env` not found

### 3. ✅ Secure File Permissions
- `.env` file should have permissions `600` (owner read/write only)
- Never world-readable or group-readable

### 4. ✅ No Key Exposure in Code
- Error messages never expose API keys
- Debug logging never includes keys
- All key access is through environment variables

### 5. ✅ Git Safety
- `.env` is in `.gitignore`
- `.env.local`, `*.key`, `*.pem` also ignored
- Git history checked for any accidental commits

## Setup Instructions

### Option 1: Using .env File (Recommended)

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env and add your API key:**
   ```bash
   # Edit .env file
   nano .env
   # or
   vim .env
   ```
   
   Add your key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. **Set secure permissions:**
   ```bash
   chmod 600 .env
   ```

4. **Verify it's not tracked by git:**
   ```bash
   git status
   # .env should NOT appear in the list
   ```

### Option 2: Using System Environment Variable

```bash
# Set for current session
export OPENAI_API_KEY="sk-your-actual-key-here"

# Or add to ~/.bashrc or ~/.zshrc for persistence
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Verification

### Check if key is loaded:
```python
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENAI_API_KEY")
if key:
    print(f"✅ Key loaded (length: {len(key)} chars)")
    print(f"   First 7 chars: {key[:7]}...")  # Should show "sk-..."
else:
    print("❌ Key not found")
```

### Test the pipeline:
```bash
python3 run_pipeline.py "https://www.youtube.com/watch?v=example"
```

## Security Best Practices

### ✅ DO:
- ✅ Use `.env` file for local development
- ✅ Set `.env` permissions to `600` (owner only)
- ✅ Use system environment variables in production
- ✅ Rotate keys regularly
- ✅ Use separate keys for development/production
- ✅ Monitor API usage in OpenAI dashboard
- ✅ Set usage limits in OpenAI dashboard

### ❌ DON'T:
- ❌ Never commit `.env` to git
- ❌ Never hardcode keys in source files
- ❌ Never share keys in chat/email
- ❌ Never commit keys to public repositories
- ❌ Never log or print API keys
- ❌ Never use keys with world-readable permissions

## Key Rotation

If your key is compromised:

1. **Revoke the key immediately:**
   - Go to https://platform.openai.com/api-keys
   - Delete the compromised key

2. **Generate a new key:**
   - Create a new API key in OpenAI dashboard

3. **Update your .env file:**
   ```bash
   # Edit .env
   OPENAI_API_KEY=sk-new-key-here
   ```

4. **Verify it works:**
   ```bash
   python3 -c "from transcript.transcribe import check_openai_available; print(check_openai_available())"
   ```

## Checking for Exposed Keys

### Check git history:
```bash
# Search git history for API keys
git log -p | grep -i "sk-"
git log -p | grep -i "OPENAI_API_KEY"
```

### Check current files:
```bash
# Search for hardcoded keys
grep -r "sk-" . --exclude-dir=.git --exclude="*.md"
grep -r "OPENAI_API_KEY.*=" . --exclude-dir=.git --exclude="*.md" --exclude=".env*"
```

## Troubleshooting

### Key not found:
- Check `.env` file exists and has correct format
- Verify permissions: `ls -l .env` (should show `-rw-------`)
- Check environment variable: `echo $OPENAI_API_KEY`
- Restart terminal after setting environment variable

### Key invalid:
- Verify key format starts with `sk-`
- Check key hasn't expired in OpenAI dashboard
- Ensure no extra spaces in `.env` file
- Try regenerating key in OpenAI dashboard

## Additional Resources

- OpenAI API Keys: https://platform.openai.com/api-keys
- OpenAI Usage Dashboard: https://platform.openai.com/usage
- python-dotenv docs: https://pypi.org/project/python-dotenv/


