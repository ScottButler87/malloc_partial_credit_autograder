from typing import Any, Dict, List, Union


class AutograderTestResult:
    def __init__(self, score=None, max_score=None, name=None, number=None,
                 output=None, tags=None, visibility=None, extra_data=None):
        self.score: Union[float, None] = score
        self.max_score: Union[float, None] = max_score
        self.name: Union[str, None] = name
        self.number: Union[float, None] = number
        self.output: Union[output, None] = output
        self.tags: Union[List[str], None] = tags
        self.visibility: Union[float, None] = visibility
        self.extra_data: Union[Dict, None] = extra_data
       

class LeaderboardEntry:
    SORT_ASCENDING = 'asc'

    def __init__(self, name=None, value=None, order=SORT_ASCENDING):
        self.name: Union[str, None] = name
        self.value: Union[float, None] = value
        self.order: Union[str, None] = order


class AutograderResult:
    VISIBILITY_AFTER_DUE_DATE = 'after_due_date'
    VISIBILITY_AFTER_PUBLISHED = 'after_published'
    VISIBILITY_HIDDEN = 'hidden'
    VISIBILITY_VISIBLE = 'visible'

    def __init__(self, score=None, execution_time=None, output=None, visibility=VISIBILITY_HIDDEN,
                 stdout_visibility=VISIBILITY_HIDDEN, extra_data=None, tests=None, leaderboard=None):
        self.score: Union[float, None] = score
        self.execution_time: Union[float, None] = execution_time
        self.output: Union[str, None] = output
        self.visibility: Union[str, None] = visibility
        self.stdout_visibility: Union[str, None] = stdout_visibility
        self.extra_data: Union[Dict[str, Any], None] = extra_data
        self.tests: [Union[List[AutograderTestResult], None]] = tests
        self.leaderboard: Union[List[LeaderboardEntry], None] = leaderboard
