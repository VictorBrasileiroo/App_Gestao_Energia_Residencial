from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from ..models import ConsumptionDaily, TariffPlan, Prediction
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def generate_prediction_for_user(db: Session, user_id: int):
    """
    Predição avançada usando ML com LinearRegression
    Considera tendências, sazonalidade (dia da semana) e padrões históricos
    """
    # Pegar a data mais recente disponível nos dados
    most_recent = db.query(ConsumptionDaily).filter_by(user_id=user_id).order_by(ConsumptionDaily.date.desc()).first()
    
    if not most_recent:
        print(f"[INFO] Usuário {user_id} não possui dados.")
        return None
    
    reference_date = most_recent.date

    # Calcular próximo mês baseado na data de referência
    first_day_next_month = reference_date.replace(day=1) + timedelta(days=32)
    target_month = first_day_next_month.replace(day=1).strftime("%Y-%m")

    # Pegar dados dos últimos 90 dias para treinar o modelo
    cutoff = reference_date - timedelta(days=90)
    data = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= cutoff,
        ConsumptionDaily.date <= reference_date
    ).order_by(ConsumptionDaily.date).all()

    if len(data) < 14:
        print(f"[INFO] Usuário {user_id} não possui dados suficientes para previsão (mínimo 14 dias).")
        return None

    # Preparar features avançadas para ML
    X_features = []
    y = []
    
    for record in data:
        day_index = (record.date - data[0].date).days
        day_of_week = record.date.weekday()  # 0=Monday, 6=Sunday
        day_of_month = record.date.day
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Criar features normalizadas
        features = [
            day_index,  # Tendência temporal
            day_of_week / 6.0,  # Dia da semana normalizado
            day_of_month / 31.0,  # Dia do mês normalizado
            is_weekend  # Binário para fim de semana
        ]
        
        X_features.append(features)
        y.append(record.energy_kwh)
    
    X = np.array(X_features)
    y = np.array(y)
    
    # Normalizar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Treinar modelo
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Fazer predições para os próximos 30 dias
    predictions = []
    last_day_index = (reference_date - data[0].date).days
    
    for i in range(1, 31):
        future_date = reference_date + timedelta(days=i)
        day_index = last_day_index + i
        day_of_week = future_date.weekday()
        day_of_month = future_date.day
        is_weekend = 1 if day_of_week >= 5 else 0
        
        X_future = np.array([[
            day_index,
            day_of_week / 6.0,
            day_of_month / 31.0,
            is_weekend
        ]])
        
        X_future_scaled = scaler.transform(X_future)
        pred_value = model.predict(X_future_scaled)[0]
        predictions.append(max(0, pred_value))  # Garantir não-negativo
    
    # Calcular estatísticas
    predicted_energy = float(np.sum(predictions))
    
    # Intervalo de confiança baseado no erro do modelo
    y_pred_train = model.predict(X_scaled)
    mse = np.mean((y - y_pred_train) ** 2)
    std_error = np.sqrt(mse) * np.sqrt(30)  # Erro padrão para 30 dias
    
    confidence_low = max(0, predicted_energy - 1.96 * std_error)
    confidence_high = predicted_energy + 1.96 * std_error

    tariff = db.query(TariffPlan).filter_by(user_id=user_id).first()
    price = tariff.price_per_kwh if tariff else 0.70

    cost_pred = predicted_energy * price

    # Cria a previsão
    pred = Prediction(
        user_id=user_id,
        target_month=target_month,
        energy_kwh_pred=round(predicted_energy, 2),
        cost_pred=round(cost_pred, 2),
        confidence_low_kwh=round(confidence_low, 2),
        confidence_high_kwh=round(confidence_high, 2),
        generated_at=datetime.utcnow()
    )

    db.add(pred)
    db.commit()
    db.refresh(pred)

    r2_score = model.score(X_scaled, y)
    print(f"[ML] Previsão gerada para usuário {user_id} - Mês: {target_month}")
    print(f"[ML] Energia prevista: {predicted_energy:.2f} kWh (intervalo 95%: {confidence_low:.2f} - {confidence_high:.2f})")
    print(f"[ML] R² Score: {r2_score:.3f} - Modelo treinado com {len(data)} dias de dados")
    return pred
