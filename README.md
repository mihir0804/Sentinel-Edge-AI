# 🛡️ Sentinel Edge AI: Autonomous Local SOC

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Model](https://img.shields.io/badge/AI-Qwen_2.5_Nano-purple?style=for-the-badge)](https://ollama.com/library/qwen2.5)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange?style=for-the-badge&logo=gradio&logoColor=white)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **A privacy-first Autonomous Security Agent that ingests server logs, identifies cyberattacks using local Edge AI, and generates audit-ready PDF reports.**

---

## 📸 Project Overview

**Sentinel Edge AI** is a locally hosted Security Operations Center (SOC) tool designed to automate threat analysis without compromising data privacy. Unlike cloud-based solutions, Sentinel runs entirely on **localhost**, ensuring sensitive server logs never leave the secure network.

It utilizes the **Qwen 2.5 (1.5B)** quantized model, optimized via **System Prompt Engineering** to achieve high-accuracy threat classification (SQLi, XSS, RCE) on consumer hardware with < 4GB RAM.

![Dashboard Preview](<img width="1872" height="942" alt="Dashboard_Screenshot_Of_Sentinel Edge AI" src="https://github.com/user-attachments/assets/4a23ee68-5ad7-432a-bdf9-f962ac9683c4" />

)


---

## 🚀 Key Features

* **🧠 Edge Intelligence Engine:** Powered by `qwen2.5:1.5b` (via Ollama) for sub-second inference on standard laptops.
* **🎯 Rule-Guided Classification:** Uses strict prompt engineering to correctly classify complex attacks like **Command Injection**, **Path Traversal**, and **Blind SQLi** that smaller models usually miss.
* **📄 Automated Reporting:** One-click generation of professional PDF Incident Reports containing evidence, analysis, and remediation steps.
* **🔒 Privacy-First:** 100% offline capability. No API keys, no cloud data leaks.
* **💻 Dark Mode Interface:** Professional Gradio-based UI designed for security analysts.

---

## 🛠️ Architecture

```mermaid
graph TD
    A[User / Analyst] -->|Raw Log Entry| B(Gradio Interface)
    B -->|Sanitized Input| C{Python Logic Controller}
    C -->|API Request| D[Ollama Local Inference Server]
    D -->|Model: qwen2.5:1.5b| D
    D -->|Threat Analysis| C
    C -->|Structured Data| E[PDF Generator Engine]
    E -->|Downloadable Report| A
