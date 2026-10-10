from flask import Flask, render_template, request, jsonify
import base64, hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

app = Flask(__name__)
PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PUBLIC_KEY = PRIVATE_KEY.public_key()
DOMAIN = "example.com"
SELECTOR = "student"

def body_hash(message):
    return base64.b64encode(hashlib.sha256(message.encode("utf-8")).digest()).decode("ascii")

def signing_data(sender, receiver, subject, bh):
    header_fields = [
        f"from:{sender}",
        f"to:{receiver}",
        f"subject:{subject}",
        f"bh:{bh}",
    ]
    return "\n".join(header_fields)

def make_signature(sender, receiver, subject, bh):
    data = signing_data(sender, receiver, subject, bh).encode("utf-8")
    sig = PRIVATE_KEY.sign(data, padding.PKCS1v15(), hashes.SHA256())
    return base64.b64encode(sig).decode("ascii")

def make_header(bh, sig):
    return f"v=1; a=rsa-sha256; d={DOMAIN}; s={SELECTOR}; h=from:to:subject; bh={bh}; b={sig}"

def public_key_pem():
    return PUBLIC_KEY.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()

@app.route("/")
def index():
    return render_template("index.html", public_key=public_key_pem())

@app.post("/sign")
def sign():
    d = request.get_json() or {}
    sender, receiver, subject, message = [d.get(k, "").strip() for k in ("sender","receiver","subject","message")]
    if not all((sender, receiver, subject, message)):
        return jsonify(error="Please fill all email fields."), 400
    bh = body_hash(message)
    sig = make_signature(sender, receiver, subject, bh)
    return jsonify(body_hash=bh, signature=sig, dkim_header=make_header(bh, sig), signing_data=signing_data(sender, receiver, subject, bh))

@app.post("/verify")
def verify():
    d = request.get_json() or {}
    sender, receiver, subject = [d.get(k, "").strip() for k in ("sender","receiver","subject")]
    original, received, sig = [d.get(k, "").strip() for k in ("original_message","received_message","signature")]
    if not all((sender, receiver, subject, original, received, sig)):
        return jsonify(error="Please sign an email first and enter the received message."), 400
    oh, rh = body_hash(original), body_hash(received)
    try:
        PUBLIC_KEY.verify(
            base64.b64decode(sig),
            signing_data(sender, receiver, subject, oh).encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        valid = True
    except Exception:
        valid = False
    return jsonify(original_hash=oh, received_hash=rh, hash_match=(oh == rh), signature_valid=valid, success=(oh == rh and valid))

if __name__ == "__main__":
    app.run(debug=True)
