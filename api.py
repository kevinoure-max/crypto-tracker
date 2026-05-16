from fastapi import FastAPI, HTTPException
from database import init_db, get_snapshots
from tracker import get_history, compute_summary

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/coins/{coin}")
def get_coin(coin: str, days: int = 7):
    if days <= 0:
        raise HTTPException(status_code=400, detail="--days must be greater than 0")
    prices = get_history(coin, days)
    if prices is None:
        raise HTTPException(status_code=404, detail=f"coin '{coin}' not found")
    summary = compute_summary(prices)
    summary["coin"] = coin
    summary["days"] = days
    return summary


@app.get("/history")
def get_history_endpoint():
    rows = get_snapshots()
    result = []
    for (
        id,
        coin,
        days,
        current_price,
        high,
        low,
        change_pct,
        avg_price,
        created_at,
    ) in rows:
        result.append(
            {
                "id": id,
                "coin": coin,
                "days": days,
                "current_price": current_price,
                "high": high,
                "low": low,
                "change_pct": change_pct,
                "avg_price": avg_price,
                "created_at": created_at,
            }
        )
    return result
