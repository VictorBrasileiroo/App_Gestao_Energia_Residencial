"""
Serviço para análise de consumo por hora
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..models import ConsumptionHourly, ConsumptionDaily

def get_hourly_pattern(db: Session, user_id: int):
    """
    Retorna o padrão de consumo por hora do dia
    Agrupa todos os dados por hora e calcula a média
    """
    # Pegar dados de consumo horário
    most_recent = db.query(ConsumptionDaily).filter_by(user_id=user_id).order_by(ConsumptionDaily.date.desc()).first()
    
    if not most_recent:
        return []
    
    # Pegar dados dos últimos 30 dias
    cutoff_date = most_recent.date - timedelta(days=30)
    
    # Agrupar por hora do dia e calcular média
    hourly_data = db.query(
        func.extract('hour', ConsumptionHourly.datetime).label('hour'),
        func.avg(ConsumptionHourly.energy_kwh).label('avg_kwh'),
        func.count(ConsumptionHourly.id).label('count')
    ).filter(
        ConsumptionHourly.user_id == user_id,
        ConsumptionHourly.datetime >= cutoff_date
    ).group_by(
        func.extract('hour', ConsumptionHourly.datetime)
    ).order_by('hour').all()
    
    return [
        {
            'hour': int(row.hour),
            'avg_kwh': round(float(row.avg_kwh), 2),
            'count': row.count
        }
        for row in hourly_data
    ]

def get_daily_distribution(db: Session, user_id: int):
    """
    Retorna a distribuição de consumo por período do dia
    """
    most_recent = db.query(ConsumptionDaily).filter_by(user_id=user_id).order_by(ConsumptionDaily.date.desc()).first()
    
    if not most_recent:
        return {
            'morning': 0,
            'afternoon': 0,
            'evening': 0,
            'night': 0
        }
    
    cutoff_date = most_recent.date - timedelta(days=30)
    
    # Pegar todos dados horários dos últimos 30 dias
    hourly_records = db.query(ConsumptionHourly).filter(
        ConsumptionHourly.user_id == user_id,
        ConsumptionHourly.datetime >= cutoff_date
    ).all()
    
    morning = 0  # 6-12h
    afternoon = 0  # 12-18h
    evening = 0  # 18-24h
    night = 0  # 0-6h
    
    for record in hourly_records:
        hour = record.datetime.hour
        if 6 <= hour < 12:
            morning += record.energy_kwh
        elif 12 <= hour < 18:
            afternoon += record.energy_kwh
        elif 18 <= hour < 24:
            evening += record.energy_kwh
        else:
            night += record.energy_kwh
    
    return {
        'morning': round(morning, 2),
        'afternoon': round(afternoon, 2),
        'evening': round(evening, 2),
        'night': round(night, 2)
    }
