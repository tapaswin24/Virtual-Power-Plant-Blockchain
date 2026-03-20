def calculate_ac_tariff(bimonthly_kwh):
    """
    Modular bimonthly AC load calculation split strictly into user-defined segments.
    """
    b_units = max(bimonthly_kwh, 0)
    
    if b_units <= 500:
        t1_u = min(b_units, 100)
        t2_u = min(max(b_units - 100, 0), 100)
        t3_u = min(max(b_units - 200, 0), 200)
        t4_u = min(max(b_units - 400, 0), 100)
        return {
            "category": "<= 500 Units Slab",
            "tier (0-100 units)": {"units": round(t1_u,2), "cost": round(t1_u * 0, 2), "rate": 0},
            "tier (101-200 units)": {"units": round(t2_u,2), "cost": round(t2_u * 4.95, 2), "rate": 4.95},
            "tier (201-400 units)": {"units": round(t3_u,2), "cost": round(t3_u * 4.95, 2), "rate": 4.95},
            "tier (401-500 units)": {"units": round(t4_u,2), "cost": round(t4_u * 6.65, 2), "rate": 6.65},
            "total": round((t1_u*0) + (t2_u*4.95) + (t3_u*4.95) + (t4_u*6.65), 2)
        }
    else:
        t1_u = min(b_units, 100)
        t2_u = min(max(b_units - 100, 0), 300)
        t3_u = min(max(b_units - 400, 0), 200)
        t4_u = min(max(b_units - 600, 0), 200)
        t5_u = min(max(b_units - 800, 0), 200)
        t6_u = max(b_units - 1000, 0)
        return {
            "category": "> 500 Units Slab",
            "tier (0-100 units)": {"units": round(t1_u,2), "cost": round(t1_u * 0, 2), "rate": 0},
            "tier (101-400 units)": {"units": round(t2_u,2), "cost": round(t2_u * 4.95, 2), "rate": 4.95},
            "tier (401-600 units)": {"units": round(t3_u,2), "cost": round(t3_u * 6.65, 2), "rate": 6.65},
            "tier (601-800 units)": {"units": round(t4_u,2), "cost": round(t4_u * 9.95, 2), "rate": 9.95},
            "tier (801-1000 units)": {"units": round(t5_u,2), "cost": round(t5_u * 11.05, 2), "rate": 11.05},
            "tier (> 1000 units)": {"units": round(t6_u,2), "cost": round(t6_u * 12.15, 2), "rate": 12.15},
            "total": round((t1_u*4.95) + (t2_u*4.95) + (t3_u*6.65) + (t4_u*9.95) + (t5_u*11.05) + (t6_u*12.15), 2)
        }

def calculate_bimonthly_financials(bimonthly_charge_kwh, bimonthly_renewable_kwh):
    """
    Extrapolates user-defined Bimonthly battery charging logic and applies 
    the fixed 4.45rs/unit savings bound explicitly mapped to Renewable energy grids.
    """
    # Fixed solar offset savings rate
    bimonthly_savings = bimonthly_renewable_kwh * 4.45
    
    # 24H DC Charging algebra normalized around an active 60-day window
    avg_charging_kw = bimonthly_charge_kwh / 1440.0  # (60 days * 24 hrs)
    x_charge = avg_charging_kw / 24.0
    
    daily_charge_cost = (7 * x_charge * 9.75) + (7 * x_charge * 6.5) + (10 * x_charge * 8.10)
    bimonthly_charge_cost = daily_charge_cost * 60
    
    return bimonthly_charge_cost, bimonthly_savings