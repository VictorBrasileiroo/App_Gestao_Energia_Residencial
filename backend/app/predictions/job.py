from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from ..models import ConsumptionDaily, TariffPlan, Prediction

def generate_prediction_for_user(db: Session, user_id: int):
    # previsao simples de consumo para o proximo mes
    # usa a media dos ultimos 90 dias e multiplica por 30; tambem gera um intervalo de confianca

    today = date.today()

    first_day_next_month = today.replace(day=1) + timedelta(days=32)
    target_month = first_day_next_month.replace(day=1).strftime("%Y-%m")

    cutoff = today - timedelta(days=90)
    data = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= cutoff
    ).all()

    if not data:
        print(f"[INFO] Usuário {user_id} não possui dados suficientes para previsão.")
        return None

    avg_kwh = sum(r.energy_kwh for r in data) / len(data)

    tariff = db.query(TariffPlan).filter_by(user_id=user_id).first()
    price = tariff.price_per_kwh if tariff else 1.0  # fallback para 1.0 se não tiver plano

    predicted_energy = avg_kwh * 30
    cost_pred = predicted_energy * price

    # Cria a previsão
    pred = Prediction(
        user_id=user_id,
        target_month=target_month,
        energy_kwh_pred=predicted_energy,
        cost_pred=cost_pred,
        confidence_low_kwh=predicted_energy * 0.95,
        confidence_high_kwh=predicted_energy * 1.05,
        generated_at=datetime.utcnow()
    )

    db.add(pred)
    db.commit()
    db.refresh(pred)

    print(f"[INFO] Previsão gerada para usuário {user_id} para o mês {target_month}")
    return pred
