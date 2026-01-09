from datetime import date
from typing import List, Dict, Any

from core.segmentation import SegmentationAgent
from core.event_matching import EventMatcher
from core.xp_engine import XPEngine
from core.models import DailyLog, Task
from core.state import StateManager


class DailyPipeline:

    def __init__(self, state: StateManager):
        self.state = state
        self.xp_engine = XPEngine()

    # ==============================
    # MAIN ENTRY POINT
    # ==============================
    def process_day(self, daily_input: DailyLog, completed_tasks: List[Task] = None):

        print("Step 1 - Ingest")
        self._lock_day(daily_input)

        print("Step 2 - Segment Text")
        segments = self._segment_text(daily_input.raw_text)

        print("Step 3 - Match Events")
        event_data = self._match_events(segments, completed_tasks)

        print("Step 4 - Run Agents (placeholder)")
        agent_outputs = self._run_agents(event_data)

        print("Step 5 - XP + Modifiers")
        xp_results = self._calculate_xp(agent_outputs, daily_input)

        print("Step 6 - Anti-Farming")
        xp_final = self._apply_anti_farming(xp_results)

        print("Step 7 - Update State")
        self.state.update_from_day(xp_final)

        print("Step 8 - Snapshot")
        self.state.save_snapshot(daily_input.log_date, xp_final)

        return xp_final

    # ==============================
    # INTERNAL STEPS
    # ==============================

    def _lock_day(self, daily_input: DailyLog):
        return True

    def _segment_text(self, text: str):
        return SegmentationAgent.segment(text)

    def _match_events(self, segments, completed_tasks):
        matched = EventMatcher.match_events(segments, completed_tasks)
        return matched

    def _run_agents(self, event_data):
        # For now, no agent processing
        return event_data

    def _apply_anti_farming(self, xp_results: Dict[str, Any]):
        # Anti-farming comes later
        return xp_results

    def _calculate_xp(self, events, daily_input):

        # Step 1 — categories done today
        categories_done = {
            e["category"] for e in events if e["type"] == "task_event"
        }

        # Step 2 — update streaks
        self.state.update_streaks(categories_done, daily_input.log_date)

        # Step 3 — reset repetition
        self.state.reset_repetition()
        for e in events:
            if e["type"] == "task_event":
                self.state.repetition_count[e["category"]] += 1
        # Step 4 — raw XP calculation
        streak_multipliers = {
            c: self.state.get_consistency_multiplier(c)
            for c in self.state.streak_count.keys()
        }

        raw_xp = self.xp_engine.calculate_xp(
            events,
            streaks=streak_multipliers,
            repetition_count_map=self.state.repetition_count
        )
        # Step 5 — sum XP per stat
        per_stat = {
            "strength": 0,
            "intelligence": 0,
            "lifestyle": 0,
            "mental_health": 0,
            "financial_health": 0,
        }

        for e in raw_xp:
            per_stat[e["category"]] += e["final_xp"]

        # Step 6 — apply daily caps
        capped = self.state.apply_daily_caps(per_stat)

        # Step 7 — apply weekly caps
        weekly = self.state.apply_weekly_caps(capped)

        # Step 8 — store in weekly history
        for stat, amount in weekly.items():
            self.state.record_daily_xp(stat, amount)

        return weekly