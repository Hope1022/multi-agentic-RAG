# Multi-Agent RAG Study Assistant

A professional, safety-aware academic study assistant built with **LangGraph**, **LangChain**, **LangSmith**, FastAPI, and Next.js. The system combines structured student performance data, course-document retrieval, and web search to produce a grounded, personalized study response.

## Highlights

- **Multi-agent orchestration:** A supervisor delegates work to four specialist agents and synthesizes their reports.
- **Retrieval-augmented generation:** Curriculum agents retrieve relevant chunks from course PDFs stored in a persistent Chroma vector database.
- **Student-aware analysis:** The performance agent reads scores and attendance from PostgreSQL through `asyncpg`.
- **Web-grounded resources:** Resource and study-plan agents use Google Serper to find current learning materials and study strategies.
- **LLM fallback routing:** Groq, Google Gemini, and Cohere models are configured with provider fallbacks.
- **Prompt-injection and safety controls:** A heuristic detector and Llama Prompt Guard run before the agent graph. A Guardrails ToxicLanguage validator is also included for optional activation.
- **Tracing and debugging:** LangSmith tracing is configured for inspecting runs, agent transitions, prompts, outputs, and latency.
- **API and chat UI:** FastAPI exposes the backend and a Next.js frontend provides a simple chat interface.

## Architecture

```mermaid
flowchart TD
    UI[Next.js chat UI] --> API[FastAPI POST /chat]
    API --> ENTRY[main.run]
    ENTRY --> H[Heuristic input check]
    H -->|safe| LG[Llama Prompt Guard]
    H -->|unsafe| STOP[Reject request]
    LG -->|safe| S[Supervisor]
    LG -->|unsafe| STOP
    S --> P[Performance agent]
    S --> C[Curriculum RAG agent]
    S --> R[Resource web-search agent]
    S --> SP[Study-plan web-search agent]
    P --> SYN[Synthesis checkpoint]
    C --> SYN
    R --> SYN
    SP --> SYN
    SYN --> S
    S --> OUT[Personalized final answer]

    P --> DB[(PostgreSQL)]
    C --> VDB[(Chroma vector store)]
    C --> PDF[Course PDFs]
    R --> WEB[Google Serper]
    SP --> WEB
    ENTRY -. traces .-> LS[LangSmith]
```

### Agent responsibilities

| Component | Responsibility | Data source |
| --- | --- | --- |
| Supervisor | Creates specialist instructions, then combines the reports into a concise answer | All agent outputs |
| Performance agent | Identifies score trends, weak topics, and attendance impact | PostgreSQL |
| Curriculum agent | Finds priorities, topics to focus on, and exam guidance | Chroma retrieval over PDFs |
| Resource agent | Recommends specific learning resources | Google Serper web search |
| Study-plan agent | Produces a three-week plan and expected outcome | Student context plus web search |
| Heuristic guard | Blocks common prompt-injection phrases | User input |
| Llama Guard | Performs model-based prompt-injection screening | User input |
| Guardrails validator | Optional toxicity validation | User input |
| Judge agent | Optional grounding and quality-control pass | Draft and source reports |

## RAG and project resources

The curriculum corpus is represented by the PDFs in `resources/pdf's/`:

- `math101_syllabus.pdf`
- `math101_study_guide.pdf`
- `math101_past_exam.pdf`

`ingest.py` loads these documents with `PyPDFLoader`, splits them with `RecursiveCharacterTextSplitter`, creates `nomic-embed-text` embeddings through Ollama, and persists the `odyssey` collection in Chroma. The curriculum agent retrieves up to five relevant chunks using similarity-score filtering before asking the LLM to analyze them.

The project also includes a PostgreSQL schema and seed data in `database.py`. It models users, courses, enrollments, assessments, scores, and attendance. The performance agent uses this structured data to ground its analysis in measurable academic results.

> **Storage path note:** `ingest.py` currently writes to `db/chroma_db`, while the curriculum agent reads from `resources/db/chroma_db`. Keep these paths aligned before rebuilding the vector store, or move the generated store to the path used by the curriculum agent.

## Safety and quality controls

Input processing begins with a deterministic heuristic detector and then calls the Groq-hosted `meta-llama/llama-prompt-guard-2-86m` model. Unsafe input terminates the graph with a rejection message.

`guardrails.py` contains a `Guardrails AI` `ToxicLanguage` validator backed by a Hugging Face model. The node is available for activation in the graph, but it is not currently connected in `graph/graph.py`.

The LLM-as-a-judge implementation in `agents/judge.py` checks grounding, hallucination, relevance, and tone. Its graph edges are currently commented out, so it should be treated as an optional quality-control extension rather than an active runtime stage.

## Project structure

```text
.
├── agents/                 Specialist agents and supervisor
├── backend/                FastAPI application and request schema
├── frontend/               Next.js chat application
├── graph/                  LangGraph state graph and synthesis checkpoint
├── resources/              Persistent Chroma data and PDF resources
├── safety/input/           Heuristic, Guardrails, and Llama Guard checks
├── database.py             PostgreSQL schema and seed data
├── ingest.py               PDF ingestion and vector-store creation
├── llm.py                  LLM providers and fallback configuration
├── main.py                 Application entry point
└── requirements.txt        Python dependencies
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL database
- Ollama with the `nomic-embed-text` model
- API keys for the configured providers and Google Serper
- A LangSmith account for tracing and debugging

Install the embedding model locally:

```bash
ollama pull nomic-embed-text
```

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Install the frontend dependencies:

```powershell
cd frontend
npm install
cd ..
```

Create a `.env` file in the project root. The application currently reads these variables:

```env
groq_api_key=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
SERPER_API_KEY=your_serper_api_key
DB_URL=postgresql://user:password@localhost:5432/database
CURRENT_STUDENT_ID=1
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=multi-agentic-rag
```

Never commit `.env` or provider credentials.

## Prepare data

Initialize the PostgreSQL schema and seed data using the async helpers in `database.py` from your own application or an async setup script. Then build the document index:

```powershell
python ingest.py
```

Verify that the Chroma output path matches the path configured in `agents/curriculum.py` before starting the application.

## Run the application

Start the FastAPI backend from the project root:

```powershell
uvicorn backend.backend:app --reload --port 8000
```

In a second terminal, start the Next.js frontend:

```powershell
cd frontend
npm run dev
```

Open `http://localhost:3000` and send a study question. The frontend sends requests to `http://127.0.0.1:8000/chat`.

You can also call the API directly:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"I am struggling with integration. How should I prepare for my exam?\"}"
```

## Observability with LangSmith

Set `LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, and `LANGSMITH_PROJECT` to capture LangChain and LangGraph activity. LangSmith can then be used to inspect execution traces, compare model behavior, identify failed or slow nodes, and debug prompts and intermediate agent outputs.

## Current implementation notes

- The API currently uses `CURRENT_STUDENT_ID` for every request; per-request student authentication is not implemented.
- `main.run()` returns the supervisor draft answer. The optional judge and retry path is defined but disabled in the graph.
- The backend CORS policy currently allows local frontend origins on ports 3000.
- External LLM, web-search, PostgreSQL, and Ollama services must be available at runtime.

## License

No license has been specified for this project yet.
