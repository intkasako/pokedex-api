# Pokedex API

A REST API for querying and managing Pokémon data, built with **FastAPI** and **SQLite** using raw SQL queries.

## Overview

This project is a simple Pokédex that exposes a RESTful API with full CRUD operations. The database stores Pokémon with their types and generation info, linked through foreign keys. All SQL is written by hand — no ORM involved.

### Features

- Full CRUD — create, read, update and delete Pokémon
- Filter by type, generation, or both
- Two related tables with foreign key constraints
- JOIN queries to resolve type names from IDs
- Case-insensitive type input (e.g. `fire`, `FIRE` and `Fire` all work)
- Auto-generated interactive docs via Swagger UI

## Tech Stack

| Layer     | Technology          |
|-----------|---------------------|
| Framework | FastAPI             |
| Database  | SQLite3 (raw SQL)   |
| Validation| Pydantic            |
| Server    | Uvicorn             |
| Language  | Python 3.10+        |

## Getting Started

### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/intkasako/pokedex-api.git
   cd pokedex-api
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn
   ```

3. Initialize the database:
   ```bash
   python database.py
   ```

4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## API Endpoints

### List all Pokémon

```
GET /pokemon
```

Supports optional query parameters for filtering:

| Parameter    | Type   | Description             |
|--------------|--------|-------------------------|
| `type`       | string | Filter by type name     |
| `generation` | int    | Filter by generation    |

**Examples:**

```
GET /pokemon?type=Fire
GET /pokemon?generation=1
GET /pokemon?type=Water&generation=3
```

### Get a Pokémon by ID

```
GET /pokemon/{id}
```

### Create a Pokémon

```
POST /pokemon
```

```json
{
  "name_": "Pikachu",
  "type_primary": "Electric",
  "type_secondary": null,
  "generation": 1
}
```

### Update a Pokémon

```
PUT /pokemon/{id}
```

Same body format as `POST`.

### Delete a Pokémon

```
DELETE /pokemon/{id}
```

## Project Structure

```
pokedex-api/
├── main.py        # FastAPI app with all endpoints
├── database.py    # Database connection and initialization
├── schema.sql     # Table definitions (types + pokemon)
├── seed.sql       # Initial data (18 types, 32 Pokémon)
└── .gitignore
```

## Database Schema

The database uses two tables linked by foreign keys:

```
types                       pokemon
┌──────────┬──────────┐     ┌─────────────────┬──────────────────┐
│ type_id  │ name_    │     │ pokemon_id      │ name_            │
│ (PK)     │          │◄────│ type_primary_id  │ type_secondary_id│
│          │          │     │ (FK)             │ (FK, nullable)   │
│          │          │     │                  │ generation       │
└──────────┴──────────┘     └─────────────────┴──────────────────┘
```

> [!NOTE]
> The database ships pre-seeded with all 18 official Pokémon types and 32 Pokémon spanning generations 1 through 6.
