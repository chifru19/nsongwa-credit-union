# 🏦 Nsongwa Bank: Secure Financial Gateway
**Status:** 🟢 Operational | **Security Audit:** ✅ Passed (Checkov v3.2.506)

This repository contains the containerized core banking engine for Nsongwa Credit Union. It is built using a **Security-First** approach to protect member data and ensure 24/7 service availability.

## 🛡️ Security & Compliance Features
* **Least Privilege Execution**: The application runs as a dedicated `bankuser` (non-root) to prevent system-wide breaches.
* **Infrastructure-as-Code Auditing**: Every deployment is scanned by **Checkov** to ensure compliance with financial security standards.
* **Automated Health Monitoring**: Built-in `HEALTHCHECK` protocols monitor the application heartbeat every 30 seconds.
* **Network Isolation**: Secure internal bridging prevents unauthorized external access to the banking API.

## 🚀 Deployment Instructions
To launch the secure environment locally for a Board demonstration:

1.  **Build and Start**:
    ```bash
    docker-compose up --build
    ```
2.  **Verify Service**:
    Access the Member Balance API at: `http://localhost:5000/api/v1/balance`.

## 📊 Technical Stack
* **Language**: Python 3.9-slim (Hardened Base Image)
* **Orchestration**: Docker Compose
* **Security Scanner**: Checkov
* **CI/CD**: GitHub Actions

---
*© 2026 Nsongwa Credit Union Digital Transformation Project*