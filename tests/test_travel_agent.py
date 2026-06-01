from fastapi.testclient import TestClient

from src.agent.travel_agent import TravelPlanningAgent, TravelRequest
from src.app import app
from src.tools.travel_tools import check_budget, estimate_trip_cost, get_weather, recommend_activities


client = TestClient(app)


def test_hanoi_tools_use_destination_specific_data():
    weather = get_weather("Hà Nội", "2026-12-01")
    activities = recommend_activities("Hà Nội", weather, "văn hóa và ăn uống", "standard")
    cost = estimate_trip_cost("Hà Nội", 3, activities, "standard")
    budget = check_budget(cost["total_cost"], 6_000_000)

    activity_names = [activity["name"] for activity in activities]
    assert weather["condition"] == "cloudy"
    assert "Văn Miếu" in activity_names or "Hoàng Thành Thăng Long" in activity_names
    assert cost["breakdown"]["hotel"] == 2_400_000
    assert budget["within_budget"] is True


def test_unknown_destination_uses_fallback_only():
    weather = get_weather("Bắc Kạn", "2026-07-01")
    activities = recommend_activities("Bắc Kạn", weather, "thiên nhiên", "budget")
    cost = estimate_trip_cost("Bắc Kạn", 2, activities, "budget")

    assert activities[0]["name"] == "Công viên trung tâm"
    assert cost["breakdown"]["transport"] == 500_000


def test_agent_returns_breakdown_and_advice():
    agent = TravelPlanningAgent()
    result = agent.plan_trip(
        TravelRequest(
            destination="Phú Quốc",
            date="2026-08-20",
            preference="biển và ăn uống",
            days=4,
            budget=12_000_000,
            travel_style="standard",
        )
    )

    assert len(result["thoughts"]) == 4
    assert result["actions"][0].startswith("get_weather")
    assert "hotel" in result["cost_breakdown"]
    assert result["travel_advice"]


def test_homepage_renders_generate_button():
    response = client.get("/")
    assert response.status_code == 200
    assert "Generate Travel Plan" in response.text


def test_plan_endpoint_supports_required_demo_destinations():
    cases = [
        {"destination": "Hà Nội", "date": "2026-12-01", "preference": "văn hóa và ăn uống", "days": 3, "budget": 6_000_000, "travel_style": "standard"},
        {"destination": "Sapa", "date": "2026-10-15", "preference": "thiên nhiên và ăn uống", "days": 3, "budget": 7_000_000, "travel_style": "standard"},
        {"destination": "Đà Lạt", "date": "2026-07-10", "preference": "thiên nhiên", "days": 4, "budget": 3_000_000, "travel_style": "budget"},
        {"destination": "Đà Nẵng", "date": "2026-06-15", "preference": "biển và ăn uống", "days": 3, "budget": 4_000_000, "travel_style": "standard"},
        {"destination": "Phú Quốc", "date": "2026-08-20", "preference": "biển và ăn uống", "days": 4, "budget": 12_000_000, "travel_style": "standard"},
        {"destination": "Quảng Ninh (Hạ Long)", "date": "2026-08-20", "preference": "thiên nhiên và văn hóa", "days": 2, "budget": 5_000_000, "travel_style": "standard"},
    ]

    for payload in cases:
        response = client.post("/plan", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert len(data["thoughts"]) == 4
        assert len(data["actions"]) == 4
        assert len(data["observations"]) == 4
        assert data["destination"] == payload["destination"]
        assert data["travel_style"] == payload["travel_style"]
        assert data["total_cost"] > 0
        assert "hotel" in data["cost_breakdown"]
        assert "food" in data["cost_breakdown"]
        assert "transport" in data["cost_breakdown"]
        assert "activities" in data["cost_breakdown"]
        assert len(data["final_answer"]) > 100
