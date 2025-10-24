#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de dados realistas de consumo de energia elétrica
para uma família brasileira típica - 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_realistic_consumption():
    """
    Gera dados realistas de consumo horário para uma família brasileira
    Baseado em padrões típicos de uso residencial no Brasil
    """
    
    # Período: 01/01/2025 até 27/10/2025
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 10, 27, 23, 0, 0)  # Até 27/10/2025 23:00
    
    # Lista para armazenar os dados
    data = []
    
    current_datetime = start_date
    
    while current_datetime <= end_date:
        hour = current_datetime.hour
        month = current_datetime.month
        weekday = current_datetime.weekday()  # 0=segunda, 6=domingo
        
        # Padrão base por horário (família brasileira típica)
        base_consumption = {
            0: 0.12,   # Madrugada - geladeira, standby
            1: 0.11,   # Madrugada
            2: 0.10,   # Madrugada
            3: 0.10,   # Madrugada
            4: 0.11,   # Madrugada
            5: 0.15,   # Início despertar
            6: 0.35,   # Café da manhã, banho
            7: 0.45,   # Preparação para trabalho
            8: 0.30,   # Saída para trabalho
            9: 0.18,   # Casa vazia - básico
            10: 0.16,  # Casa vazia
            11: 0.18,  # Casa vazia
            12: 0.25,  # Almoço (alguns em casa)
            13: 0.20,  # Pós-almoço
            14: 0.18,  # Tarde
            15: 0.20,  # Tarde
            16: 0.22,  # Volta da escola/trabalho
            17: 0.28,  # Chegada em casa
            18: 0.40,  # Jantar, TV
            19: 0.50,  # Pico - TV, cozinha, banho
            20: 0.45,  # Pico noturno
            21: 0.42,  # TV, família reunida
            22: 0.35,  # Preparação para dormir
            23: 0.20,  # Final do dia
        }
        
        # Consumo base para a hora
        base_kwh = base_consumption[hour]
        
        # Ajustes sazonais (verão brasileiro = mais ar condicionado)
        seasonal_multiplier = 1.0
        if month in [12, 1, 2, 3]:  # Verão
            if hour in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]:
                seasonal_multiplier = 1.6  # Ar condicionado
            else:
                seasonal_multiplier = 1.2
        elif month in [6, 7, 8]:  # Inverno
            if hour in [6, 7, 18, 19, 20, 21]:
                seasonal_multiplier = 1.3  # Chuveiro elétrico mais usado
            else:
                seasonal_multiplier = 1.1
        else:  # Outono/Primavera
            seasonal_multiplier = 1.0
            
        # Ajustes por dia da semana
        weekend_multiplier = 1.0
        if weekday >= 5:  # Fim de semana
            if hour in [8, 9, 10, 11, 12, 13, 14, 15]:
                weekend_multiplier = 1.4  # Mais gente em casa
            else:
                weekend_multiplier = 1.2
                
        # Variação aleatória realista (-20% a +30%)
        random_variation = random.uniform(0.8, 1.3)
        
        # Calcular consumo final
        final_consumption = base_kwh * seasonal_multiplier * weekend_multiplier * random_variation
        
        # Garantir valores mínimos realistas
        final_consumption = max(final_consumption, 0.08)
        
        # Adicionar ruído para tornar mais realista
        noise = random.gauss(0, 0.02)  # Ruído gaussiano
        final_consumption += noise
        final_consumption = max(final_consumption, 0.05)  # Mínimo absoluto
        
        # Arredondar para precisão realista
        final_consumption = round(final_consumption, 6)
        
        data.append({
            'datetime': current_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'energy_kwh': final_consumption
        })
        
        # Próxima hora
        current_datetime += timedelta(hours=1)
    
    return data

def generate_daily_data(hourly_data):
    """
    Gera dados diários a partir dos dados horários
    """
    df_hourly = pd.DataFrame(hourly_data)
    df_hourly['datetime'] = pd.to_datetime(df_hourly['datetime'])
    df_hourly['date'] = df_hourly['datetime'].dt.date
    
    # Agrupar por dia e somar
    daily_data = df_hourly.groupby('date')['energy_kwh'].sum().reset_index()
    daily_data['date'] = daily_data['date'].astype(str)
    
    return daily_data.to_dict('records')

def main():
    print("🔄 Gerando dados realistas de consumo elétrico...")
    print("📅 Período: 01/01/2025 até 27/10/2025")
    print("🏠 Padrão: Família brasileira típica")
    
    # Gerar dados horários
    hourly_data = generate_realistic_consumption()
    print(f"✅ Gerados {len(hourly_data)} registros horários")
    
    # Gerar dados diários
    daily_data = generate_daily_data(hourly_data)
    print(f"✅ Gerados {len(daily_data)} registros diários")
    
    # Salvar arquivo horário
    df_hourly = pd.DataFrame(hourly_data)
    hourly_path = 'data/dados_consumo_por_hora.csv'
    df_hourly.to_csv(hourly_path, index=False)
    print(f"💾 Dados horários salvos em: {hourly_path}")
    
    # Salvar arquivo diário
    df_daily = pd.DataFrame(daily_data)
    daily_path = 'data/dados_consumo_por_dia.csv'
    df_daily.to_csv(daily_path, index=False)
    print(f"💾 Dados diários salvos em: {daily_path}")
    
    # Estatísticas
    avg_daily = df_daily['energy_kwh'].mean()
    max_daily = df_daily['energy_kwh'].max()
    min_daily = df_daily['energy_kwh'].min()
    
    print("\n📊 Estatísticas geradas:")
    print(f"   Consumo diário médio: {avg_daily:.2f} kWh")
    print(f"   Consumo diário máximo: {max_daily:.2f} kWh")
    print(f"   Consumo diário mínimo: {min_daily:.2f} kWh")
    print(f"   Consumo mensal estimado: {avg_daily * 30:.2f} kWh")
    
    print("\n🎉 Dados realistas gerados com sucesso!")
    print("🔄 Reinicie o backend para usar os novos dados")

if __name__ == "__main__":
    main()