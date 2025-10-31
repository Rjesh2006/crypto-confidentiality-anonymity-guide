# Signal Protocol

## Overview

The Signal Protocol is an end-to-end encryption protocol that provides perfect forward secrecy and breaks long-term keys into per-message keys. It is the cryptographic protocol used by Signal, WhatsApp, and other messaging platforms to secure communications.

## Key Components

### 1. X3DH (Extended Triple Diffie-Hellman)

X3DH is the initial key agreement protocol that establishes a shared secret between two parties who have never communicated before.

**Three main purposes:**
- Authenticate the identity of both parties
- Establish a shared secret for symmetric encryption
- Provide forward secrecy from the first message

### 2. Double Ratchet Algorithm

After X3DH establishes the initial shared secret, the Double Ratchet algorithm ensures that every message has its own unique encryption key, providing both forward and future secrecy.

---

## Phase 1: Setup and Key Generation

### Bob's Actions (Receiver)

| Step | Action | Purpose |
|------|--------|---------|
| B1 | Generate Identity Key (IK_B), Signed Pre-Key (SPK_B signed by IK_B), and multiple One-Time Pre-Keys (OPK_B[n]) | Establishes long-term identity, medium-term authentication, and single-use forward secrecy keys |
| B2 | Optionally generate PQKEM keypair | Enables post-quantum cryptographic security |
| B3 | Upload key bundle to server: {IK_B, SPK_B_signature, OPK_B, PQKEM_pub} | Makes keys available for Alice to initiate sessions while Bob is offline |

### Alice's Actions (Initiator)

| Step | Action | Purpose |
|------|--------|---------|
| A1 | Fetch Bob's public key bundle from server | Prepares for secure session setup |
| A2 | Verify SPK_B signature using IK_B_pub | Ensures Bob's pre-key is authentic and not tampered with |

---

## Phase 2: Key Exchange and Derivation

### Alice's Key Derivation

| Step | Action | Purpose |
|------|--------|---------|
| A3 | Generate fresh Ephemeral Key (EK_A) and optional PQKEM keypair | Provides forward secrecy and uniqueness for this specific session |
| A4 | Perform four Diffie-Hellman operations: DH1, DH2, DH3, DH4 | Derives shared secret components from identity and ephemeral keys |
| A5 | Concatenate all DH results and apply KDF-SHA256 | Combines all shared secret components into a single Root Key (RK) |
| A6 | Send initial message to server with {EK_A_pub, identifiers, optional PQ data} | Initiates encrypted communication with Bob |

**The Four DH Operations:**
```
DH1 = DH(IK_A, SPK_B)    // Alice's identity with Bob's signed pre-key
DH2 = DH(EK_A, IK_B)     // Alice's ephemeral with Bob's identity
DH3 = DH(EK_A, SPK_B)    // Alice's ephemeral with Bob's pre-key
DH4 = DH(EK_A, OPK_B)    // Alice's ephemeral with Bob's one-time key
```

### Bob's Key Derivation

| Step | Action | Purpose |
|------|--------|---------|
| B4 | Server delivers Alice's initial message to Bob | Message is queued until Bob comes online |
| B5 | Locate the OPK_B that Alice used | Ensures one-time key usage tracking |
| B6 | Perform the same four DH operations | Derives the identical Root Key (RK) as Alice |
| B7 | Delete the used OPK_B from storage | Maintains forward secrecy by preventing one-time key reuse |

**Bob computes the same DH operations:**
```
DH1 = DH(IK_B, EK_A)     // Bob's identity with Alice's ephemeral
DH2 = DH(SPK_B, EK_A)    // Bob's pre-key with Alice's ephemeral
DH3 = DH(SPK_B, EK_A)    // Bob's pre-key with Alice's ephemeral
DH4 = DH(OPK_B, EK_A)    // Bob's one-time key with Alice's ephemeral
```

Note: DH is commutative, so DH(A,B) = DH(B,A), allowing both parties to compute the same shared secret.

---

## Phase 3: Key Purposes and Security Properties

| Key | Purpose | Security Property |
|-----|---------|-------------------|
| IK_A / IK_B | Authenticate identities of Alice and Bob | Identity verification and non-repudiation |
| SPK_B | Supports offline session setup and prevents replay attacks | Medium-term authentication without online server |
| OPK_B | Strengthens forward secrecy for the initial message | Even if SPK_B is compromised, first message stays secure |
| EK_A | Provides ephemeral session-level secrecy | Session isolation - each conversation is independent |
| Root Key (RK) | Master key fed into Double Ratchet algorithm | Foundation for per-message key derivation |

---

## Phase 4: Transition to Double Ratchet

Once X3DH establishes the Root Key, the Double Ratchet algorithm takes over:

| Step | Action | Benefit |
|------|--------|---------|
| R1 | Initialize Double Ratchet with Root Key | Begins continuous key derivation process |
| R2 | Generate unique symmetric key for each message | Every message encrypted with a different key |
| R3 | Implement DH ratchet and symmetric ratchet | Provides both forward and future secrecy |
| R4 | Perfect forward secrecy in action | Past messages remain secure even if current keys are compromised |

### Double Ratchet Properties:

- **Forward Secrecy**: If a session key is compromised, past messages remain secure because they used different keys
- **Future Secrecy**: If a session key is compromised, future messages become secure again after one ratchet step
- **Out-of-order message handling**: Messages can be decrypted even if received out of order
- **Key expiration**: Old keys are deleted after use, preventing accidental reuse

---

## Security Guarantees

### What Signal Protocol Protects Against

✅ **Perfect Forward Secrecy**: Compromised long-term keys do not compromise past messages  
✅ **Replay Attack Prevention**: Signed pre-keys and ratcheting prevent message replay  
✅ **Man-in-the-Middle (MITM) Prevention**: Identity key authentication prevents imposters  
✅ **Passive Eavesdropping**: End-to-end encryption prevents server from reading messages  
✅ **Key Compromise**: One-time pre-keys and ratcheting limit damage from compromised keys  

### What Signal Protocol Does NOT Protect Against

❌ Metadata (who talks to whom, when, message count)  
❌ Compromised devices running the application  
❌ Physical attacks on devices in use  
❌ Quantum computers (unless using PQKEM hybrid variant)

---

## Post-Quantum Extension (PQKEM)

The Signal Protocol can be enhanced with post-quantum resistant cryptography:

| Component | Classical | Post-Quantum |
|-----------|-----------|--------------|
| DH Operations | Elliptic Curve DH | EC-DH + PQKEM |
| Key Encapsulation | Direct DH output | DH output + PQKEM shared secret combined |
| Security Level | Secure against classical computers | Secure against both classical and quantum computers |

**How it works:**
```
Root Key = KDF(DH1 || DH2 || DH3 || DH4 || PQKEM_shared_secret)
```

This ensures that even if quantum computers break DH in the future, the PQ shared secret keeps the encryption secure.

---

## Implementation Overview

```
┌─────────────────────────────────────────────────────────┐
│              Signal Protocol Stack                      │
├─────────────────────────────────────────────────────────┤
│  Application Layer (Messages)                           │
├─────────────────────────────────────────────────────────┤
│  Double Ratchet (Per-message encryption keys)           │
├─────────────────────────────────────────────────────────┤
│  X3DH (Initial key agreement)                           │
├─────────────────────────────────────────────────────────┤
│  Cryptographic Primitives                               │
│  - AES-256-CBC (symmetric encryption)                   │
│  - HMAC-SHA256 (authentication)                         │
│  - Curve25519 (elliptic curve DH)                       │
│  - SHA-256 (key derivation)                             │
├─────────────────────────────────────────────────────────┤
│  Transport Layer (Network)                              │
└─────────────────────────────────────────────────────────┘
```

---

## Sequence Example

```
Alice                           Server                          Bob
  |                              |                              |
  |------- Fetch Bob's Bundle ---|                              |
  |<----- IK_B, SPK_B, OPK_B ----|                              |
  |                              |                              |
  |--- Verify SPK_B Signature ---|                              |
  |--- Generate EK_A -----------|                              |
  |--- Compute DH1, DH2, DH3, DH4                              |
  |--- Derive Root Key ---------|                              |
  |                              |                              |
  |------- Send {EK_A, Msg} ----|                              |
  |                              |------- Deliver to Bob -------->
  |                              |                              |
  |                              |        Receive message       |
  |                              |        Perform same DH ops   |
  |                              |        Derive Root Key       |
  |                              |        Delete OPK_B          |
  |                              |<----- Initialize Ratchet ----
  |                              |                              |
  |<----- Both have shared RK, begin Double Ratchet encryption-->
  |
```

---

## References

- [Signal Protocol Specifications](https://signal.org/docs/)
- [Double Ratchet Algorithm (RFC 9420)](https://www.rfc-editor.org/rfc/rfc9420.html)
- [X3DH Key Agreement](https://signal.org/docs/specifications/x3dh/)
- [Curve25519 Elliptic Curves](https://cr.yp.to/ecdh.html)

---

## Summary

The Signal Protocol combines X3DH for initial key agreement with the Double Ratchet algorithm for continuous per-message key derivation. This two-layer approach provides:

1. **Strong initial authentication** via X3DH
2. **Perfect forward secrecy** through ephemeral keys and one-time pre-keys
3. **Per-message security** via Double Ratchet
4. **Offline capability** through pre-key bundles
5. **Post-quantum readiness** with optional PQKEM

This makes Signal Protocol one of the most secure and widely-adopted end-to-end encryption protocols in the world.

## Here we have the Flowchart that make it more easy to get in
![spv3](https://github.com/user-attachments/assets/2f591170-2bd9-4e7b-a65c-0f49ea2de626)
<svg id="export-svg" width="100%" xmlns="http://www.w3.org/2000/svg" class="flowchart" style="max-width: 1376px; background: rgb(255, 255, 255);" viewBox="0 0 1376 3930" role="graphics-document document" aria-roledescription="flowchart-v2">

