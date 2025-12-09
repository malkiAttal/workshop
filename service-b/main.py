
from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone

app = FastAPI()

@app.post("/sum")
def sum_numbers(payload: dict):
    nums = payload.get("numbers")
    if not isinstance(nums, list):
        raise HTTPException(status_code=400, detail="numbers must be list")
    try:
        total = float(sum(nums))
    except:
        raise HTTPException(status_code=400, detail="invalid numbers")
    return {
        "total": total,
        "count": len(nums),
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0"
    }
