import builtins
import json

from flight_logger import write_flight_log


def test_write_flight_log_closes_file(tmp_path, monkeypatch):
    events = [{"event": "takeoff"}]
    log_path = tmp_path / "flight.json"
    opened_files = []
    real_open = builtins.open

    def tracking_open(*args, **kwargs):
        file = real_open(*args, **kwargs)
        opened_files.append(file)
        return file

    monkeypatch.setattr(builtins, "open", tracking_open)

    write_flight_log(str(log_path), events)

    assert opened_files[0].closed
    assert json.loads(log_path.read_text(encoding="utf-8")) == events
