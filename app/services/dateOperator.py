from datetime import datetime, timezone

class DateOperator:
    @staticmethod 
    def normalizer(date):
        total_seconds = date.seconds + date.nanos / 1e9
        return datetime.fromtimestamp(total_seconds, tz=timezone.utc)
