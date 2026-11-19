class RecordManager:
    def __init__(self, records):
        self.records = records

    def filter_records(self, required_status, metric_limit):
        filtered_records = []

        for record in self.records:
            if (
                record["metric"] > metric_limit
                and record["status"] == required_status
            ):
                filtered_records.append(record)

        return filtered_records


def calculate_total_value(records, discount_enabled):
    total_value = 0

    for record in records:
        total_value += record["value"]

    if discount_enabled:
        total_value *= 0.9

    return total_value
