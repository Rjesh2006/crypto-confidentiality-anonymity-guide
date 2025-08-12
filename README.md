# Privacy & Anonymity in Cryptocurrency — A Concise Guide

This repository explains key technologies that protect **confidentiality** (hiding transaction details) and **anonymity** (hiding identities), along with the real-world methods governments use to investigate or deanonymize blockchain activity.

---

## Privacy Technologies

### **ZK-SNARKs** (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge)
- **Purpose:** Prove a statement is true without revealing *why* it’s true.
- **Benefits:**  
  - Confidentiality: transaction amounts and participants can be hidden.  
  - Anonymity: identities remain undisclosed.  
  - Efficiency: small proofs, fast verification.  
- **Four main ingredients:**
  1. **Polynomial arithmetic over finite fields** — translates computation into equations.
  2. **Quadratic Arithmetic Programs (QAPs)** — represent computation as polynomial constraints.
  3. **Homomorphic-style cryptography** — enables checking without revealing the underlying data.
  4. **Trusted setup** — initial secret parameters; if leaked, privacy can be broken.
- **Used in:** Zcash, privacy-focused rollups.

---

### **CoinJoin**
- **Purpose:** Obfuscate transaction paths in Bitcoin.
- **How it works:**
  - Multiple users combine their inputs and outputs in one transaction.
  - Observers see a large mixed transaction, not direct sender → receiver links.
- **Limitations:**  
  - Does not hide amounts.  
  - Susceptible to amount-pattern analysis.  
- **Tools:** Wasabi Wallet, JoinMarket.

---

### **Monero**
- **Purpose:** Privacy-by-default cryptocurrency.
- **Techniques used:**
  - **Ring Signatures:** Conceal the actual spender among a set of decoys.
  - **Stealth Addresses:** One-time addresses per transaction to hide recipient identity.
  - **RingCT (Confidential Transactions):** Conceals transaction amounts.
  - **Dandelion++:** Obfuscates transaction origin on the network layer.
- **Facts:**  
  - No transparent ledger view like Bitcoin.  
  - Designed to resist blockchain analysis.

---

### **Threshold Cryptography**
- **Purpose:** Distribute control of a private key across multiple parties.
- **How it works:** A threshold number (`t`) of `n` total shares is required to perform actions.
- **Uses:** Multi-party signing, secure custody, reducing single-point failure risk.
- **Example:** `2-of-3` wallet signing for exchanges.

---

### **BOLTs** (Basis of Lightning Technology)
- **Purpose:** Define Lightning Network protocol rules for payment channels.
- **Privacy aspects:**  
  - Onion routing for payments (similar to Tor).  
  - BOLT 12: reusable invoices with privacy improvements.
- **Facts:** BOLTs are specification documents, not code.

---

## How Governments & Law Enforcement Deanonymize

### **1. Blockchain Analytics**
- Cluster related addresses, trace fund flows to exchanges or known entities.
- Identify patterns even in mixed or shielded transactions.
- Tools: Chainalysis, Elliptic, CipherTrace.

### **2. Honeypots**
- Fake wallets, mixers, or services that attract privacy-seeking users.
- Collect IP addresses, browser metadata, and blockchain addresses.
- Can lead to direct identification.

### **3. Subpoenas to Exchanges**
- Target KYC/AML-compliant exchanges for user data.
- Exchanges act as on/off-ramps linking blockchain addresses to real identities.

### **4. Exploiting Protocol Flaws**
- Example: Small Monero ring sizes in early versions allowed partial tracing.
- Weak implementations or cryptographic parameters can leak data.
- User mistakes like address reuse also break privacy.

### **5. Network-Level Surveillance**
- Monitor IP traffic and timing correlations to link transactions to users.
- Use of VPN/Tor reduces risk but is not foolproof.

### **6. Human Factors**
- Undercover infiltration of forums, marketplaces, or wallet support channels.
- Social engineering or informants used to gather information.

---

## Key Facts
- **Confidentiality** hides *what* happened in a transaction (amounts, details).
- **Anonymity** hides *who* was involved.
- True privacy requires both — most tools focus more on one than the other.
- Even strong cryptography can fail if user habits or implementations are weak.

---

**Purpose:**  
To provide a brief but clear overview of privacy tools, their cryptographic foundations, and the investigative methods used to break them — for researchers, privacy advocates, and crypto users.

---

**License:** MIT — You may freely use, modify, and share this content.
