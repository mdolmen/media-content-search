from datetime import datetime, timedelta

def float_to_datetime(seconds):
    """
    Convert a number of seconds in datetime format.
    """
    delta = timedelta(seconds=seconds)
    reference_datetime = datetime(1, 1, 1, 0, 0, 0)
    result_datetime = reference_datetime + delta
    result_str = result_datetime.strftime("%H:%M:%S")

    return result_str
