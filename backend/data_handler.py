from datetime import datetime, timezone
import math
import json
from backend.tariff import calculate_ac_tariff, calculate_bimonthly_financials

class DataHandler:
    def __init__(self):
        self.total_energy = 0
        self.grid_energy = 0
        
        # Riemann sums (Energy in Wh)
        self.ac_energy = 0.0
        self.dc_energy = 0.0
        self.batt_charge_energy = 0.0
        self.batt_discharge_energy = 0.0
        self.net_energy = 0.0

        # Flow tracking
        self.last_processed_timestamp = None
        self.total_uptime_hours = 0.0

    def parse(self, ts):
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))

    def process(self, prev1, curr1, prev2, curr2, is_history_replay=False):
        t1 = self.parse(prev1["created_at"])
        t2 = self.parse(curr1["created_at"])

        # Validate gap and freshness
        try:
            now_utc = datetime.now(timezone.utc)
        except:
            now_utc = datetime.utcnow()
            
        is_live_stale = False if is_history_replay else (now_utc - t2).total_seconds() > 300
        is_historical_drop = (t2 - t1).total_seconds() > 300
        is_stale = is_live_stale or is_historical_drop
        
        is_duplicate = (self.last_processed_timestamp == curr1["created_at"])
        self.last_processed_timestamp = curr1["created_at"]

        dt_hr = max((t2 - t1).total_seconds() / 3600, 0)
        
        if is_duplicate or is_historical_drop:
            dt_hr = 0  # Stop double counting or tracking offline phantom time

        self.total_uptime_hours += dt_hr

        # -------- CLOUD DATA (Anomalies Capped to 10kW) --------
        batt_v = min(float(curr1.get("field1") or 0), 200.0)
        batt_i = min(float(curr1.get("field2") or 0), 200.0)
        batt_soc = min(max(float(curr1.get("field3") or 0), 0.0), 100.0)
        rect_p = min(float(curr1.get("field6") or 0), 10000.0)
        solar_p = min(float(curr2.get("field3") or 0), 10000.0)
        grid_ac_p = min(float(curr2.get("field6") or 0), 10000.0)

        # Force instantaneous readouts to 0 if the backend is stuck on an old row
        if is_duplicate or is_stale:
            batt_v = batt_i = rect_p = solar_p = grid_ac_p = 0
            mode = "INACTIVE" if is_duplicate and not is_stale else "OFFLINE"
        elif rect_p > 0 or grid_ac_p > 0:
            mode = "GRID"
        elif solar_p > 0:
            mode = "SOLAR/BATTERY"
        else:
            mode = "BATTERY ONLY"

        battery_p = batt_v * batt_i
        total_power = solar_p + battery_p + rect_p
        ac_total = grid_ac_p + rect_p
        
        # -------- ENERGY ACCUMULATION --------
        self.ac_energy += ac_total * dt_hr
        
        discharging_power = battery_p if battery_p > 0 else 0
        self.dc_energy += (solar_p + discharging_power) * dt_hr
        
        if battery_p < 0:
            self.batt_charge_energy += abs(battery_p) * dt_hr
        elif battery_p > 0:
            self.batt_discharge_energy += battery_p * dt_hr
            
        self.net_energy = self.ac_energy + self.dc_energy

        # -------- CONSUMPTION METRICS EXTRAPOLATION --------
        ac_kwh = self.ac_energy / 1000.0
        dc_kwh = self.dc_energy / 1000.0
        batt_charge_kwh = self.batt_charge_energy / 1000.0
        
        if self.total_uptime_hours > 0:
            projected_daily_kwh = (ac_kwh / self.total_uptime_hours) * 24
            projected_daily_ren = (dc_kwh / self.total_uptime_hours) * 24
            projected_daily_chr = (batt_charge_kwh / self.total_uptime_hours) * 24
        else:
            projected_daily_kwh = 0
            projected_daily_ren = 0
            projected_daily_chr = 0
            
        bimonthly_kwh = projected_daily_kwh * 60
        bimonthly_renewable_kwh = projected_daily_ren * 60
        bimonthly_charge_kwh = projected_daily_chr * 60

        # -------- BIMONTHLY FINANCIALS LOGIC --------
        ac_tariff = calculate_ac_tariff(bimonthly_kwh)
        hypo_ac_tariff = calculate_ac_tariff(bimonthly_kwh + bimonthly_renewable_kwh)
        bimonthly_charge_cost, bimonthly_savings = calculate_bimonthly_financials(bimonthly_charge_kwh, bimonthly_renewable_kwh)

        # Basic Carbon output based on absolute Grid AC load metric (kg)
        carbon = ac_kwh * 0.82

        return {
            "mode": mode,
            "solar_power": round(solar_p, 2),
            "battery_power": round(battery_p, 2),
            "rectifier_power": round(rect_p, 2),
            "grid_ac_power": round(grid_ac_p, 2),
            "ac_total": round(ac_total, 2),
            "ac_energy": round(self.ac_energy, 2),
            "dc_energy": round(self.dc_energy, 2),
            "net_energy": round(self.net_energy, 2),
            "batt_charge_energy": round(self.batt_charge_energy, 2),
            "batt_discharge_energy": round(self.batt_discharge_energy, 2),
            "batt_soc": round(batt_soc, 2),
            
            "projected_daily_kwh": round(projected_daily_kwh, 2),
            "bimonthly_kwh": round(bimonthly_kwh, 2),
            "bimonthly_renewable_kwh": round(bimonthly_renewable_kwh, 2),
            "bimonthly_charge_kwh": round(bimonthly_charge_kwh, 2),
            "ac_tariff": ac_tariff,
            
            "bimonthly_charge_cost": round(bimonthly_charge_cost, 2),
            "bimonthly_savings": round(bimonthly_savings, 2),
            "hypo_ac_tariff_total": round(hypo_ac_tariff["total"], 2),
            "carbon": round(carbon, 3),

            "uptime_hours": round(self.total_uptime_hours, 2),
            "timestamp": curr1["created_at"],
            "is_stale": is_stale,
            "is_duplicate": is_duplicate
        }