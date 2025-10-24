from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from ..database import SessionLocal
from ..models import ConsumptionDaily, ConsumptionHourly, TariffPlan, Prediction, Alert
from ..auth.routes import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("/monthly-comparison")
def get_monthly_comparison(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Retorna dados mensais para comparação histórica - linha verde SÓ até outubro"""
    user_id = current_user.id
    from collections import defaultdict
    from datetime import datetime
    
    # Pegar todos os dados disponíveis
    all_data = db.query(ConsumptionDaily).filter_by(user_id=user_id).order_by(ConsumptionDaily.date).all()
    
    if not all_data:
        return {"monthly_data": [], "has_prediction": False}
    
    # Data de HOJE para referência (21 de outubro de 2025)
    today = datetime.now().date()
    
    # Agrupar por mês - excluindo meses FUTUROS
    monthly_totals = defaultdict(float)
    for record in all_data:
        # CRÍTICO: Só incluir registros até HOJE
        if record.date <= today:
            month_key = record.date.strftime("%Y-%m")
            monthly_totals[month_key] += record.energy_kwh
    
    # Se não houver dados, retornar vazio
    if not monthly_totals:
        return {"monthly_data": [], "has_prediction": False}
    
    # Pegar os últimos 6 meses com dados (termina em outubro 2025)
    sorted_months = sorted(monthly_totals.keys())[-6:]
    
    monthly_data = []
    for month_key in sorted_months:
        year, month = month_key.split('-')
        month_name = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][int(month)-1]
        
        monthly_data.append({
            "label": month_name,
            "month_key": month_key,
            "energy_kwh": round(monthly_totals[month_key], 2),
            "is_prediction": False
        })
    
    # Adicionar predição para NOVEMBRO 2025 - SEM aleatoriedade
    pred = db.query(Prediction).filter_by(user_id=user_id).order_by(Prediction.generated_at.desc()).first()
    if pred:
        # Novembro (predição base do modelo ML)
        monthly_data.append({
            "label": "Nov (Prev)",
            "month_key": "2025-11",
            "energy_kwh": round(pred.energy_kwh_pred, 2),
            "is_prediction": True
        })
        
        # Dezembro (usando 108% da predição de novembro - valor fixo, não aleatório)
        monthly_data.append({
            "label": "Dez (Prev)", 
            "month_key": "2025-12",
            "energy_kwh": round(pred.energy_kwh_pred * 1.08, 2),  # Valor fixo 8% maior
            "is_prediction": True
        })
    
    return {
        "monthly_data": monthly_data,
        "has_prediction": pred is not None
    }

@router.get("/")
def get_dashboard(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id

    # Pegar a data mais recente disponível nos dados do usuário (independente do ano)
    most_recent_record = db.query(ConsumptionDaily).filter_by(user_id=user_id).order_by(ConsumptionDaily.date.desc()).first()
    
    if not most_recent_record:
        # Se não há dados, retornar estrutura vazia
        return {
            "summary_today": {
                "date": str(date.today()),
                "energy_kwh": 0,
                "cost_brl": 0,
                "comparison_vs_yesterday_pct": 0
            },
            "daily_view_last_7_days": {
                "series": []
            },
            "next_month_prediction": {
                "target_month": None,
                "energy_kwh_pred": None,
                "cost_brl_pred": None
            }
        }
    
    # Usar a data mais recente como "hoje" - SEMPRE dados reais do banco
    reference_date = most_recent_record.date
    yesterday_date = reference_date - timedelta(days=1)

    # record de dados do dia mais recente e do dia anterior
    today_record = most_recent_record
    yesterday_record = db.query(ConsumptionDaily).filter_by(user_id=user_id, date=yesterday_date).first()

    # kwh gastos no dia mais recente e no anterior - DADOS REAIS
    today_kwh = today_record.energy_kwh if today_record else 0
    yesterday_kwh = yesterday_record.energy_kwh if yesterday_record else 0

    # comparacao entre a energia gasta - DADOS REAIS
    comparison = ((today_kwh - yesterday_kwh) / yesterday_kwh * 100) if yesterday_kwh else 0

    # tarifa e o preco por kwh
    tariff = db.query(TariffPlan).filter(TariffPlan.user_id == user_id).first()
    price = tariff.price_per_kwh if tariff else 0.70

    # Últimos 7 dias a partir da data mais recente disponível - DADOS REAIS
    start_7 = reference_date - timedelta(days=6)
    
    # Buscar dados dos últimos 7 dias reais do banco
    last_7 = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= start_7,
        ConsumptionDaily.date <= reference_date
    ).order_by(ConsumptionDaily.date).all()

    # Se não houver dados suficientes, pegar os últimos registros disponíveis
    if len(last_7) == 0:
        last_7 = db.query(ConsumptionDaily).filter(
            ConsumptionDaily.user_id == user_id
        ).order_by(ConsumptionDaily.date.desc()).limit(7).all()
        last_7.reverse()
    
    daily_series = [{"date": str(r.date), "energy_kwh": r.energy_kwh} for r in last_7]

    # predicao mais recente
    pred = db.query(Prediction).filter_by(user_id=user_id).order_by(Prediction.generated_at.desc()).first()

    # Buscar padrão de consumo por hora (média das últimas 24h de dados disponíveis)
    hourly_data = db.query(
        func.extract('hour', ConsumptionHourly.datetime).label('hour'),
        func.avg(ConsumptionHourly.energy_kwh).label('avg_kwh')
    ).filter(
        ConsumptionHourly.user_id == user_id
    ).group_by('hour').order_by('hour').all()
    
    hourly_pattern = [{"hour": int(h.hour), "avg_kwh": round(h.avg_kwh, 2)} for h in hourly_data]

    return {
        "summary_today": {
            "date": str(reference_date),
            "energy_kwh": today_kwh,
            "cost_brl": round(today_kwh * price, 2),
            "comparison_vs_yesterday_pct": round(comparison, 1)
        },
        "daily_view_last_7_days": {
            "series": daily_series
        },
        "hourly_pattern": hourly_pattern,
        "next_month_prediction": {
            "target_month": pred.target_month if pred else None,
            "energy_kwh_pred": pred.energy_kwh_pred if pred else None,
            "cost_brl_pred": pred.cost_pred if pred else None
        }
    }
