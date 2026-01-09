from typing import Dict, List
from datetime import date

from core import state


class XPEngine:

    # Difficulty multipliers
    difficulty_multiplier = {
        "easy": 0.8,
        "normal": 1.0,
        "hard": 1.3,
        "very_hard": 1.6
    }

    # Base effort scoring (default placeholder)
    def get_effort_score(self, event):
        """
        v1: Dummy effort score.
        Strength tasks → 3
        Intelligence tasks → 3
        Lifestyle tasks → 2
        Everything else → 1
        """

        if event["type"] != "task_event":
            return 1

        cat = event.get("category", "")
        if cat in ["strength", "intelligence"]:
            return 3
        if cat == "lifestyle":
            return 2

        return 1

    def get_difficulty(self, event):

        """
        v1: difficulty classification.
        Later replaced by Task Classification Agent.
        """

        if event["type"] != "task_event":
            return "easy"

        cat = event.get("category", "")
        if cat in ["strength", "intelligence"]:
            return "normal"
        if cat == "lifestyle":
            return "easy"

        return "easy"

  
    # BASE XP FORMULA


    def base_xp(self, effort, difficulty, consistency):
        mult = self.difficulty_multiplier[difficulty]
        return effort * mult * consistency

   
    # DIMINISHING RETURNS (Anti-spam)


    def decay_xp(self, base_xp, repetition_count):
        decay = max(0.4, 1 - (repetition_count * 0.15))
        return base_xp * decay

   
    # MAIN XP CALCULATION


    def calculate_xp(self, events: List[Dict], streaks, repetition_count_map):
        """
        events: list of matched events from event_matching
        streaks: dict of streak stats for each category
        repetition_count_map: dict counting events in same category for the day
        """

        xp_events = []

        for event in events:

            # ignore non-task events
            if event["type"] != "task_event":
                continue

            category = event["category"]

            effort = self.get_effort_score(event)
            difficulty = self.get_difficulty(event)

            # consistency multiplier based on streaks
            consistency = streaks.get(category, 1.0)


            # get repetition count for this task category
            rep = repetition_count_map.get(category, 0)

            # compute base XP
            bxp = self.base_xp(effort, difficulty, consistency)

            # apply diminishing returns
            fxp = self.decay_xp(bxp, rep)

            # record event
            xp_events.append({
                "category": category,
                "effort": effort,
                "difficulty": difficulty,
                "base_xp": round(bxp, 2),
                "final_xp": round(fxp, 2)
            })

        return xp_events
