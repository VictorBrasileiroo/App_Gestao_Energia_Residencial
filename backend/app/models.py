# app/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime

# =========================
# Tabela de Usuários
# =========================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # relacionamentos
    tariff_plans = relationship("TariffPlan", back_populates="user")
    hourly_records = relationship("ConsumptionHourly", back_populates="user")
    daily_records = relationship("ConsumptionDaily", back_populates="user")
    alert_rules = relationship("AlertRule", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
    predictions = relationship("Prediction", back_populates="user")


# =========================
# Tarifas (plano do usuário)
# =========================
class TariffPlan(Base):
    __tablename__ = "tariff_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)
    price_per_kwh = Column(Float, nullable=False, default=0.0)
    currency = Column(String, default="BRL")

    user = relationship("User", back_populates="tariff_plans")


# =========================
# Consumo por hora
# =========================
class ConsumptionHourly(Base):
    __tablename__ = "consumption_hourly"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    energy_kwh = Column(Float, nullable=False)

    user = relationship("User", back_populates="hourly_records")


# =========================
# Consumo diário
# =========================
class ConsumptionDaily(Base):
    __tablename__ = "consumption_daily"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    energy_kwh = Column(Float, nullable=False)

    user = relationship("User", back_populates="daily_records")


# =========================
# Regras de alerta
# =========================
class AlertRule(Base):
    __tablename__ = "alert_rules"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    rule_type = Column(String, nullable=False)  # FIXED_THRESHOLD ou MOVING_AVERAGE
    config = Column(JSON, nullable=True)
    enabled = Column(Boolean, default=True)

    user = relationship("User", back_populates="alert_rules")
    alerts = relationship("Alert", back_populates="alert_rule")


# =========================
# Alertas disparados
# =========================
class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    alert_rule_id = Column(Integer, ForeignKey("alert_rules.id"), nullable=True)
    trigger_date = Column(Date, nullable=False)
    value_kwh = Column(Float, nullable=True)
    status = Column(String, default="OPEN")  # OPEN, ACKNOWLEDGED

    user = relationship("User", back_populates="alerts")
    alert_rule = relationship("AlertRule", back_populates="alerts")


# =========================
# Predições
# =========================
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_month = Column(String, nullable=False)  # ex: "2025-11"
    energy_kwh_pred = Column(Float, nullable=False)
    cost_pred = Column(Float, nullable=False)
    confidence_low_kwh = Column(Float, nullable=True)
    confidence_high_kwh = Column(Float, nullable=True)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="predictions")
