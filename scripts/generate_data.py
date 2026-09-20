import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Configuration initiale
np.random.seed(42) # Reproductibilité stricte pour le TD
Faker.seed(42)
fake = Faker(['fr_FR', 'en_US', 'en_GB', 'de_DE', 'ja_JP'])

N_CUSTOMERS = 158
N_ORDERS = 200078
OUTPUT_DIR = 'data/landing'
START_DATE = '2025-01-01'
# La date maximale pour les commandes (ex: "Aujourd'hui", ou une date passée fixe)
SIMULATION_END_DATE = '2026-09-21'
# Le calendrier et les taux peuvent aller jusqu'à la fin de l'année
CALENDAR_END_DATE = '2026-12-31'


# Mapping réaliste Pays -> Devise (Strictement UE, US, UK)
COUNTRY_CURRENCY = {
    'France': 'EUR', 'Germany': 'EUR', 'Spain': 'EUR', 'Italy': 'EUR', 'United States': 'USD', 'United Kingdom': 'GBP'
}

# Catalogue de produits réalistes (Tech / Accessoires)
PRODUCTS = [
    # Périphériques de saisie
    {'id': 'PRD-001', 'name': 'Souris Ergonomique Sans Fil', 'base_price': 29.99},
    {'id': 'PRD-002', 'name': 'Clavier Mécanique RGB', 'base_price': 85.00},
    {'id': 'PRD-003', 'name': 'Repose-Poignet en Gel', 'base_price': 12.90},
    {'id': 'PRD-004', 'name': 'Tapis de Souris XXL', 'base_price': 15.00},

    # Audio & Vidéo
    {'id': 'PRD-005', 'name': 'Casque à Réduction de Bruit', 'base_price': 150.00},
    {'id': 'PRD-006', 'name': 'Webcam Full HD 1080p', 'base_price': 45.00},
    {'id': 'PRD-007', 'name': 'Microphone Podcast USB', 'base_price': 65.00},
    {'id': 'PRD-008', 'name': 'Enceintes PC Bluetooth 2.1', 'base_price': 55.00},

    # Connectique & Énergie
    {'id': 'PRD-009', 'name': 'Hub USB-C 7-en-1', 'base_price': 35.50},
    {'id': 'PRD-010', 'name': 'Chargeur Rapide GaN 100W', 'base_price': 49.90},
    {'id': 'PRD-011', 'name': 'Batterie Externe 20000mAh', 'base_price': 39.99},
    {'id': 'PRD-012', 'name': 'Câble HDMI 2.1 Tressé (2m)', 'base_price': 12.50},
    {'id': 'PRD-013', 'name': 'Adaptateur Ethernet USB-C', 'base_price': 19.99},
    {'id': 'PRD-014', 'name': 'Onduleur (UPS) 900VA', 'base_price': 120.00},

    # Stockage
    {'id': 'PRD-015', 'name': 'Disque Externe SSD 1To', 'base_price': 110.00},
    {'id': 'PRD-016', 'name': 'Clé USB 3.2 256Go', 'base_price': 22.50},
    {'id': 'PRD-017', 'name': 'Carte MicroSD 512Go Pro', 'base_price': 45.00},

    # Ergonomie & Mobilier
    {'id': 'PRD-018', 'name': 'Support Ordinateur Portable', 'base_price': 24.90},
    {'id': 'PRD-019', 'name': 'Bras Articulé Double Écran', 'base_price': 75.00},
    {'id': 'PRD-020', 'name': 'Siège Ergonomique Bureau', 'base_price': 299.00},
    {'id': 'PRD-021', 'name': 'Lampe de Bureau LED Tactile', 'base_price': 35.00},
    {'id': 'PRD-022', 'name': 'Sac à Dos Ordinateur Antivol', 'base_price': 65.00},

    # Écrans & Réseau
    {'id': 'PRD-023', 'name': 'Écran PC Gamer 27" 144Hz', 'base_price': 250.00},
    {'id': 'PRD-024', 'name': 'Répéteur Mesh WiFi 6', 'base_price': 89.90},
    {'id': 'PRD-025', 'name': 'Kit Nettoyage Écran & Clavier', 'base_price': 14.90},
]

def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def generate_calendar():
    print("📅 Génération de la table Calendar...")
    dates = pd.date_range(start=START_DATE, end=CALENDAR_END_DATE)
    cal = pd.DataFrame({'date': dates})
    cal['year'] = cal['date'].dt.year
    cal['month'] = cal['date'].dt.month
    cal['day'] = cal['date'].dt.day
    cal['day_of_week'] = cal['date'].dt.dayofweek
    cal['is_weekend'] = cal['day_of_week'].isin([5, 6])
    return cal

def generate_exchange_rates():
    print("💱 Génération des taux de change (Fermé le week-end)...")
    bdates = pd.bdate_range(start=START_DATE, end=SIMULATION_END_DATE) # On s'arrête avant la fin de l'année pour éviter les dates futures
    rates = []

    base_rates = {'EUR': 1.0, 'USD': 1.08, 'GBP': 0.85}
    volatility = 0.005 # Variation quotidienne

    for currency, base_rate in base_rates.items():
        current_rate = base_rate
        for date in bdates:
            # FIX : L'Euro reste strictement à 1.0 par rapport à lui-même
            if currency == 'EUR':
                current_rate = 1.0
            else:
                # Marche aléatoire pour simuler les fluctuations boursières
                current_rate = current_rate * (1 + np.random.normal(0, volatility))

            rates.append({'date': date, 'currency_from': 'EUR', 'currency_to': currency, 'rate': round(current_rate, 4)})

    return pd.DataFrame(rates)

def generate_products_scd2():
    print("📦 Génération du catalogue produits (SCD2)...")
    scd2_records = []

    for prod in PRODUCTS:
        # Certains produits subissent une hausse de prix due à l'inflation en cours d'année
        has_price_change = np.random.choice([True, False], p=[0.4, 0.6])

        if has_price_change:
            change_date = pd.to_datetime('2026-01-01') + pd.Timedelta(days=np.random.randint(1, 180))
            scd2_records.append({
                'product_id': prod['id'], 'product_name': prod['name'],
                'price': prod['base_price'], 'start_date': pd.to_datetime(START_DATE), 'end_date': change_date - pd.Timedelta(days=1)
            })
            scd2_records.append({
                'product_id': prod['id'], 'product_name': prod['name'],
                'price': round(prod['base_price'] * 1.15, 2), # +15% inflation
                'start_date': change_date, 'end_date': pd.to_datetime('2099-12-31')
            })
        else:
            scd2_records.append({
                'product_id': prod['id'], 'product_name': prod['name'],
                'price': prod['base_price'], 'start_date': pd.to_datetime(START_DATE), 'end_date': pd.to_datetime('2099-12-31')
            })

    return pd.DataFrame(scd2_records)

def generate_customers():
    print("👥 Génération des clients...")
    customers = []
    countries = list(COUNTRY_CURRENCY.keys())

    for i in range(1, N_CUSTOMERS + 1):
        country = np.random.choice(countries)
        customers.append({
            'customer_id': f'CUST-{i:04d}',
            'name': fake.name(),
            'country': country,
            'signup_date': fake.date_time_between(start_date=pd.to_datetime('2024-01-01'), end_date=pd.to_datetime(SIMULATION_END_DATE)).date()
        })
    return pd.DataFrame(customers)

def generate_orders_and_payments(customers_df, products_scd2_df, rates_df):
    print(f"🛒 Génération de {N_ORDERS} commandes et paiements (Calcul vectorisé)...")

    # 1. Commandes de base
    order_dates = pd.to_datetime(np.random.choice(pd.date_range(START_DATE, SIMULATION_END_DATE, freq='h'), N_ORDERS))
    order_dates = np.sort(order_dates) # Chronologique

    orders = pd.DataFrame({
        'order_id': [f'ORD-{i:07d}' for i in range(1, N_ORDERS + 1)],
        'customer_id': np.random.choice(customers_df['customer_id'], N_ORDERS),
        'product_id': np.random.choice(products_scd2_df['product_id'].unique(), N_ORDERS),
        'quantity': np.random.choice([1, 2, 3, 5], N_ORDERS, p=[0.7, 0.2, 0.08, 0.02]),
        'order_date': order_dates,
        'status': np.random.choice(['COMPLETED', 'SHIPPED', 'CANCELLED'], N_ORDERS, p=[0.85, 0.10, 0.05])
    })

    # 2. Résolution du prix SCD2 (merge_asof pour trouver le prix à l'instant T)
    orders = orders.sort_values('order_date')
    products_scd2_sorted = products_scd2_df.sort_values('start_date')
    orders_with_price = pd.merge_asof(
        orders, products_scd2_sorted[['product_id', 'start_date', 'price']],
        left_on='order_date', right_on='start_date', by='product_id', direction='backward'
    )

  # 3. Préparation des paiements (Attribution Devise + Taux de change + Date)
    payments = orders_with_price[['order_id', 'customer_id', 'order_date', 'quantity', 'price']].copy()
    payments['payment_id'] = [f'PAY-{i:07d}' for i in range(1, N_ORDERS + 1)]
    payments = payments.merge(customers_df[['customer_id', 'country']], on='customer_id', how='left')
    payments['currency'] = payments['country'].map(COUNTRY_CURRENCY)

    # Rapprochement du taux de change (date de paiement / commande tronquée au jour)
    payments['payment_date'] = payments['order_date'] # On fixe la date de paiement égale à la date de commande
    payments['date_only'] = payments['payment_date'].dt.normalize()

    # Rapprochement du taux de change
    payments = payments.merge(rates_df[['date', 'currency_to', 'rate']],
                              left_on=['date_only', 'currency'], right_on=['date', 'currency_to'], how='left')

    # Calcul du montant brut (avec ffill temporaire des taux pour le script)
    temp_rates = rates_df.pivot(index='date', columns='currency_to', values='rate').asfreq('D').ffill().reset_index()
    payments = payments.merge(temp_rates.melt(id_vars='date', value_name='filled_rate'),
                              left_on=['date_only', 'currency'], right_on=['date', 'currency_to'], how='left')

    payments['amount'] = round(payments['quantity'] * payments['price'] * payments['filled_rate'], 2)
    payments['payment_method'] = np.random.choice(['CREDIT_CARD', 'PAYPAL', 'BANK_TRANSFER', 'APPLE_PAY'], len(payments))

    # On garde payment_date dans les colonnes finales du fichier brut
    payments = payments[['payment_id', 'order_id', 'payment_date', 'amount', 'currency', 'payment_method']]

    return orders, payments

def inject_anomalies(orders, payments):
    print("🦠 Injection des anomalies DataOps...")

    # -- ANOMALIES MINEURES (4%) --
    minor_mask_orders = np.random.rand(len(orders)) < 0.04
    minor_mask_payments = np.random.rand(len(payments)) < 0.04

    # Quantités nulles ou négatives
    orders.loc[minor_mask_orders, 'quantity'] = np.random.choice([0, -1], sum(minor_mask_orders))
    # Montants négatifs
    payments.loc[minor_mask_payments, 'amount'] = -payments.loc[minor_mask_payments, 'amount']
    # Statut inconnu
    orders.loc[minor_mask_orders & (np.random.rand(len(orders)) < 0.3), 'status'] = 'UNKNOWN'
    # Méthode de paiement manquante
    payments.loc[minor_mask_payments & (np.random.rand(len(payments)) < 0.3), 'payment_method'] = np.nan

    # -- ANOMALIES CRITIQUES (1%) --
    major_mask_orders = np.random.rand(len(orders)) < 0.01
    major_mask_payments = np.random.rand(len(payments)) < 0.01

    # Commandes sans client (Rupture d'intégrité référentielle)
    orders.loc[major_mask_orders, 'customer_id'] = np.nan
    # Paiements orphelins (Effacement de l'order_id)
    payments.loc[major_mask_payments, 'order_id'] = np.nan
    # Produit inexistant
    orders.loc[major_mask_orders & (np.random.rand(len(orders)) < 0.3), 'product_id'] = 'PRD-999'

    return orders, payments

def align_customer_signup_dates(customers, orders):
    print("🗓️ Alignement temporel : signup_date <= date de première commande...")
    # Trouver la date de la première commande pour chaque client
    first_orders = orders.groupby('customer_id')['order_date'].min().reset_index()
    first_orders.rename(columns={'order_date': 'first_order_date'}, inplace=True)

    # Joindre cette info à la table des clients
    customers = customers.merge(first_orders, on='customer_id', how='left')

    # Pour les clients ayant passé commande, reculer la date d'inscription de 0 à 30 jours avant le premier achat
    mask = customers['first_order_date'].notna()
    random_offsets = pd.to_timedelta(np.random.randint(0, 30, size=mask.sum()), unit='d')

    # Appliquer le calcul et ne garder que la date (sans l'heure)
    customers.loc[mask, 'signup_date'] = (customers.loc[mask, 'first_order_date'] - random_offsets).dt.date

    # Nettoyer la colonne temporaire
    customers = customers.drop(columns=['first_order_date'])
    return customers


def main():
    ensure_dir()

    cal = generate_calendar()
    rates = generate_exchange_rates()
    scd2 = generate_products_scd2()
    cust = generate_customers()

    orders, payments = generate_orders_and_payments(cust, scd2, rates)

    # --- NOUVEAU : Réconciliation des dates ---
    cust = align_customer_signup_dates(cust, orders)

    # Injection des anomalies APRES la réconciliation
    orders, payments = inject_anomalies(orders, payments)

    # Sauvegarde en CSV
    print("💾 Sauvegarde des fichiers dans data/landing/ ...")
    cal.to_csv(f'{OUTPUT_DIR}/calendar.csv', index=False)
    rates.to_csv(f'{OUTPUT_DIR}/exchange_rates.csv', index=False)
    scd2.to_csv(f'{OUTPUT_DIR}/products_scd2.csv', index=False)
    cust.to_csv(f'{OUTPUT_DIR}/raw_customers.csv', index=False)
    orders.to_csv(f'{OUTPUT_DIR}/raw_orders.csv', index=False)
    payments.to_csv(f'{OUTPUT_DIR}/raw_payments.csv', index=False)

    total_revenue_eur = (payments['amount'] / np.where(payments['currency'] == 'EUR', 1, 1.08)).sum() # Approx pour l'affichage
    print(f"✅ Terminé ! {N_ORDERS} commandes générées. CA estimé: ~{total_revenue_eur/1000000:.2f} M€")

if __name__ == "__main__":
    main()
