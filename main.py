import json
import random
import urllib.error
import urllib.request
from typing import Protocol, runtime_checkable


@runtime_checkable
class TemperatureSensor(Protocol):
    def read_temperature(self) -> float:
        ...

    def get_sensor_id(self) -> str:
        ...


class WeatherAPISensor:
    URL = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=46.4825&longitude=30.7233&current=temperature_2m"
    )

    def read_temperature(self) -> float:
        try:
            with urllib.request.urlopen(self.URL, timeout=10) as response:
                data = json.load(response)
            return float(data["current"]["temperature_2m"])
        except (urllib.error.URLError, TimeoutError) as e:
            raise RuntimeError(f"Network error: {e}") from e
        except (KeyError, ValueError, TypeError) as e:
            raise RuntimeError(f"Unexpected API response: {e}") from e

    def get_sensor_id(self) -> str:
        return "WAS26-Odesa"


class SimulatedSensor:
    def __init__(self, base: float, deviation: float) -> None:
        self.base = base
        self.deviation = deviation

    def read_temperature(self) -> float:
        return self.base + random.uniform(-self.deviation, self.deviation)

    def get_sensor_id(self) -> str:
        return "SIM-SENSOR"


class FakeAlways25:
    def read_temperature(self) -> float:
        return 25.0

    def get_sensor_id(self) -> str:
        return "Fake-25"


class BrokenSensor:
    def read_temperature(self) -> float:
        raise RuntimeError("Sensor is broken!")

    def get_sensor_id(self) -> str:
        return "BROKEN-999"


class RealDHT22:
    def read_temperature(self) -> float:
        return 22.0

    def get_sensor_id(self) -> str:
        return "DHT22-001"


def monitor_room(sensors: list[TemperatureSensor]) -> None:
    for sensor in sensors:
        sensor_id = sensor.get_sensor_id()
        try:
            temperature = sensor.read_temperature()
            print(f"[{sensor_id}] Temperature: {temperature:.1f} °C")
        except Exception as e:
            print(f"[{sensor_id}] ERROR: {e}")


if __name__ == "__main__":
    sensors: list[TemperatureSensor] = [
        WeatherAPISensor(),
        SimulatedSensor(base=21.5, deviation=3.0),
        FakeAlways25(),
        BrokenSensor(),
    ]
    monitor_room(sensors)

    print()
    print(isinstance(RealDHT22(), TemperatureSensor))
    print(isinstance({"temp": 22}, TemperatureSensor))
