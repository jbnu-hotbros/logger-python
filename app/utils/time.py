from datetime import datetime, timezone, timedelta

def get_current_time(timezone_offset: int = 9):
    """
    Returns current time as datetime object with timezone information.
    
    Args:
        timezone_offset (int): Timezone offset in hours from UTC. 
                              Default is 9 (Asia/Seoul, Korea/Japan timezone).
                              Example: -5 for New York, 0 for London, +8 for Beijing
    
    Returns:
        datetime: Current time with specified timezone offset
    """
    # Get current UTC time
    utc_now = datetime.now(timezone.utc)
    
    # Add timezone offset
    offset = timedelta(hours=timezone_offset)
    local_time = utc_now + offset
    
    return local_time 