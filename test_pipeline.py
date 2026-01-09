from datetime import date

from core.pipeline import DailyPipeline
from core.segmentation import SegmentationAgent
from core.state import StateManager
from core.models import DailyLog, Task


if __name__ == "__main__":
    state = StateManager()
    pipeline = DailyPipeline(state)

    log = DailyLog(
        log_date=date.today(),
        raw_text="Went to gym. Felt distracted. Spent 200 on food. Walked in evening.",
        journal_text="Mind was cluttered today."
    )

    completed = [
        Task(title="Workout", planned=True, completed=True)
    ]

    result = pipeline.process_day(log, completed)
    print("\nSegments → Events:")
    for e in pipeline._match_events(SegmentationAgent.segment(log.raw_text), completed):
        print(e)

    print("\nFINAL RESULT:", result)
    print("\nXP Calculation Output:")
print(result)
