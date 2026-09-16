from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    filtered_data = []
    for item in data:
        if item.get("state") == state:
            filtered_data.append(item)
    return filtered_data


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    return sorted(data, key=lambda item: str(item.get("date", "")), reverse=reverse)