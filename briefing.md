**Weekly Cybersecurity Briefing – 08 October 2026**  
*A quick, beginner‑friendly rundown of the biggest headlines, sorted from the most serious threats to the least, followed by three practical safety tips.*

---

## 1️⃣ Critical Vulnerabilities (Highest Risk)

| # | Issue | Impact | Current Status |
|---|-------|--------|----------------|
| 1 | **LMCache – Unpatched Remote Code Execution (RCE)** | Unauthenticated attackers can run code on any LMCache server (used by LLM platforms such as vLLM). | No patch available yet; mitigation is only to avoid exposing the service or to apply custom firewall rules. |
| 2 | **SonicWall SMA1000 – CVSS 10.0 Pre‑auth SSRF** | An unauthenticated attacker can send arbitrary requests through the gateway, potentially reaching internal network services. | Hotfixes released for four flaws; no known active exploitation yet. |
| 3 | **Atlassian (Jira/Confluence/Bitbucket) – CVE‑2026‑21589** | Unauthenticated attackers can exploit the flaw to gain access or cause denial of service. | Public PoC already out; attackers are already using it. |

> **Why this matters**: A CVSS of 10.0 is the maximum severity rating. If you run any of these services, patching or isolating them should be a top priority.

---

## 2️⃣ Ransomware & Backup Threats

| # | Issue | Target | Recommendation |
|---|-------|--------|----------------|
| 1 | **Backup Infrastructure Targeting** | Corporate backups, both off‑site and cloud, to erase recovery options. | Adopt *isolated, immutable, and regularly tested* backup copies that ransomware cannot reach. |

---

## 3️⃣ Data Breaches & Registry Hijacks

| # | Issue | Affected Domains | Key Take‑away |
|---|-------|-----------------|---------------|
| 1 | **.gh, .sl, .as Registry Hijack** | Any domain ending in `.gh`, `.sl` or `.as` that is registered through Google Domains. | Attackers issued forged HTTPS certificates, enabling man‑in‑the‑middle attacks. Verify SSL/TLS certificates for any site you visit. |

---

## 4️⃣ Malware & Supply‑Chain Attacks

| # | Campaign | Delivery | Impact |
|---|----------|----------|--------|
| 1 | **MALFEX (npm Supply‑Chain)** | Eight malicious npm packages downloaded 40 k+ times. | Carries an information‑stealer and a Remote‑Access Trojan (RAT). |
| 2 | **PoeLLM – AI Server Cryptomining** | Targets exposed AI and LLM infrastructure. | Converts servers into crypto‑mining botnets, draining resources. |

---

## 5️⃣ Other Notable Events

| # | Event | Key Point |
|---|-------|-----------|
| 1 | **Microsoft Outlook MSIX Block** | Outlook Web & the new Windows client will block `.msix` / `.msixbundle` attachments starting November. |
| 2 | **ShinyHunters & Related Arrests** | Arrests in Jordan and the Netherlands, plus increased attacks post‑arrest. |
| 3 | **U.S. Army Soldier Sentenced** | 70‑month sentence for hacking into AT&T & Verizon, stealing 100 M+ customer metadata. |
| 4 | **Radaris Domains Seized** | Court ordered transfer of Radaris.com and other data‑broker domains under New Jersey privacy law. |
| 5 | **Microsoft Patch Batch** | 974 security holes fixed in a single update—the largest batch ever. |

---

## 3 Safety Tips for Beginners

1. **Patch & Update First**  
   * Keep operating systems, firmware, and applications up‑to‑date. Install vendor‑provided security patches immediately, especially for known CVSS 10.0 or critical flaws.  

2. **Verify Certificates & Use MFA**  
   * Always inspect SSL/TLS certificates when accessing sensitive sites (especially new or unfamiliar domains).  
   * Enable multi‑factor authentication (MFA) on all services that support it—this blocks most credential‑stealing attacks.  

3. **Back Up & Test**  
   * Store backups in at least two isolated locations (e.g., local encrypted drive + off‑site cloud).  
   * Perform a full restore test quarterly to ensure data is recoverable without ransomware.  

> *Stay tuned each week for fresh threats and practical guidance. Remember, the simplest controls—patching, MFA, and tested backups—save the most lives.*