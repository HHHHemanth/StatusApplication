from fastapi import FastAPI, WebSocket, Depends
from models import MachineData
from database.mongodb import machine_collection
from database.postgresql import SessionLocal, MachineStatus
from websocket.manager import manager

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ POST endpoint - add machine status
@app.post("/add_status")
async def add_machine_status(data: MachineData, db=Depends(get_db)):
    # Insert into MongoDB
    machine_collection.insert_one(data.dict())

    # Get last status from PostgreSQL for this machine
    last_status = (
        db.query(MachineStatus)
        .filter(MachineStatus.machine_id == data.machine_id)
        .order_by(MachineStatus.id.desc())
        .first()
    )

    # Compare status and insert if changed
    if not last_status or last_status.status != data.status:
        new_status = MachineStatus(
            machine_id=data.machine_id,
            machine_name=data.machine_name,
            status=data.status,
            time=data.time
        )
        db.add(new_status)
        db.commit()
        await manager.broadcast(f"Status Changed: {data.machine_id} → {data.status}")

    return {"message": "Inserted into MongoDB (and PostgreSQL if changed)"}

# ✅ GET endpoint - return all PostgreSQL status data
@app.get("/status_log")
def get_status_log(db=Depends(get_db)):
    records = db.query(MachineStatus).all()
    return records

# ✅ WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        manager.disconnect(websocket)
