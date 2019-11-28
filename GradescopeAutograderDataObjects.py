from typing import Any, Dict, List, Union


class AutograderTestResult:
    def __init__(self):
        pass


class LeaderboardEntry:
    SORT_ASCENDING = 'asc'

    def __init__(self):
        self.name: Union[str, None]
        self.value: Union[float, None]
        self.order: Union[str, None]


class AutograderResult:
    VISIBILITY_AFTER_DUE_DATE = 'after_due_date'
    VISIBILITY_AFTER_PUBLISHED = 'after_published'
    VISIBILITY_HIDDEN = 'hidden'
    VISIBILITY_VISIBLE = 'visible'

    def __init__(self):
        self.score: Union[float, None]
        self.execution_time: Union[float, None]
        self.output: Union[str, None]
        self.visibility: Union[str, None]
        self.stdout_visibility: Union[str, None]
        self.extra_data: Union[Dict[str, Any], None]
        self.tests: [Union[List[AutograderTestResult], None]]
        self.leaderboard: Union[float, None]
