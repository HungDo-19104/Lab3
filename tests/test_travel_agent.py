from fastapi.testclient import TestClient

from src.agent.travel_agent import TravelChatbot, TravelPlanningAgent, TravelRequest
from src.app import app
from src.tools.travel_tools import check_budget, estimate_trip_cost, get_weather, recommend_activities


client = TestClient(app)


def test_agent_uses_all_four_tools_for_da_lat():
    agent = TravelPlanningAgent()
    result = agent.plan_trip(
        TravelRequest(
            destination="Đà Lạt",
            date="2026-06-15",
            preference="thiên nhiên",
            days=4,
            budget=2_000_000,
            travel_style="budget",
        )
    )

    assert len(result["trace"]) == 4
    assert result["trace"][0]["action"] == "get_weather"
    assert result["trace"][1]["action"] == "recommend_activities"
    assert result["trace"][2]["action"] == "estimate_trip_cost"
    assert result["trace"][3]["action"] == "check_budget"


def test_chatbot_never_uses_tools():
    chatbot = TravelChatbot()
    result = chatbot.respond(
        TravelRequest(
            destination="Đà Lạt",
            date="2026-06-15",
            preference="thiên nhiên",
            days=4,
            budget=2_000_000,
            travel_style="budget",
        )
    )

    assert result["uses_tools"] is False
    assert result["method"] == "Direct LLM response"


def test_compare_endpoint_returns_chatbot_and_agent_difference():
    response = client.post(
        "/compare",
        json={
            "destination": "Đà Lạt",
            "date": "2026-06-15",
            "preference": "thiên nhiên",
            "days": 4,
            "budget": 2_000_000,
            "travel_style": "budget",
        },
    )

    data = response.json()
    assert response.status_code == 200
    assert data["chatbot"]["uses_tools"] is False
    assert data["agent"]["uses_tools"] is True
    assert len(data["agent"]["trace"]) == 4
    assert len(data["comparison"]) >= 8
    assert data["chatbot"]["final_answer"] != data["agent"]["final_answer"]


def test_plan_endpoint_still_available():
    response = client.post(
        "/plan",
        json={
            "destination": "Phú Quốc",
            "date": "2026-08-20",
            "preference": "biển và ăn uống",
            "days": 4,
            "budget": 12_000_000,
            "travel_style": "standard",
        },
    )

    data = response.json()
    assert response.status_code == 200
    assert data["uses_tools"] is True
    assert "cost_breakdown" in data


def test_homepage_renders_compare_button():
    response = client.get("/")
    assert response.status_code == 200
    assert "Compare Chatbot vs Agent" in response.text
