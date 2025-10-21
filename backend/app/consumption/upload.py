import pandas as pd
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from .. import models

def process_csv(user_id: int, file: UploadFile, db: Session):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao ler o arquivo CSV")
    
    if not {"datetime", "energy_kwh"}.issubset(df.columns):
        raise HTTPException(status_code=422, detail="Formato de CSV inválido")
    
    # conversao e validacao
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    if df["datetime"].isna().any():
        raise HTTPException(status_code=422, detail="Datas inválidas")
    
    # inserir o consumo por hora
    hourly = [
        models.ConsumptionHourly(
            user_id=user_id,
            datetime=row["datetime"],
            energy_kwh=row["energy_kwh"]
        )
        for _, row in df.iterrows()
    ]

    db.bulk_save_objects(hourly)

    # agregar o consumo diario
    df["date"] = df["datetime"].dt.date
    daily_df = df.groupby("date")["energy_kwh"].sum().reset_index()

    daily = [
        models.ConsumptionDaily(
            user_id=user_id,
            date=row["date"],
            energy_kwh=row["energy_kwh"]
        )
        for _, row in daily_df.iterrows()
    ]

    db.bulk_save_objects(daily)
    db.commit()

    return {"status": "success", "records_created": {"hourly": len(hourly), "daily": len(daily)}}
    