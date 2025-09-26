# Samsung Blockchain Keystore & Knox Vault: Key Management Flow

---

## 1. Key Generation & Storage

- **Algorithms & Standards**
  - Mnemonic phrase generated with **BIP-39**.
  - Private key derived using **BIP-32/BIP-44** (ECDSA on secp256k1 curve).
- **Process**
  1. User initiates key creation.
  2. Mnemonic phrase generated.
  3. Private key derived from mnemonic.
  4. Private key encrypted and stored securely in **Knox Vault**.
- **Storage Location**
  - Keys are stored inside Knox Vault's tamper-proof secure processor and memory.
  - Encrypted using a device-unique **Physically Unclonable Function (PUF)** key, non-extractable.

---

## 2. Encryption & Secure Storage

- Private keys are encrypted using **AES-256** (likely GCM or CBC mode).
- Encryption key is derived internally from device's unique **PUF**.
- Keys are stored in Knox Vault’s isolated, non-volatile memory.
- Keys never leave Knox Vault nor are exposed to OS or cloud.

---

## 3. Decryption & Key Usage Flow

1. **App Requests Key Usage:**  
   - App requests signing or other sensitive operation using a secure API.
2. **User Authentication:**  
   - User authenticates via PIN, biometric, or password using Trusted UI.
   - Samsung Weaver protects against brute-force with retry limits/timeouts.
3. **Knox Vault Internal Operations:**  
   - Knox Vault verifies credentials.
   - Private key decrypted internally with PUF-derived key.
4. **Secure Output Returned:**  
   - Cryptographic operation (e.g., signature) performed inside Knox Vault.
   - Only the result (signature/auth token) is sent to the app.
   - Raw private key never leaves Knox Vault.

---

## 4. SDK Functions & APIs

| Function Name    | Description                                  |
|------------------|----------------------------------------------|
| `getAddress()`   | Returns public wallet address                 |
| `signTransaction()` | Signs data with private key inside Knox Vault |
| `importKey()`    | Imports an external key into secure storage  |
| `exportMnemonic()` | Displays recovery phrase securely via TUI    |

---

## 5. Security Guarantees

- Knox Vault is physically isolated from main processor.
- Tamper-resistant against side channel, fault injection, physical attacks.
- Private keys never exposed to OS, apps, or cloud.
- Authentication strictly enforced before any key operation.
- Encryption and decryption use hardware-rooted keys that are non-extractable.

---

## BIP-39 and BIP-32/44 Explained

### BIP-39: Mnemonic Phrase

- Generates a human-readable set of 12-24 words from random entropy.
- Provides a simple recovery phrase for backup and restore.
- Example phrase: `"guitar welcome sunset coconut ..."`.
- Used to generate the root seed for wallet keys.

### BIP-32 / BIP-44: Key Derivation

- Uses the BIP-39 seed to create a master private key.
- Derives many hierarchical private/public key pairs deterministically.
- BIP-44 sets a path structure for multi-account, multi-coin wallets.

**Example derivation path:**  
`m / 44' / 0' / 0' / 0 / 0`

- `m` - master key  
- `44'` - BIP-44 standard  
- `0'` - coin type (Bitcoin)  
- Subsequent parts designate accounts, change addresses, and indices

---

## Knox Vault Key Access Explained

### Steps during key operation:

1. **App Requests Key Usage:**  
   Calls secure API to use private key inside Knox Vault.

2. **User Authenticates:**  
   User confirms identity via PIN, password, or biometric.

3. **Knox Vault Verifies & Decrypts Internally:**  
   Credentials verified, private key decrypted inside secure enclave.

4. **Secure Output Returned:**  
   Result of cryptographic operation (signature, token) sent back.  
   Raw private key never exposed.

---

## Is Knox Vault Private Key Used for Encryption or Decryption?

- Keys are stored encrypted inside Knox Vault.
- When needed, decryption occurs **only inside Knox Vault’s secure processor**.
- Private key is used internally for both encryption and decryption actions (e.g., signing).
- Raw private key **never leaves** Knox Vault hardware, preventing leaks.

---

# Summary Flow Visual (Text Representation)

