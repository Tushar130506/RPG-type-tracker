from datetime import date, timedelta
from typing import Dict, Any


class StateManager:

    def __init__(self):

        # Weekly XP history per category
        self.weekly_xp = {
            "strength": [],
            "intelligence": [],
            "lifestyle": [],
            "mental_health": [],
            "financial_health": []
        }

        self.stats = {
            "strength": 50,
            "intelligence": 50,
            "lifestyle": 50,
            "mental_health": 50,
            "financial_health": 50,
        }

        # streaks per category
        self.streak_count = {
            "strength": 0,
            "intelligence": 0,
            "lifestyle": 0,
        }

        # repetition counts reset every day
        self.repetition_count = {
            "strength": 0,
            "intelligence": 0,
            "lifestyle": 0,
        }

        # Last active day per category
        self.last_active_day = {
            "strength": None,
            "intelligence": None,
            "lifestyle": None,
        }
    # -----------------------------------------------------
    # Store daily XP for weekly averaging
    # -----------------------------------------------------
    def record_daily_xp(self, stat, amount):
        
        xp_list = self.weekly_xp[stat]
        xp_list.append(amount)

        # Limit to last 7 days
        if len(xp_list) > 7:
            xp_list.pop(0)
    
    # -----------------------------------------------------
    # Enforces:
       # - Hard cap: max 25 XP per stat per day
       # - Soft cap after 18 XP (extra * 0.6)
    # -----------------------------------------------------

    def apply_daily_caps(self, xp_per_stat):
        capped = {}

        for stat, amount in xp_per_stat.items():

            if amount <= 18:
                capped[stat] = amount
            else:
                extra = amount - 18
                capped_amount = 18 + (extra * 0.6)
                capped_amount = min(capped_amount, 25)
                capped[stat] = round(capped_amount, 2)
        return capped
    # -----------------------------------------------------
    # If XP > (weekly_avg * 1.8), reduce excess by 30%.
    # -----------------------------------------------------

    def apply_weekly_caps(self, daily_xp):

        adjusted = {}

        for stat, amount in daily_xp.items():

            xp_list = self.weekly_xp[stat]
            
            if len(xp_list) == 0:
                adjusted[stat] = amount
                continue

            weekly_avg = sum(xp_list) / len(xp_list)
            threshold = weekly_avg * 1.8

            if amount > threshold:
                excess = amount - threshold
                reduced = amount - (excess * 0.30)
                adjusted[stat] = round(reduced, 2)
            else:
                adjusted[stat] = amount

        return adjusted

    # -----------------------------------------------------
    # Consistency multiplier based on streak count
    # -----------------------------------------------------
    def get_consistency_multiplier(self, category):
        streak = self.streak_count.get(category, 0)

        if streak == 0:
            return 1.0
        if streak == 1:
            return 1.2
        if 2 <= streak <= 4:
            return 1.35
        if streak >= 5:
            return 1.5

        return 1.0

    # -----------------------------------------------------
    # Update streaks after daily tasks
    # -----------------------------------------------------
    def update_streaks(self, categories_done_today, today_date):
        for category in self.streak_count.keys():

            # If user performed the category today
            if category in categories_done_today:

                last = self.last_active_day[category]

                # Continue streak if last active yesterday
                if last == today_date - timedelta(days=1):
                    self.streak_count[category] += 1
                else:
                    self.streak_count[category] = 1  # new streak

                self.last_active_day[category] = today_date

            else:
                # Streak broken
                self.streak_count[category] = 0

    # -----------------------------------------------------
    # Repetition tracking
    # -----------------------------------------------------
    def update_repetition(self, events):
        for e in events:
            if e["type"] == "task_event":
                cat = e["category"]
                self.repetition_count[cat] += 1

    def reset_repetition(self):
        for k in self.repetition_count:
            self.repetition_count[k] = 0

    # -----------------------------------------------------
    # Placeholder update/snapshot (DB later)
    # -----------------------------------------------------
    def update_from_day(self, xp_results):
        print("XP Results Applied:", xp_results)

    def save_snapshot(self, log_date: date, xp_final: Dict[str, Any]):
        print(f"Snapshot saved for {log_date}")
