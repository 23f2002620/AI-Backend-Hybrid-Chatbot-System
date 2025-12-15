# AI-Backend-Hybrid-Chatbot-System

**Status:** Production-ready  
**Architecture:** Hybrid AI + Deterministic Moderation  
**Backend:** FastAPI (Python)

---

## 📌 Overview

This backend powers **two AI chatbots** for a dating application:

1. **User-Side Chatbot (Hybrid AI)**
2. **Admin-Side Chatbot (Rule-Based + Semantic Retrieval)**

The system is designed for **safety, explainability, and scalability**, which are critical for dating platforms.

---

## 🤖 Chatbot Types

### 1️⃣ User Bot (Hybrid)

Used by app users for:
- Onboarding assistance
- Feature explanations (Boost, Superlike, etc.)
- Safety guidance
- Friendly conversation support

**Approach**
- Rule-based safety checks
- FAQ lookup
- Semantic vector retrieval (RAG)
- LLM generation (OpenAI → Gemini fallback)

---

### 2️⃣ Admin Bot (Deterministic)

Used by moderators/admins for:
- Reviewing reported users
- Understanding moderation policies
- Getting contextual policy guidance

**Approach**
- Strict rule-based decisions
- Semantic retrieval over admin policies
- No free-form LLM decisions (to avoid hallucinations)

---

## 🧱 Architecture
Client (User App / Admin Panel)
|
v
FastAPI Backend
|
├── User Bot (Hybrid)
│ ├── Safety Rules
│ ├── FAQ Retrieval
│ ├── Vector Search (RAG)
│ └── LLM (OpenAI → Gemini)
|
└── Admin Bot
├── Rule Engine
└── Vector Search (Policies)


---

## 🛠️ Technology Stack

| Layer | Technology |
|-----|-----------|
Backend | FastAPI |
Language | Python 3.11+ |
ORM | SQLAlchemy |
Database | SQLite (dev) / PostgreSQL (prod) |
Vector DB | FAISS (local) |
Embeddings | OpenAI / Sentence-Transformers |
LLM | OpenAI (primary), Gemini (fallback) |
OS | Windows / Linux |

---

## 📁 Project Structure

project-root/
│
├── app/
│ ├── main.py
│ ├── config.py
│ ├── database.py
│ ├── models.py
│
│ ├── llm/
│ │ ├── openai_client.py
│ │ ├── gemini_client.py
│ │ └── llm_router.py
│
│ ├── retrieval/
│ │ ├── embeddings.py
│ │ ├── vector_store.py
│ │ └── store_and_query.py
│
│ ├── user_bot/
│ │ ├── hybrid.py
│ │ ├── intent.py
│ │ ├── moderation.py
│ │ └── router.py
│
│ └── admin_bot/
│ |├── rules.py
│ |├── retrieval.py
│ |├── admin.py
│ |└── router.py
│
├── scripts/
│ ├── index_admin_policies.py
│ └── index_faq_and_recent.py
│
├── tests/
│ ├── user.json
│ └── admin.json
│
└── venv/


---

## 🗄️ Database Design

### Core Tables

| Table | Purpose |
|-----|--------|
users | Application users |
profiles | Dating profiles |
trust_scores | Safety scoring |
reports | User reports |
bot_sessions | Chat sessions |
bot_messages | Chat history |
admin_actions | Admin decisions |
embeddings_meta | Vector-indexed text |

> ⚠️ SQLAlchemy reserved names are avoided (e.g., `metadata` is **not** used).

---

## 🧠 Vector Retrieval (RAG)

### Purpose
Semantic search over:
- FAQs
- Admin policies
- Recent conversations

### Flow
Text → Embedding → Vector Index → Similarity Search → Context

### Backend
- FAISS (local / dev)
- Replaceable with Pinecone, Milvus, Qdrant

---

## 👤 User Bot – Execution Flow

1. Save user message
2. Safety rule check
3. Intent detection
4. Exact FAQ lookup
5. Semantic vector retrieval
6. LLM response generation
7. Save bot reply

### LLM Failover
OpenAI → (error/quota) → Gemini

---

## 🛡️ Admin Bot – Execution Flow

### Rule Engine
- Deterministic
- Explainable
- Robust key handling

**Rules**
- `reports >= 3` → `CRITICAL_REVIEW`
- `trust < 40` → `ESCALATE`

### Semantic Retrieval
- Admin policies indexed in vector DB
- Deduplication + confidence threshold applied

---

## 🧹 Deduplication & Confidence Filtering

- Duplicate semantic results removed
- Low-confidence matches filtered (`score < 0.45`)
- Ensures clean, relevant admin output

---

## 📦 Indexing (Required Before Launch)

Vector DB starts **empty**.

### Run once from project root:
```bash
python -m scripts.index_admin_policies
python -m scripts.index_faq_and_recent
```
❗ Always use python -m, not python file.py

---
###🌐 API Endpoints
User Chat
```bash
POST /user/chat
```
Request
```json
{
  "user_id": 1,
  "message": "How does boost work?"
}
```
Response
```json
{
  "reply": "Boost increases visibility for 30 minutes.",
  "intent": "chat"
}
```
---
Admin Chat
```bash
POST /admin/chat
```
Request
```json
{
  "query": "harassment",
  "user": {
    "reports": 4,
    "trust": 30
  }
}
```
Response
```josn
{
  "actions": ["CRITICAL_REVIEW", "ESCALATE"],
  "reasons": [
    "User has 4 reports (>=3)",
    "Trust score is 30 (<40)"
  ],
  "signals": {
    "reports": 4,
    "trust": 30
  },
  "knowledge": [
    {
      "score": 0.58,
      "text": "Harassment cases must be reviewed within 2 hours."
    }
  ]
}
```
---
###🧪 Testing on Windows

PowerShell does not support curl flags.
Use:
```powershell
Invoke-RestMethod ... | ConvertTo-Json -Depth 6
```
---
**🔐 Security Considerations
**
No sensitive user data sent to LLMs
Admin decisions are explainable and auditable
Deterministic moderation rules
Embeddings store only short text snippets

---

**✅ Launch Checklist**

 User hybrid chatbot
 Admin deterministic chatbot
 Vector retrieval
 Deduplication
 LLM failover
 Persistent storage
 Indexing completed
 Windows-tested

---

