# InsightFlow AI

InsightFlow AI is a multi-agent data analysis assistant. Upload CSV/Excel datasets and PDF/Word/text documents into a workspace, then chat with an AI pipeline that cleans your data, analyzes it, retrieves relevant  document context, generates charts, and returns a grounded natural-language answer.

## How it works

Each chat message runs through a pipeline of cooperating agents ([backend/app/agents](backend/app/agents)):

```
Planner Agent
     │
     ├──► CSV Analysis Agent  ─┐
     │                         ├──► Knowledge Fusion Agent ──► Insight Agent ──► Answer
     └──► RAG Agent (docs)   ──┘
              │
              └──► Visualization Agent (chart, if requested)
```

- **Planner Agent** — decides which files are relevant, whether a chart is needed, and the query type.
- **Preprocessing Agent / Service** — cleans uploaded CSV/Excel files (encoding detection, dtype conversion, missing values, outliers, deduplication) before analysis.
- **CSV Analysis Agent** — runs pandas-based statistical analysis over the cleaned datasets.
- **RAG Agent** — retrieves relevant chunks from uploaded documents using FAISS + sentence-transformer embeddings.
- **Visualization Agent** — builds a Plotly chart when the question calls for one.
- **Knowledge Fusion Agent** — merges structured (CSV) and unstructured (RAG) findings into one context.
- **Insight Agent** — calls Gemini to produce the final natural-language answer.
- **Report Agent** — assembles workspace findings into an exportable PDF report.

## Tech stack

| Layer      | Technology |
|------------|------------|
| Backend    | FastAPI, Motor (async MongoDB), Pandas, LangChain, FAISS, sentence-transformers, Plotly, ReportLab |
| LLM        | Google Gemini (`google-genai`) |
| Database   | MongoDB (Atlas or local) |
| Frontend   | React 18, Vite, Tailwind CSS, Zustand, React Router, Plotly.js |

## Prerequisites

- Python 3.11+
- Node.js 18+
- A MongoDB connection string (local instance or MongoDB Atlas)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Installation

### 1. Clone and configure environment variables

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and set your own values — **do not reuse the example file's committed credentials**, they are for local demo purposes only:

```env
MONGODB_URL=mongodb://localhost:27017        # or your Atlas connection string
MONGODB_DB_NAME=insightflow
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 3. Frontend setup

```bash
cd frontend
npm install
```

## Running the app

Run backend and frontend in two separate terminals.

**Backend** (from `backend/`):

```bash
python run.py
```

Starts the API at `http://localhost:8000`. Interactive API docs are available at `http://localhost:8000/docs`. First run downloads the `all-MiniLM-L6-v2` embedding model (~90 MB).

**Frontend** (from `frontend/`):

```bash
npm run dev
```

Starts the Vite dev server at `http://localhost:5173`.

Open `http://localhost:5173` in your browser to use the app.

## Project structure

```
backend/
  app/
    agents/        # Planner, CSV analysis, RAG, visualization, insight, report agents
    api/v1/         # FastAPI routers (workspaces, upload, chat, datasets, documents, charts, reports)
    core/           # DB connection, storage paths, embeddings, vector store
    models/         # Domain models
    repositories/   # MongoDB data-access layer
    services/       # Business logic orchestrating repositories + agents
    schemas/        # Pydantic request/response schemas
  storage/          # Uploaded files, cleaned datasets, FAISS indexes, charts, reports
  run.py            # Entrypoint (uvicorn)

frontend/
  src/
    components/     # Layout, chat, upload, chart, workspace UI components
    pages/           # Home, Workspace, NotFound
    hooks/           # useWorkspace, useChat, useUpload
    services/        # API clients
```

## Notes

- Uploaded datasets are never modified in place — preprocessing writes a cleaned copy to `storage/uploads/cleaned/`, keeping the original untouched.
- Files with a `.xls` extension that are actually plain CSV/HTML exports (common with government/public datasets) are auto-detected and parsed as CSV rather than failing on the Excel engine.
