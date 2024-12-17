def _timecode_convert(time : int) -> str:
    """
    Converts time value from seconds to timecode value,
    str -like

    Example:
    ---------
    ::

            _timecode_convert(100)

    returns "01:40"
    """
    minutes = int(time/60)
    if minutes<10: minutes = f"0{minutes}"
    
    sec = int((time/60-int(time/60))*60)
    if sec<10: sec = f"0{sec}"

    return f'{minutes}:{sec}'