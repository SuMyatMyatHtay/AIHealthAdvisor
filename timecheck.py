from datetime import datetime

def is_it_7am():
    # Get the current time
    now = datetime.now()
    
    # Check if the current time is 7 AM
    if now.hour == 11 and now.minute == 15:
        return True
    else:
        return False

# Usage example
if is_it_7am():
    print("ALARM ON")
else:
    print("NO ALARM")
