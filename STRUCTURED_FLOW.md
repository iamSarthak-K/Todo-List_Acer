# AI Productivity Assistant - Structured Flow

## 🛠️ Tools & Technologies Used
### Backend
- **Framework**: FastAPI (Python)
- **Database ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Database**: SQLite (local: `dev.db`), Supabase (remote capability)
- **Background Jobs**: Celery + Redis
- **AI Integration**: Google GenAI SDK (`gemini-3.5-flash`), LangGraph
- **Other**: Uvicorn (server), Loguru (logging), python-jose (JWT)

### Frontend
- **Framework**: React (Vite)
- **Routing**: React Router DOM (`v7`)
- **Charting**: Chart.js (`react-chartjs-2`)
- **Icons**: Lucide React
- **Styling**: Standard CSS (`index.css`, `App.css`)

---

## 🏗️ Architecture & File Connections

### 1. Frontend Flow
**Entry Point**: `index.html` → `src/main.jsx` → `src/App.jsx`

*   **`src/App.jsx`**
    *   **Role**: Main Application Router & Authentication Guard.
    *   **Connections**:
        *   Checks auth via `src/services/api.js` (`getToken`, `getMe`).
        *   Renders `Login.jsx` if unauthenticated.
        *   Wraps authenticated routes in `src/components/Layout.jsx`.
        *   Routes to Pages: `Dashboard.jsx`, `Commitments.jsx`, `Focus.jsx`, `Analytics.jsx`.

*   **Pages (`src/pages/`)**
    *   **`Dashboard.jsx`**: Main overview.
    *   **`Commitments.jsx`**: Manage high-level goals.
    *   **`Focus.jsx`**: Deep work sessions.
    *   **`Analytics.jsx`**: Data visualization.
    *   **`Login.jsx`**: Authentication handling.

### 2. Backend Flow
**Entry Point**: `backend/app/main.py`

*   **`backend/app/main.py`**
    *   **Role**: FastAPI App instantiation, CORS configuration, DB initialization (`Base.metadata.create_all`), and Router wiring.
    *   **Connects to Routers**:
        *   `/api/auth` → `routers/auth.py`
        *   `/api/commitments` → `routers/commitments.py`
        *   `/api/tasks` → `routers/tasks.py`
        *   `/api/focus` → `routers/focus.py`
        *   `/api/reminders` → `routers/reminders.py`
        *   `/api/analytics` → `routers/analytics.py`
        *   `/api/ai` → `routers/ai.py` (New centralized AI Gateway)

*   **Routers (`backend/app/routers/`)**
    *   Handle HTTP requests and map them to Database operations and Services.
    *   **Example (`ai.py`)**:
        *   `POST /api/ai/plan` → Calls `ContextService`, routes to `LangGraph`, invokes `PlannerAgent`, returns structured subtasks.

*   **Services (`backend/app/services/`)**
    *   **`llm_client.py` & `gemini_client.py`**: Interacts with Google GenAI API for model generation.
    *   **`context_service.py` & `memory_service.py`**: Retrieve state data for AI context without agents touching DB.
    *   **`parser.py`**: Validates LLM outputs against Pydantic schemas.
    *   **`focus_service.py`**: Manages focus session logic.
    *   **`graph_service.py`**, **`intervention_engine.py`**, **`priority_engine.py`**, **`risk_engine.py`**, **`root_cause_engine.py`**: Business logic engines for productivity analysis.

*   **AI Graph & Agents (`backend/app/ai/`)**
    *   **`prompts/`**: Markdown files for system instructions (`commitment.md`, `planner.md`, etc.).
    *   **`agents/`**: Isolated AI responsibilities (`commitment_agent.py`, `planner_agent.py`, etc.).
    *   **`graph/`**: LangGraph orchestration (`graph.py`, `nodes.py`, `router.py`, `state.py`).

*   **Models (`backend/app/models/`)**
    *   **`user.py`**: User table.
    *   **`commitment.py`**: Main goals/commitments table.
    *   **`task.py`**: Subtasks linked to commitments.
    *   **`focus_session.py`**: Tracking deep work blocks.
    *   **`reminder.py`**: Notification scheduling.

### 3. Testing & Tooling
*   **`backend/test_ai_endpoints.py`**: Standalone testing script that handles demo authentication and sequentially tests the LangGraph-powered AI endpoints (`/api/ai/extract`, `plan`, `recover`, `chat`) to ensure models and context parsing are working properly.

---

## 🔄 How Request Data Flows (Example: Task Completion)

1. **User Action**: Clicks "Complete" on a task in the React frontend (`Dashboard.jsx` or `Commitments.jsx`).
2. **API Call**: Frontend sends `PATCH /api/tasks/{task_id}/done` via `src/services/api.js`.
3. **Backend Routing**: `main.py` directs the request to `routers/tasks.py`.
4. **Auth Check**: `routers/tasks.py` verifies user identity via `app.routers.deps.get_current_user`.
5. **Database Update**: SQLAlchemy queries `app.models.task.Task` and updates `is_done = True` in SQLite (`dev.db`).
6. **Response**: Backend returns `{"message": "Task completed"}`.
7. **UI Update**: Frontend updates the local state to show the task as checked.

---

*Note: This file should be updated whenever new tools are added, new architectural patterns are introduced, or major files are refactored.*
