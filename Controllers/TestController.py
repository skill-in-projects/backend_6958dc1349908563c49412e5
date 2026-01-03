from fastapi import APIRouter, HTTPException
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Models.TestProjects import TestProjects
from psycopg import connect
from psycopg.rows import dict_row

router = APIRouter(prefix="/api/test", tags=["test"])

def get_db_connection():
    connection_string = os.getenv("DATABASE_URL")
    if not connection_string:
        raise ValueError("DATABASE_URL environment variable not set")
    try:
        return connect(connection_string, row_factory=dict_row)
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

@router.get("/")
async def get_all():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT "Id", "Name" FROM "TestProjects" ORDER BY "Id"')
            results = cur.fetchall()
            return results
    finally:
        conn.close()

@router.get("/{id}")
async def get(id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT "Id", "Name" FROM "TestProjects" WHERE "Id" = %s', (id,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Project not found")
            return result
    finally:
        conn.close()

@router.post("/")
async def create(project: TestProjects):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO "TestProjects" ("Name") VALUES (%s) RETURNING "Id"', (project.name,))
            project_id = cur.fetchone()["Id"]
            conn.commit()
            project.id = project_id
            return project
    finally:
        conn.close()

@router.put("/{id}")
async def update(id: int, project: TestProjects):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('UPDATE "TestProjects" SET "Name" = %s WHERE "Id" = %s', (project.name, id))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Project not found")
            conn.commit()
            return {{"message": "Updated successfully"}}
    finally:
        conn.close()

@router.delete("/{id}")
async def delete(id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM "TestProjects" WHERE "Id" = %s', (id,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Project not found")
            conn.commit()
            return {{"message": "Deleted successfully"}}
    finally:
        conn.close()
