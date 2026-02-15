from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

# CORS supaya frontend bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# koneksi postgres
conn = psycopg2.connect(
    dbname="drug_db",
    user="postgres",
    password="lurimamirdas",  # ganti sesuai password kamu
    host="localhost",
    port="5432"
)

@app.get("/")
def home():
    return {"message": "Drug Interaction API Ready"}

@app.get("/check")
def check_interaction(name: str, interact: str):
    cur = conn.cursor()

    query = """
    SELECT interaction_description, severity, recommendation
    FROM drug_interactions
    WHERE LOWER(name)=LOWER(%s)
    AND LOWER(interact_with)=LOWER(%s)
    LIMIT 1;
    """

    cur.execute(query, (name, interact))
    result = cur.fetchone()
    cur.close()

    if result:
        return {
            "interaction_description": result[0],
            "severity": result[1],
            "recommendation": result[2]
        }
    else:
        return {"message": "No interaction found"}

@app.get("/search_drug")
def search_drug(q: str):
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT name
        FROM drug_interactions
        WHERE name ILIKE %s
        LIMIT 15;
    """, (f"%{q}%",))

    results = cur.fetchall()
    cur.close()

    return [r[0] for r in results]

@app.get("/search_interact")
def search_interact(q: str):
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT interact_with
        FROM drug_interactions
        WHERE interact_with ILIKE %s
        LIMIT 15;
    """, (f"%{q}%",))

    results = cur.fetchall()
    cur.close()

    return [r[0] for r in results]

@app.get("/interactions_by_drug")
def interactions_by_drug(drug: str, q: str = ""):
    cur = conn.cursor()

    if q:
        cur.execute("""
            SELECT DISTINCT interact_with
            FROM drug_interactions
            WHERE LOWER(name)=LOWER(%s)
            AND interact_with ILIKE %s
            LIMIT 20;
        """, (drug, f"%{q}%"))
    else:
        cur.execute("""
            SELECT DISTINCT interact_with
            FROM drug_interactions
            WHERE LOWER(name)=LOWER(%s)
            LIMIT 20;
        """, (drug,))

    results = cur.fetchall()
    cur.close()

    return [r[0] for r in results]

@app.get("/all_drugs")
def all_drugs():
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT name
        FROM drug_interactions
        ORDER BY name ASC;
    """)

    results = cur.fetchall()
    cur.close()

    return [r[0] for r in results]
