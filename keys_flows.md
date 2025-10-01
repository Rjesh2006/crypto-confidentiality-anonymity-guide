# 🔐 End-to-End Encryption & Backup Security (WhatsApp / Signal Model)

This document explains **all components** of secure messaging with Double Ratchet, the protocols used, the keys involved, how they are generated, stored, rotated, and destroyed.

---

## 1. Protocols Used
- **X3DH (Extended Triple Diffie-Hellman):**
  - Used for initial key agreement when a session is created.
  - Combines identity keys, signed pre-keys, and one-time pre-keys.
- **Double Ratchet Algorithm:**
  - Used for ongoing messaging.
  - Provides **Forward Secrecy** and **Break-in Recovery**.
- **AES-256-CBC:** Symmetric encryption for messages & backups.
- **HMAC-SHA256:** Message authentication & integrity.
- **PBKDF2 / Argon2 / scrypt:** Key Derivation Functions (used for password → backup key).
- **Curve25519:** Elliptic curve used for key pairs (identity, pre-keys, ephemeral).

---

## 2. Types of Keys
### 🔑 Long-Term Keys
1. **Identity Key Pair (Curve25519)**
   - Generated on installation.
   - Private key: stored securely on device.
   - Public key: uploaded to server.
   - Purpose: uniquely identifies the user.

2. **Signed Pre-Key**
   - Medium-term (weeks/months).
   - Signed by identity key to prove authenticity.
   - Stored on server (public part).
   - Used for session setup.

3. **One-Time Pre-Keys**
   - Short-term, consumed once.
   - Stored on server (public part).
   - Used in first-time session setup for extra secrecy.

---

### 🔑 Ephemeral / Session Keys
4. **Ephemeral Key Pair**
   - Generated per new session or DH ratchet step.
   - Used in Diffie-Hellman exchanges.
   - Short-lived.

5. **Root Key**
   - Derived from shared master secret during X3DH.
   - Used to derive chain keys.

6. **Chain Keys**
   - Derived from root key.
   - Advanced (ratcheted) after each message.

7. **Message Keys**
   - Derived from chain key.
   - Used once per message (AES-256 + HMAC).
   - Deleted immediately after use.

---

### 🔑 Backup Keys
8. **Backup Encryption Key**
   - Protects chat history backups stored in cloud.
   - Two user options:
     - **Password → Backup Key:** Password processed with KDF → 256-bit key.
     - **64-digit Recovery Key:** Random 256-bit key generated locally on device.
   - Never uploaded to server.

---

## 3. Key Generation Timeline
1. **Installation**
   - Device generates:
     - Identity key pair (Curve25519).
     - Signed pre-key.
     - One-time pre-keys.
   - Public parts uploaded to server.

2. **Session Setup (when first message sent)**
   - Sender fetches recipient’s public keys.
   - Runs **X3DH** → produces master secret.
   - Root Key + Chain Keys derived.

3. **Messaging (Double Ratchet)**
   - For each message:
     - Chain Key → Message Key.
     - Encrypt message with AES-256.
     - Authenticate with HMAC-SHA256.
     - Advance chain key.
   - Occasionally exchange new ephemeral DH keys → resets chain keys.

4. **Backup (optional)**
   - User enables backup encryption.
   - Key generated:
     - If password: `BackupKey = KDF(password, salt, iterations)`.
     - If recovery key: `BackupKey = Random(256-bit)` → shown as 64-digit.
   - Backup file encrypted with `BackupKey`.

5. **Recovery**
   - User re-installs WhatsApp.
   - Re-registers phone via SMS OTP.
   - If backup exists:
     - Must provide password or 64-digit recovery key.
     - App decrypts backup with that key.
   - Without it → messages unrecoverable.

---

## 4. Key Lifetimes
- **Identity Key:** Permanent (until reinstall).
- **Signed Pre-Key:** Medium-term, rotated periodically.
- **One-Time Pre-Key:** Consumed once, replaced by server.
- **Ephemeral DH Keys:** Short-lived, used in DH ratchet steps.
- **Chain Keys:** Continuously replaced (ratchet).
- **Message Keys:** One-time only, immediately deleted.
- **Backup Encryption Key:** Persistent until changed/reset by user.

---

## 5. Security Properties
- **Forward Secrecy:**  
  Each message key is unique and deleted after use → old messages cannot be decrypted even if future keys are compromised.

- **Post-Compromise Security (Break-in Recovery):**  
  Even if attacker temporarily compromises device, new DH ratchets refresh chain → future communication secure again.

- **End-to-End Encryption:**  
  Only sender & recipient can derive the session keys → servers cannot decrypt.

- **Backup Security:**  
  Cloud backups encrypted with user-only known key → without password/recovery key, even the provider cannot decrypt.

---

## 6. Example Key Flow
```plaintext
[Install]
   |
   v
Identity Key + Pre-Keys generated
   |
   v
[Session Setup]
   |----> X3DH → Root Key
   v
[Messaging]
   |----> Double Ratchet
   |        |-> Chain Key -> Message Key (AES-256)
   |        |-> DH Ratchet refreshes root/chain keys
   v
[Backup Enabled]
   |----> Password → KDF → Backup Key
   |----> OR 64-digit Recovery Key (Random)
   v
[Recovery]
   |----> Enter password / recovery key
   |----> Decrypt backup
