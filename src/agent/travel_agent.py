from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List

from src.telemetry.logger import logger
from src.tools.travel_tools import check_budget, estimate_trip_cost, get_weather, recommend_activities


@dataclass
class TravelRequest:
    destination: str
    date: str
    preference: str
    days: int
    budget: int
    travel_style: str


@dataclass
class TraceStep:
    thought: str
    action: str
    observation: Any


class TravelPlanningAgent:
    def __init__(self) -> None:
        self.tools = [
            {"name": "get_weather", "function": get_weather},
            {"name": "recommend_activities", "function": recommend_activities},
            {"name": "estimate_trip_cost", "function": estimate_trip_cost},
            {"name": "check_budget", "function": check_budget},
        ]

    def plan_trip(self, request: TravelRequest) -> Dict[str, Any]:
        self._validate_request(request)
        logger.log_event("AGENT_START", {"request": request.__dict__})

        steps: List[TraceStep] = []

        weather = self._call_tool(
            steps,
            thought=f"Cần kiểm tra thời tiết tại {request.destination} vào ngày {request.date} trước khi lên lịch trình.",
            tool_name="get_weather",
            arguments={"destination": request.destination, "date": request.date},
        )

        activity_thought = self._build_activity_thought(weather, request.preference, request.travel_style, request.budget)
        activities = self._call_tool(
            steps,
            thought=activity_thought,
            tool_name="recommend_activities",
            arguments={
                "destination": request.destination,
                "weather": weather,
                "preference": request.preference,
                "travel_style": request.travel_style,
            },
        )

        trip_cost = self._call_tool(
            steps,
            thought=(
                f"Đã có hoạt động phù hợp cho {request.days} ngày, giờ cần tính chi phí khách sạn, ăn uống, "
                f"di chuyển và vé hoạt động theo travel style {request.travel_style}."
            ),
            tool_name="estimate_trip_cost",
            arguments={
                "destination": request.destination,
                "days": request.days,
                "activities": activities,
                "travel_style": request.travel_style,
            },
        )

        budget_result = self._call_tool(
            steps,
            thought=f"Cần đối chiếu tổng chi phí {trip_cost['total_cost']:,}đ với ngân sách {request.budget:,}đ để xem kế hoạch có phù hợp không.",
            tool_name="check_budget",
            arguments={"total_cost": trip_cost["total_cost"], "budget": request.budget},
        )

        final_answer = self._build_final_answer(request, weather, activities, trip_cost, budget_result)
        logger.log_event(
            "AGENT_END",
            {
                "destination": request.destination,
                "travel_style": request.travel_style,
                "total_cost": trip_cost["total_cost"],
                "within_budget": budget_result["within_budget"],
            },
        )

        return {
            "thoughts": [step.thought for step in steps],
            "actions": [step.action for step in steps],
            "observations": [step.observation for step in steps],
            "final_answer": final_answer,
            "total_cost": trip_cost["total_cost"],
            "within_budget": budget_result["within_budget"],
            "difference": budget_result["difference"],
            "destination": request.destination,
            "travel_style": request.travel_style,
            "weather": weather,
            "recommended_activities": activities,
            "cost_breakdown": trip_cost["breakdown"],
            "travel_advice": self._build_advice(request, trip_cost, budget_result),
        }

    def _call_tool(self, steps: List[TraceStep], thought: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        action = f"{tool_name}({json.dumps(arguments, ensure_ascii=False)})"
        logger.info(f"Thought: {thought}")
        logger.info(f"Action: {action}")
        tool_function = self._get_tool(tool_name)
        observation = tool_function(**arguments)
        logger.info(f"Observation: {json.dumps(observation, ensure_ascii=False)}")
        logger.log_event("TOOL_EXECUTION", {"tool": tool_name, "arguments": arguments, "observation": observation})
        steps.append(TraceStep(thought=thought, action=action, observation=observation))
        return observation

    def _get_tool(self, tool_name: str):
        for tool in self.tools:
            if tool["name"] == tool_name:
                return tool["function"]
        raise ValueError(f"Tool {tool_name} not found.")

    @staticmethod
    def _validate_request(request: TravelRequest) -> None:
        missing = []
        if not request.destination:
            missing.append("destination")
        if not request.date:
            missing.append("date")
        if request.budget is None:
            missing.append("budget")
        if missing:
            raise ValueError(f"Thiếu thông tin bắt buộc: {', '.join(missing)}")
        if request.days <= 0:
            raise ValueError("days phải lớn hơn 0.")
        if request.travel_style not in {"budget", "standard", "premium"}:
            raise ValueError("travel_style phải là budget, standard hoặc premium.")

    @staticmethod
    def _build_activity_thought(weather: Dict[str, Any], preference: str, travel_style: str, budget: int) -> str:
        weather_hint = "Trời mưa nên cần ưu tiên hoạt động trong nhà." if weather.get("rain") else "Thời tiết ổn nên có thể kết hợp hoạt động ngoài trời."
        budget_hint = (
            "Ngân sách thấp nên ưu tiên hoạt động miễn phí hoặc chi phí nhẹ."
            if travel_style == "budget"
            else "Ngân sách tốt nên có thể cân nhắc thêm trải nghiệm trả phí nổi bật."
            if travel_style == "premium"
            else "Cần cân bằng giữa trải nghiệm và chi phí."
        )
        return f"{weather_hint} Người dùng thích '{preference}'. {budget_hint} Mục tiêu là giữ kế hoạch trong khoảng ngân sách {budget:,}đ."

    @staticmethod
    def _translate_condition(condition: str) -> str:
        return {"sunny": "nắng đẹp", "rainy": "mưa", "cloudy": "nhiều mây"}.get(condition, condition)

    @staticmethod
    def _build_advice(request: TravelRequest, trip_cost: Dict[str, Any], budget_result: Dict[str, Any]) -> str:
        if budget_result["within_budget"]:
            if request.travel_style == "budget":
                return "Kế hoạch hiện khá an toàn với ngân sách. Bạn có thể giữ ưu tiên hoạt động miễn phí và món ăn địa phương."
            if request.travel_style == "premium":
                return "Ngân sách vẫn đủ tốt. Bạn có thể nâng cấp thêm một trải nghiệm cao cấp hoặc khách sạn đẹp hơn nếu muốn."
            return "Kế hoạch đang cân bằng tốt giữa chi phí và trải nghiệm."
        return (
            "Chi phí đang vượt ngân sách. Nên giảm số hoạt động trả phí, hạ hạng khách sạn "
            "hoặc chuyển sang travel style budget để tối ưu hơn."
        )

    def _build_final_answer(
        self,
        request: TravelRequest,
        weather: Dict[str, Any],
        activities: List[Dict[str, Any]],
        trip_cost: Dict[str, Any],
        budget_result: Dict[str, Any],
    ) -> str:
        activity_names = ", ".join(activity["name"] for activity in activities)
        breakdown = trip_cost["breakdown"]
        budget_line = (
            f"Phù hợp ngân sách, còn dư khoảng {budget_result['difference']:,}đ."
            if budget_result["within_budget"]
            else f"Đang vượt ngân sách khoảng {budget_result['difference']:,}đ."
        )
        advice = self._build_advice(request, trip_cost, budget_result)
        return (
            f"Điểm đến: {request.destination}. "
            f"Thời tiết: {self._translate_condition(weather['condition'])}, khoảng {weather['temperature']}°C. {weather['description']} "
            f"Hoạt động gợi ý: {activity_names}. "
            f"Chi phí dự kiến gồm khách sạn {breakdown['hotel']:,}đ, ăn uống {breakdown['food']:,}đ, "
            f"di chuyển {breakdown['transport']:,}đ, hoạt động {breakdown['activities']:,}đ. "
            f"Tổng chi phí: {trip_cost['total_cost']:,}đ. {budget_line} "
            f"Lời khuyên: {advice}"
        )
