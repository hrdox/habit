from pywebpush import Vapid

try:
    # Generate new keys
    vapid = Vapid()
    vapid.generate_keys()
    
    # Save to files (optional but good practice)
    vapid.save_key('private_key.pem')
    # Public key is derived, but let's print the base64url encoded public key for frontend use
    # and the private key path/content for backend use.
    
    print("KEYS GENERATED SUCCESSFULLY")
    
    # Vapid.public_key is an object, we need to get the public key in uncompressed format for web push
    # Actually, pywebpush Vapid class matches the library usage. 
    # Let's inspect what .public_key returns or how to get the claims.
    
    # It seems the easiest way to get the usage-ready keys is:
    print(f"PRIVATE_KEY_PATH: private_key.pem")
    
    # Getting the public key string for the frontend is tricky if we don't know the exact object structure.
    # Let's try to grab it from the Vapid object properties if possible or re-read the file.
    
    # Alternative:
    # Trigger a dummy claim to see headers? No.
    
    # Let's just use the file content.
    with open('private_key.pem', 'r') as f:
        print("PRIVATE_KEY_CONTENT:")
        print(f.read())

    # We also need the public key to put in applicationServerKey on frontend.
    # The 'Vapid' object in this library might have a method for it.
    # Let's try importing the helper.
    
    # Actually, let's use the `vapid.public_key` if it works, or we might need to derive it.
    # From source, `vapid.public_key` is an EllipticCurvePublicKey.
    
    from cryptography.hazmat.primitives import serialization
    
    public_key = vapid.public_key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # print("PUBLIC_KEY_PEM:")
    # print(public_pem.decode('utf-8'))
    
    # But for frontend we need base64url encoded raw bytes (uncompressed point) usually.
    # Or checking `vapid.get_public_key()`?
    
    # Let's try to use the library's internal way if possible. 
    # Actually, let's just dump the DER and base64url encode it for the frontend.
    
    # Standard Web Push requires the public key as a base64url encoded string of the uncompressed point.
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962, 
        format=serialization.PublicFormat.UncompressedPoint
    )
    
    import base64
    public_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').strip('=')
    print(f"PUBLIC_KEY_B64: {public_b64}")

except Exception as e:
    print(f"ERROR: {e}")
