name: Auto Notes Publisher

on:
  schedule:
    - cron: '0 4 * * *' # Daily Subah 9:30 AM IST par automatic chalega
  workflow_dispatch: # Manual test button

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests

      - name: Run Auto Notes Script
        env:
          GEMINI_API_KEY: ${{ AQ.Ab8RN6LyUWNEtsO9GSWeIIwHj3fsNgriCz9C7OfGkczqvZPPrw}}
          TELEGRAM_BOT_TOKEN: ${{ 8808842597:AAGcbswkuYpLM1g5uBwJaWfHbuJlRkBzFk0 }}
          TELEGRAM_CHAT_ID: '@Govt_job_notes_bot' # Apne Telegram channel ka @username yahan likhein (quotes mein)
        run: python auto_notes.py
