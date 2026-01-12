

# 🩺 ASHA Sahayi

**A Privacy-First, Logic-Based Telegram Bot for Frontline Health Workers**

ASHA Sahayi is a Telegram-based digital assistant designed to support **ASHA (Accredited Social Health Activist) workers** by providing **safe health guidance**, **emergency detection**, **follow-up monitoring**, and **supervisor escalation**, while strictly preserving **patient and worker privacy**.

This project was developed as part of the technical task for the **UNESCO Chair on Gender Equality and Women’s Empowerment (AMMACHI Labs)**.

---

## 🎯 Problem Statement

Frontline health workers often need **quick, reliable guidance** while working in:

* Low-resource environments
* Limited internet connectivity
* High-risk medical situations

Using unrestricted generative AI in healthcare can be unsafe due to:

* Unpredictable responses
* Hallucinated diagnoses
* Privacy risks

ASHA Sahayi addresses this by using a **logic-based medical reasoning system** instead of generative AI.

---

## 🧠 Why Logic-Based Instead of Generative AI?

ASHA Sahayi **intentionally avoids generative AI for medical decision-making**.

### Reasons:

* Healthcare requires **predictable and auditable behaviour**
* Generative AI can produce unsafe or incorrect medical advice
* ASHA workers must be protected from medical and legal liability

### Advantages of Logic-Based Reasoning:

* Deterministic, rule-driven responses
* No hallucinated diagnoses or medicine names
* Works reliably in low-connectivity settings
* Easier to validate, audit, and improve safely
* No sensitive data sent to external AI servers

ASHA Sahayi acts as a **decision-support tool**, not a medical authority.

---

## ✨ Key Features

### ✅ Symptom-Based Guidance

* Accepts input in **Tamil, English, and Tanglish**
* Handles common symptoms:

  * Fever
  * Cough
  * Stomach issues
  * Weakness

### 🚨 Emergency Detection

* Identifies critical symptoms such as:

  * Blood vomit
  * Blood in stool
* Immediately advises **hospital referral**
* Skips all home remedies for emergencies

### ⏱️ Duration-Aware Advice

* Considers how long symptoms have lasted (e.g., *“2 naal”*, *“3 days”*)
* Automatically escalates prolonged symptoms to hospital care

### 🔁 Follow-Up Monitoring

* Bot checks back after **1 hour**
* Patient responses:

  * **“சரி / OK”** → case closed
  * **“சரி இல்லை / Not OK”** → hospital advice reinforced

### 🔔 Supervisor Escalation

* Emergency cases are:

  * Logged into database
  * Immediately notified to a supervisor (manager)
* If no response after 1 hour:

  * Case is **automatically escalated again**

### 🗄️ Local Database Logging (SQLite)

Each interaction is logged with:

* Timestamp
* Symptom description
* Detected issue type
* Duration
* Advice category
* Follow-up response status

No personal identifiers are stored.

---

## 🔐 Privacy & Ethical Design

* ❌ No patient names, phone numbers, or addresses collected
* ❌ No cloud-based AI or external medical APIs used
* ❌ No diagnosis or medication recommendations
* ✅ Local rule-based logic only
* ✅ Minimal, anonymised data storage
* ✅ Human-in-the-loop escalation for emergencies

This design makes ASHA Sahayi **safer than typical AI chatbots** for healthcare use.

---

## 🛠️ Technology Stack

* **Python**
* **python-telegram-bot**
* **SQLite**
* **deep-translator** (for multilingual support)

---

## 📂 Project Structure

```
asha-sahayi/
│
├── bot.py              # Main Telegram bot
├── asha_sahayi.db      # SQLite database (auto-created)
├── view_logs.py        # Script to view database logs
├── README.md           # Project documentation
```

---

## ▶️ How to Run the Bot

### 1️⃣ Install dependencies

```bash
pip install python-telegram-bot==20.3 deep-translator
```

### 2️⃣ Configure `bot.py`

```python
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
MANAGER_CHAT_ID = 123456789  # placeholder for demo
```

### 3️⃣ Run

```bash
python bot.py
```

---

## 🧪 Sample Test Inputs

### Normal case

```
2 naal fever iruku
```

### Emergency case

```
blood vomit iruku
```

### Follow-up response

```
சரி
```

or

```
சரி இல்லை
```

---

## 📊 Viewing Logs

Run:

```bash
python view_logs.py
```

This prints all stored patient interactions from the SQLite database.

---

## 🚀 Future Enhancements

* Image-based symptom analysis (with strict safeguards)
* Supervisor dashboards
* Secure cloud deployment for institutional use
* Expansion to additional regional languages

---

## ⚖️ Ethical Note

ASHA Sahayi is designed as a **support system**, not a replacement for medical professionals.
All final decisions remain with **ASHA workers and healthcare authorities**.

---

## 📌 Project Status

✅ Prototype complete
✅ Evaluation-ready
✅ Privacy-first
✅ Ethical AI compliant

---

## 👩‍⚕️ Built for Healthcare Heroes

ASHA Sahayi aims to empower ASHA workers with **safe, responsible, and practical technology** that respects their role, protects privacy, and improves community healthcare outcomes.



## SAMPLE OUTPUT
## 📸 Screenshots

### Bot Introduction
<img width="469" height="224" alt="image" src="https://github.com/user-attachments/assets/39a11686-71cb-4ba4-b563-5c523a2bcb98" />


### Normal Symptom Handling
<img width="466" height="239" alt="image" src="https://github.com/user-attachments/assets/f3e1d706-6974-47f3-867f-6c02a700106f" />


### Emergency Detection
<img width="472" height="339" alt="image" src="https://github.com/user-attachments/assets/be5eecfe-99e0-401f-9a1a-a0b450722084" />


### LOGS
<img width="1395" height="187" alt="image" src="https://github.com/user-attachments/assets/8004b586-b18e-4fa7-a619-10ff97a8f399" />

