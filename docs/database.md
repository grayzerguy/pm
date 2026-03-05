# Database Schema for Kanban Board

## Overview
For the MVP, we use SQLite as the local database to persist the Kanban board data. Each user has one board, stored as JSON.

## Schema
**Table: boards**
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `user_id`: TEXT NOT NULL (for future multi-user support; currently always 'user')
- `data`: TEXT NOT NULL (JSON string containing the BoardData)

## BoardData JSON Structure
```json
{
  "columns": [
    {
      "id": "string",
      "title": "string",
      "cardIds": ["string", ...]
    },
    ...
  ],
  "cards": {
    "card_id": {
      "id": "string",
      "title": "string",
      "details": "string"
    },
    ...
  }
}
```

## Approach
- On app start, if no board exists for the user, create one with initial data.
- API endpoints will load/save the JSON data.
- Use SQLAlchemy or raw SQL for simplicity (keep dependencies light).

## Future Considerations
- Add timestamps for created/updated.
- Support multiple boards per user.
- Migrate to relational schema if needed.