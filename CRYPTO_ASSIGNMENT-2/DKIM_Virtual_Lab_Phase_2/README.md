# DKIM Virtual Laboratory – Phase 2

A classroom simulation of DKIM signing and verification.

DKIM is not an encryption/decryption algorithm, so the lab visualizes digital signing, transmission, verification, and tampering detection.

## Run
```bash
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## Demonstration
1. Use the default Shivaraj → Sathwik email.
2. Click **Generate DKIM Signature**.
3. Keep the received message unchanged and click **Verify DKIM** → success.
4. Change the received message and click **Verify DKIM** → failure.
5. Capture screenshots for the PDF submission.
