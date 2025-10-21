"""
Modelo de Machine Learning para predição de consumo de energia
Usa LinearRegression com features de tendência, sazonalidade e padrões
"""
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from ..models import ConsumptionDaily, TariffPlan, Prediction
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


def generate_prediction_with_ml(db: Session, user_id: int):
    """
    Gera predição usando Machine Learning (LinearRegression)
    Considera tendências, sazonalidade e padrões históricos
    """
    # Pegar dados históricos
    most_recent = db.query(ConsumptionDaily).filter_by(user_id=user_id).order_by(ConsumptionDaily.date.desc()).first()
    
    if not most_recent:
        print(f"[INFO] Usuário {user_id} não possui dados.")
        return None
    
    reference_date = most_recent.date
    
    # Pegar pelo menos 60 dias de dados para treinar o modelo
    cutoff = reference_date - timedelta(days=90)
    data = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= cutoff,
        ConsumptionDaily.date <= reference_date
    ).order_by(ConsumptionDaily.date).all()
    
    if len(data) < 14:  # Mínimo de 2 semanas
        print(f"[INFO] Dados insuficientes para ML. Usando método simples.")
        return generate_simple_prediction(db, user_id, data, reference_date)
    
    # Preparar dados para o modelo
    dates = []
    consumptions = []
    
    for record in data:
        # Converter data para número ordinal (dias desde 01/01/0001)
        dates.append(record.date.toordinal())
        consumptions.append(record.energy_kwh)
    
    # Criar features
    X = np.array(dates).reshape(-1, 1)
    y = np.array(consumptions)
    
    # Adicionar features de tendência
    # Feature 1: Número do dia (ordinal)
    # Feature 2: Dia da semana (0-6)
    # Feature 3: Dia do mês (1-31)
    X_enhanced = []
    for i, record in enumerate(data):
        day_ordinal = record.date.toordinal()
        day_of_week = record.date.weekday()
        day_of_month = record.date.day
        
        # Normalizar dia da semana e dia do mês para 0-1
        dow_normalized = day_of_week / 6.0
        dom_normalized = (day_of_month - 1) / 30.0
        
        X_enhanced.append([day_ordinal, dow_normalized, dom_normalized])
    
    X_enhanced = np.array(X_enhanced)
    
    # Normalizar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_enhanced)
    
    # Treinar modelo
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Fazer predições para os próximos 30 dias
    first_day_next_month = reference_date + timedelta(days=1)
    predictions = []
    
    for i in range(30):
        future_date = first_day_next_month + timedelta(days=i)
        day_ordinal = future_date.toordinal()
        day_of_week = future_date.weekday()
        day_of_month = future_date.day
        
        dow_normalized = day_of_week / 6.0
        dom_normalized = (day_of_month - 1) / 30.0
        
        X_future = np.array([[day_ordinal, dow_normalized, dom_normalized]])
        X_future_scaled = scaler.transform(X_future)
        
        pred_value = model.predict(X_future_scaled)[0]
        # Garantir que predição não seja negativa
        pred_value = max(0, pred_value)
        predictions.append(pred_value)
    
    # Calcular estatísticas
    predicted_total = sum(predictions)
    predicted_avg = predicted_total / 30
    
    # Intervalo de confiança baseado no desvio padrão dos dados históricos
    std_dev = np.std(y)
    confidence_low = max(0, predicted_total - (std_dev * 5))
    confidence_high = predicted_total + (std_dev * 5)
    
    # Pegar tarifa
    tariff = db.query(TariffPlan).filter_by(user_id=user_id).first()
    price = tariff.price_per_kwh if tariff else 0.70
    
    # Calcular próximo mês
    first_day_next_month = reference_date.replace(day=1) + timedelta(days=32)
    target_month = first_day_next_month.replace(day=1).strftime("%Y-%m")
    
    # Criar predição
    prediction = Prediction(
        user_id=user_id,
        target_month=target_month,
        energy_kwh_pred=round(predicted_total, 2),
        cost_pred=round(predicted_total * price, 2),
        confidence_low_kwh=round(confidence_low, 2),
        confidence_high_kwh=round(confidence_high, 2),
        generated_at=datetime.utcnow()
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    print(f"[ML] Previsão gerada com ML para {target_month}: {predicted_total:.2f} kWh")
    print(f"[ML] Score do modelo R²: {model.score(X_scaled, y):.3f}")
    
    return prediction


def generate_simple_prediction(db: Session, user_id: int, data: list, reference_date: date):
    """
    Método de predição simples baseado em média móvel
    Usado quando há poucos dados para ML
    """
    if not data:
        return None
    
    # Calcular média dos últimos dias disponíveis
    avg_kwh = sum(r.energy_kwh for r in data) / len(data)
    
    # Aplicar fator de crescimento leve (2% ao mês)
    growth_factor = 1.02
    predicted_energy = avg_kwh * 30 * growth_factor
    
    # Intervalo de confiança de +/- 10%
    confidence_low = predicted_energy * 0.9
    confidence_high = predicted_energy * 1.1
    
    # Pegar tarifa
    tariff = db.query(TariffPlan).filter_by(user_id=user_id).first()
    price = tariff.price_per_kwh if tariff else 0.70
    
    # Calcular próximo mês
    first_day_next_month = reference_date.replace(day=1) + timedelta(days=32)
    target_month = first_day_next_month.replace(day=1).strftime("%Y-%m")
    
    # Criar predição
    prediction = Prediction(
        user_id=user_id,
        target_month=target_month,
        energy_kwh_pred=round(predicted_energy, 2),
        cost_pred=round(predicted_energy * price, 2),
        confidence_low_kwh=round(confidence_low, 2),
        confidence_high_kwh=round(confidence_high, 2),
        generated_at=datetime.utcnow()
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    print(f"[SIMPLE] Previsão gerada com método simples para {target_month}: {predicted_energy:.2f} kWh")
    
    return prediction
