from typing import List, Dict


class EventMatcher:

    # Keyword dictionaries for v1 (expand later)
    strength_keywords = ["gym", "workout", "exercise", "lift", "training"]
    intelligence_keywords = ["study", "coding", "python", "learning", "project"]
    lifestyle_keywords = ["cleaned", "laundry", "organized", "routine", "walk"]
    mental_keywords = ["anxious", "stress", "tired", "overwhelmed", "mood"]
    finance_keywords = ["spent", "bought", "paid", "rs", "₹", "rupees"]

    @classmethod
    def classify_segment(cls, segment: str) -> Dict:
        """
        Classifies each segmented text into a category and type.
        """

        segment = segment.lower()

        # Finance event
        if any(word in segment for word in cls.finance_keywords):
            return {"type": "finance_event", "raw": segment}

        # Mental state event
        if any(word in segment for word in cls.mental_keywords):
            return {"type": "mental_event", "raw": segment}

        # Strength task
        if any(word in segment for word in cls.strength_keywords):
            return {"type": "task_event", "category": "strength", "raw": segment}

        # Intelligence task
        if any(word in segment for word in cls.intelligence_keywords):
            return {"type": "task_event", "category": "intelligence", "raw": segment}

        # Lifestyle task
        if any(word in segment for word in cls.lifestyle_keywords):
            return {"type": "task_event", "category": "lifestyle", "raw": segment}

        # Nothing useful
        return {"type": "ignore_event", "raw": segment}

    @classmethod
    def match_events(cls, segments: List[str], completed_tasks=None):
        """
        Applies classification to each segment.
        """
        matched = [cls.classify_segment(seg) for seg in segments]
        return matched
