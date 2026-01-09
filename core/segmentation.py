import re
from typing import List


class SegmentationAgent:

    @staticmethod
    def segment(text: str) -> List[str]:
        """
        Deterministic segmentation pipeline.
        Converts messy human text into clean atomic events.
        """

        if not text:
            return []

        # Normalize spacing
        text = text.strip().lower()

        # Replace newlines with spaces
        text = text.replace("\n", " ")

        # Insert periods for soft boundaries
        text = re.sub(r"(,|\band\b|\bbut\b)", ".", text)

        # Hard split on punctuation
        raw_parts = re.split(r"[.!?]", text)

        # Cleanup each segment
        segments = []
        for part in raw_parts:
            clean = part.strip()

            # Skip empty fragments
            if not clean:
                continue

            # Skip standalone garbage words
            if clean in {"and", "but", "then"}:
                continue

            segments.append(clean)

        # Merge extremely short fragments into previous ones
               # Merge extremely short fragments only when they are not meaningful events
        merged = []
        feeling_keywords = {"felt", "feel", "am", "was", "got", "became"}

        for seg in segments:
            words = seg.split()

            # If segment is short AND seems meaningless → merge
            if len(words) <= 2 and not any(w in feeling_keywords for w in words) and merged:
                merged[-1] = merged[-1] + " " + seg
            else:
                merged.append(seg)


        return merged
