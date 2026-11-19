import json


def write_flight_log(filename: str, events: list[dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=2)
