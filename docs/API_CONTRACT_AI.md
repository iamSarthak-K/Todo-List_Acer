# AI Layer API Contract

This document outlines the API endpoints provided by the AI layer, replacing the direct LLM interactions.

## 1. Extract Commitment (`POST /api/ai/extract`)
Extracts structured commitment details from unstructured text.

**Request:**
```json
{
  "text": "Meeting with John on Tuesday to discuss Q3 roadmap."
}
```

**Response (200 OK):**
```json
{
  "title": "Meeting with John",
  "category": "Meeting",
  "due_date": "2026-07-02",
  "priority": "High"
}
```

---

## 2. Plan Tasks (`POST /api/ai/plan`)
Breaks down a commitment into actionable subtasks.

**Request:**
```json
{
  "commitment_id": 5
}
```

**Response (200 OK):**
```json
{
  "tasks": [
    "Draft Q3 roadmap outline",
    "Review previous quarter metrics",
    "Prepare presentation slides"
  ]
}
```

---

## 3. Generate Reminder (`POST /api/ai/reminder`)
Generates a motivational reminder message for a specific task based on user history.

**Request:**
```json
{
  "task_id": 10
}
```

**Response (200 OK):**
```json
{
  "reminder": "You've been making great progress this week! Completing this draft now will give you peace of mind for the weekend."
}
```

---

## 4. Recovery Plan (`POST /api/ai/recover`)
Creates a catch-up plan for missed or overdue tasks.

**Request:**
```json
{
  "task_id": 10
}
```

**Response (200 OK):**
```json
{
  "plan": [
    "Work 30 minutes on the draft today",
    "Reschedule the review meeting to tomorrow"
  ]
}
```

---

## 5. Chat Assistant (`POST /api/ai/chat`)
Handles general user messages and provides context-aware productivity advice.

**Request:**
```json
{
  "message": "I feel overwhelmed with my tasks today."
}
```

**Response (200 OK):**
```json
{
  "reply": "It's okay to feel overwhelmed. Let's look at your high-priority tasks first. Would you like me to help you prioritize your day?"
}
```

---

## Error Codes
- **400 Bad Request:** Missing fields, invalid input format.
- **401 Unauthorized:** Missing or invalid Bearer token.
- **404 Not Found:** `commitment_id` or `task_id` does not exist or doesn't belong to the user.
- **500 Internal Server Error:** LLM service failure, parse error, or LangGraph failure.
