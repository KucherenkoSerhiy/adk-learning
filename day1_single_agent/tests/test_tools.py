from day1_single_agent.city import convert_timezone, get_current_time, get_forecast


def test_get_current_time_known_city_succeeds():
    result = get_current_time("Tokyo")
    assert result["status"] == "success"
    assert result["city"] == "Tokyo"


def test_get_current_time_unknown_city_errors():
    assert get_current_time("Nowhereville")["status"] == "error"


def test_get_forecast_known_city_returns_forecast():
    result = get_forecast("Berlin")
    assert result["status"] == "success"
    assert "forecast" in result


def test_get_forecast_unknown_city_errors():
    assert get_forecast("Nowhereville")["status"] == "error"


def test_convert_timezone_unknown_city_errors():
    result = convert_timezone("Nowhereville", "Tokyo", "2026-01-01T10:00:00")
    assert result["status"] == "error"


def test_convert_timezone_uses_the_source_citys_timezone_not_the_machines_local_time():
    result = convert_timezone("Tokyo", "Beijing", "2026-01-15T10:00:00")
    assert result["status"] == "success"
    assert result["converted_time"].startswith("2026-01-15 09:00:00")

    assert result["offset_hours"] == 0.0
