from __future__ import annotations

from datetime import datetime
import unicodedata
from typing import Any, Dict, List


FOOD_COST_BY_STYLE = {
    "budget": 150_000,
    "standard": 300_000,
    "premium": 700_000,
}


DESTINATION_DB: Dict[str, Dict[str, Any]] = {
    "Hà Nội": {
        "region": "Miền Bắc",
        "hotel_cost": {"budget": 400_000, "standard": 800_000, "premium": 1_800_000},
        "transport_cost": 300_000,
        "activities": {
            "nature": [
                {"name": "Hồ Tây", "cost": 0, "tags": ["free"]},
                {"name": "Công viên Yên Sở", "cost": 0, "tags": ["free"]},
            ],
            "food": [
                {"name": "Phở Hà Nội", "cost": 70_000, "tags": ["local-food"]},
                {"name": "Bún chả", "cost": 80_000, "tags": ["local-food"]},
                {"name": "Food tour phố cổ", "cost": 350_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Văn Miếu", "cost": 70_000, "tags": ["museum"]},
                {"name": "Hoàng Thành Thăng Long", "cost": 100_000, "tags": ["history"]},
                {"name": "Bảo tàng Dân tộc học", "cost": 40_000, "tags": ["museum"]},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Dân tộc học", "cost": 40_000, "tags": ["museum"]},
                {"name": "Tràng Tiền Plaza", "cost": 0, "tags": ["free"]},
            ],
        },
    },
    "Sapa": {
        "region": "Miền Bắc",
        "hotel_cost": {"budget": 450_000, "standard": 900_000, "premium": 2_000_000},
        "transport_cost": 1_000_000,
        "activities": {
            "nature": [
                {"name": "Fansipan", "cost": 900_000, "tags": ["premium-experience"]},
                {"name": "Bản Cát Cát", "cost": 150_000, "tags": []},
                {"name": "Trekking Lao Chải", "cost": 250_000, "tags": []},
            ],
            "food": [
                {"name": "Thắng cố", "cost": 120_000, "tags": ["local-food"]},
                {"name": "Lẩu cá hồi", "cost": 350_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Chợ vùng cao", "cost": 0, "tags": ["free"]},
                {"name": "Bản người H'Mông", "cost": 120_000, "tags": []},
            ],
            "indoor_rainy": [
                {"name": "Cafe ngắm mây Sapa", "cost": 90_000, "tags": []},
                {"name": "Bảo tàng Sapa", "cost": 50_000, "tags": ["museum"]},
            ],
        },
    },
    "Hà Giang": {
        "region": "Miền Bắc",
        "hotel_cost": {"budget": 350_000, "standard": 700_000, "premium": 1_500_000},
        "transport_cost": 1_200_000,
        "activities": {
            "nature": [
                {"name": "Đèo Mã Pí Lèng", "cost": 0, "tags": ["free"]},
                {"name": "Sông Nho Quế", "cost": 200_000, "tags": []},
                {"name": "Cột cờ Lũng Cú", "cost": 50_000, "tags": []},
            ],
            "food": [
                {"name": "Thắng dền", "cost": 40_000, "tags": ["local-food"]},
                {"name": "Cháo ấu tẩu", "cost": 60_000, "tags": ["local-food"]},
            ],
            "culture": [
                {"name": "Phố cổ Đồng Văn", "cost": 0, "tags": ["free"]},
                {"name": "Dinh Vua Mèo", "cost": 30_000, "tags": ["history"]},
            ],
            "indoor_rainy": [
                {"name": "Cafe phố cổ Đồng Văn", "cost": 60_000, "tags": []},
                {"name": "Nhà văn hóa dân tộc", "cost": 40_000, "tags": ["museum"]},
            ],
        },
    },
    "Ninh Bình": {
        "region": "Miền Bắc",
        "hotel_cost": {"budget": 350_000, "standard": 700_000, "premium": 1_500_000},
        "transport_cost": 450_000,
        "activities": {
            "nature": [
                {"name": "Tràng An", "cost": 250_000, "tags": []},
                {"name": "Tam Cốc", "cost": 250_000, "tags": []},
                {"name": "Hang Múa", "cost": 100_000, "tags": []},
            ],
            "food": [
                {"name": "Cơm cháy dê núi", "cost": 180_000, "tags": ["local-food"]},
                {"name": "Ốc núi", "cost": 120_000, "tags": ["local-food"]},
            ],
            "culture": [
                {"name": "Cố đô Hoa Lư", "cost": 20_000, "tags": ["history"]},
                {"name": "Chùa Bái Đính", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Ninh Bình", "cost": 50_000, "tags": ["museum"]},
                {"name": "Cafe nhà vườn Tràng An", "cost": 80_000, "tags": []},
            ],
        },
    },
    "Quảng Ninh (Hạ Long)": {
        "region": "Miền Bắc",
        "hotel_cost": {"budget": 500_000, "standard": 1_000_000, "premium": 2_200_000},
        "transport_cost": 700_000,
        "activities": {
            "nature": [
                {"name": "Vịnh Hạ Long", "cost": 500_000, "tags": ["premium-experience"]},
                {"name": "Đảo Ti Tốp", "cost": 150_000, "tags": []},
                {"name": "Bãi Cháy", "cost": 0, "tags": ["free"]},
            ],
            "food": [
                {"name": "Chả mực Hạ Long", "cost": 150_000, "tags": ["local-food"]},
                {"name": "Hải sản Hạ Long", "cost": 350_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Bảo tàng Quảng Ninh", "cost": 40_000, "tags": ["museum"]},
                {"name": "Chợ Hạ Long", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Quảng Ninh", "cost": 40_000, "tags": ["museum"]},
                {"name": "Cafe view biển Bãi Cháy", "cost": 90_000, "tags": []},
            ],
        },
    },
    "Mộc Châu": {
        "region": "Miền Bắc",
        "hotel_cost": {"budget": 350_000, "standard": 650_000, "premium": 1_400_000},
        "transport_cost": 800_000,
        "activities": {
            "nature": [
                {"name": "Đồi chè trái tim", "cost": 30_000, "tags": []},
                {"name": "Thác Dải Yếm", "cost": 80_000, "tags": []},
                {"name": "Rừng thông Bản Áng", "cost": 60_000, "tags": []},
            ],
            "food": [
                {"name": "Bê chao", "cost": 150_000, "tags": ["local-food"]},
                {"name": "Sữa chua nếp cẩm", "cost": 50_000, "tags": ["local-food"]},
            ],
            "culture": [
                {"name": "Làng nguyên thủy", "cost": 70_000, "tags": []},
                {"name": "Bản người Thái", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Farm cafe Mộc Châu", "cost": 70_000, "tags": []},
                {"name": "Xưởng sữa Mộc Châu", "cost": 100_000, "tags": []},
            ],
        },
    },
    "Huế": {
        "region": "Miền Trung",
        "hotel_cost": {"budget": 350_000, "standard": 700_000, "premium": 1_600_000},
        "transport_cost": 450_000,
        "activities": {
            "nature": [
                {"name": "Đồi Vọng Cảnh", "cost": 0, "tags": ["free"]},
                {"name": "Biển Thuận An", "cost": 0, "tags": ["free"]},
            ],
            "food": [
                {"name": "Bún bò Huế", "cost": 60_000, "tags": ["local-food"]},
                {"name": "Cơm hến", "cost": 50_000, "tags": ["local-food"]},
                {"name": "Food tour Huế", "cost": 280_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Đại Nội", "cost": 200_000, "tags": ["history"]},
                {"name": "Lăng Minh Mạng", "cost": 150_000, "tags": ["history"]},
                {"name": "Chùa Thiên Mụ", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Cổ vật Cung đình Huế", "cost": 50_000, "tags": ["museum"]},
                {"name": "Cafe sân vườn Huế", "cost": 70_000, "tags": []},
            ],
        },
    },
    "Đà Nẵng": {
        "region": "Miền Trung",
        "hotel_cost": {"budget": 400_000, "standard": 800_000, "premium": 1_800_000},
        "transport_cost": 500_000,
        "activities": {
            "nature": [
                {"name": "Biển Mỹ Khê", "cost": 0, "tags": ["free"]},
                {"name": "Bán đảo Sơn Trà", "cost": 150_000, "tags": []},
                {"name": "Ngũ Hành Sơn", "cost": 80_000, "tags": []},
            ],
            "food": [
                {"name": "Mì Quảng", "cost": 60_000, "tags": ["local-food"]},
                {"name": "Bánh tráng cuốn thịt heo", "cost": 90_000, "tags": ["local-food"]},
                {"name": "Food tour hải sản", "cost": 250_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Bảo tàng Chăm", "cost": 60_000, "tags": ["museum"]},
                {"name": "Cầu Rồng", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Chăm", "cost": 60_000, "tags": ["museum"]},
                {"name": "Vincom Đà Nẵng", "cost": 0, "tags": ["free"]},
            ],
        },
    },
    "Hội An": {
        "region": "Miền Trung",
        "hotel_cost": {"budget": 450_000, "standard": 900_000, "premium": 2_000_000},
        "transport_cost": 450_000,
        "activities": {
            "nature": [
                {"name": "Biển An Bàng", "cost": 0, "tags": ["free"]},
                {"name": "Rừng dừa Bảy Mẫu", "cost": 180_000, "tags": []},
            ],
            "food": [
                {"name": "Cao lầu", "cost": 50_000, "tags": ["local-food"]},
                {"name": "Bánh mì Hội An", "cost": 35_000, "tags": ["local-food"]},
                {"name": "Food tour phố cổ", "cost": 250_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Phố cổ Hội An", "cost": 120_000, "tags": ["history"]},
                {"name": "Chùa Cầu", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Workshop làm đèn lồng", "cost": 180_000, "tags": []},
                {"name": "Bảo tàng Hội An", "cost": 40_000, "tags": ["museum"]},
            ],
        },
    },
    "Quy Nhơn": {
        "region": "Miền Trung",
        "hotel_cost": {"budget": 350_000, "standard": 750_000, "premium": 1_700_000},
        "transport_cost": 550_000,
        "activities": {
            "nature": [
                {"name": "Kỳ Co", "cost": 250_000, "tags": []},
                {"name": "Eo Gió", "cost": 50_000, "tags": []},
                {"name": "Hòn Khô", "cost": 250_000, "tags": []},
            ],
            "food": [
                {"name": "Bún chả cá Quy Nhơn", "cost": 45_000, "tags": ["local-food"]},
                {"name": "Hải sản đầm Thị Nại", "cost": 280_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Tháp Đôi", "cost": 20_000, "tags": ["history"]},
                {"name": "Ghềnh Ráng", "cost": 50_000, "tags": []},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Bình Định", "cost": 30_000, "tags": ["museum"]},
                {"name": "Cafe sách Quy Nhơn", "cost": 60_000, "tags": []},
            ],
        },
    },
    "Nha Trang": {
        "region": "Miền Trung",
        "hotel_cost": {"budget": 450_000, "standard": 900_000, "premium": 2_200_000},
        "transport_cost": 700_000,
        "activities": {
            "nature": [
                {"name": "VinWonders Nha Trang", "cost": 950_000, "tags": ["premium-experience"]},
                {"name": "Hòn Mun", "cost": 450_000, "tags": []},
                {"name": "Biển Trần Phú", "cost": 0, "tags": ["free"]},
            ],
            "food": [
                {"name": "Bún sứa", "cost": 50_000, "tags": ["local-food"]},
                {"name": "Nem nướng Nha Trang", "cost": 80_000, "tags": ["local-food"]},
            ],
            "culture": [
                {"name": "Tháp Bà Ponagar", "cost": 30_000, "tags": ["history"]},
                {"name": "Chùa Long Sơn", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Viện Hải dương học", "cost": 40_000, "tags": ["museum"]},
                {"name": "Tắm bùn khoáng", "cost": 350_000, "tags": ["premium-experience"]},
            ],
        },
    },
    "Phú Yên": {
        "region": "Miền Trung",
        "hotel_cost": {"budget": 350_000, "standard": 700_000, "premium": 1_500_000},
        "transport_cost": 650_000,
        "activities": {
            "nature": [
                {"name": "Gành Đá Đĩa", "cost": 30_000, "tags": []},
                {"name": "Bãi Xép", "cost": 20_000, "tags": []},
                {"name": "Mũi Điện", "cost": 40_000, "tags": []},
            ],
            "food": [
                {"name": "Mắt cá ngừ đại dương", "cost": 120_000, "tags": ["local-food"]},
                {"name": "Bánh hỏi lòng heo", "cost": 80_000, "tags": ["local-food"]},
            ],
            "culture": [
                {"name": "Nhà thờ Mằng Lăng", "cost": 0, "tags": ["free"]},
                {"name": "Tháp Nhạn", "cost": 20_000, "tags": ["history"]},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Phú Yên", "cost": 30_000, "tags": ["museum"]},
                {"name": "Cafe ven sông Đà Rằng", "cost": 70_000, "tags": []},
            ],
        },
    },
    "TP Hồ Chí Minh": {
        "region": "Miền Nam",
        "hotel_cost": {"budget": 450_000, "standard": 900_000, "premium": 2_200_000},
        "transport_cost": 400_000,
        "activities": {
            "nature": [
                {"name": "Thảo Cầm Viên", "cost": 60_000, "tags": []},
                {"name": "Công viên bờ sông Sài Gòn", "cost": 0, "tags": ["free"]},
            ],
            "food": [
                {"name": "Cơm tấm Sài Gòn", "cost": 60_000, "tags": ["local-food"]},
                {"name": "Hủ tiếu Nam Vang", "cost": 70_000, "tags": ["local-food"]},
                {"name": "Food tour quận 1", "cost": 350_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Dinh Độc Lập", "cost": 65_000, "tags": ["history"]},
                {"name": "Bảo tàng Chứng tích Chiến tranh", "cost": 40_000, "tags": ["museum"]},
                {"name": "Nhà thờ Đức Bà", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Takashimaya", "cost": 0, "tags": ["free"]},
                {"name": "Bảo tàng Mỹ thuật", "cost": 30_000, "tags": ["museum"]},
            ],
        },
    },
    "Vũng Tàu": {
        "region": "Miền Nam",
        "hotel_cost": {"budget": 400_000, "standard": 800_000, "premium": 1_700_000},
        "transport_cost": 350_000,
        "activities": {
            "nature": [
                {"name": "Bãi Sau", "cost": 0, "tags": ["free"]},
                {"name": "Hồ Mây", "cost": 400_000, "tags": ["premium-experience"]},
                {"name": "Mũi Nghinh Phong", "cost": 0, "tags": ["free"]},
            ],
            "food": [
                {"name": "Bánh khọt", "cost": 70_000, "tags": ["local-food"]},
                {"name": "Hải sản chợ Xóm Lưới", "cost": 250_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Tượng Chúa Kitô", "cost": 0, "tags": ["free"]},
                {"name": "Bạch Dinh", "cost": 40_000, "tags": ["history"]},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Vũ khí cổ", "cost": 70_000, "tags": ["museum"]},
                {"name": "Cafe biển trong nhà", "cost": 80_000, "tags": []},
            ],
        },
    },
    "Phú Quốc": {
        "region": "Miền Nam",
        "hotel_cost": {"budget": 700_000, "standard": 1_400_000, "premium": 3_000_000},
        "transport_cost": 1_500_000,
        "activities": {
            "nature": [
                {"name": "Bãi Sao", "cost": 0, "tags": ["free"]},
                {"name": "Hòn Thơm", "cost": 650_000, "tags": ["premium-experience"]},
                {"name": "Lặn ngắm san hô", "cost": 700_000, "tags": ["premium-experience"]},
            ],
            "food": [
                {"name": "Hải sản Phú Quốc", "cost": 350_000, "tags": ["premium-experience"]},
                {"name": "Bún quậy", "cost": 80_000, "tags": ["local-food"]},
            ],
            "culture": [
                {"name": "Nhà tù Phú Quốc", "cost": 40_000, "tags": ["history"]},
                {"name": "Chợ đêm Phú Quốc", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Grand World indoor show", "cost": 300_000, "tags": ["premium-experience"]},
                {"name": "Nhà thùng nước mắm", "cost": 30_000, "tags": []},
            ],
        },
    },
    "Cần Thơ": {
        "region": "Miền Nam",
        "hotel_cost": {"budget": 350_000, "standard": 700_000, "premium": 1_500_000},
        "transport_cost": 500_000,
        "activities": {
            "nature": [
                {"name": "Chợ nổi Cái Răng", "cost": 150_000, "tags": []},
                {"name": "Bến Ninh Kiều", "cost": 0, "tags": ["free"]},
                {"name": "Vườn trái cây Mỹ Khánh", "cost": 120_000, "tags": []},
            ],
            "food": [
                {"name": "Bánh xèo miền Tây", "cost": 90_000, "tags": ["local-food"]},
                {"name": "Lẩu mắm", "cost": 250_000, "tags": ["premium-experience"]},
            ],
            "culture": [
                {"name": "Nhà cổ Bình Thủy", "cost": 30_000, "tags": ["history"]},
                {"name": "Thiền viện Trúc Lâm Phương Nam", "cost": 0, "tags": ["free"]},
            ],
            "indoor_rainy": [
                {"name": "Bảo tàng Cần Thơ", "cost": 20_000, "tags": ["museum"]},
                {"name": "Cafe bến Ninh Kiều", "cost": 70_000, "tags": []},
            ],
        },
    },
    "Đà Lạt": {
        "region": "Miền Nam",
        "hotel_cost": {"budget": 350_000, "standard": 700_000, "premium": 1_500_000},
        "transport_cost": 500_000,
        "activities": {
            "nature": [
                {"name": "Hồ Xuân Hương", "cost": 0, "tags": ["free"]},
                {"name": "Langbiang", "cost": 300_000, "tags": []},
                {"name": "Cầu Đất", "cost": 120_000, "tags": []},
                {"name": "Thung lũng Tình Yêu", "cost": 250_000, "tags": []},
            ],
            "food": [
                {"name": "Bánh căn", "cost": 60_000, "tags": ["local-food"]},
                {"name": "Lẩu gà lá é", "cost": 250_000, "tags": ["premium-experience"]},
                {"name": "Chợ đêm Đà Lạt", "cost": 0, "tags": ["free"]},
            ],
            "culture": [
                {"name": "Dinh Bảo Đại", "cost": 80_000, "tags": ["history"]},
                {"name": "Ga Đà Lạt", "cost": 50_000, "tags": ["history"]},
            ],
            "indoor_rainy": [
                {"name": "Cafe ngắm mưa", "cost": 90_000, "tags": []},
                {"name": "Bảo tàng Lâm Đồng", "cost": 40_000, "tags": ["museum"]},
            ],
        },
    },
}


FALLBACK_DESTINATION = {
    "region": "Fallback",
    "hotel_cost": {"budget": 350_000, "standard": 700_000, "premium": 1_400_000},
    "transport_cost": 500_000,
    "activities": {
        "nature": [{"name": "Công viên trung tâm", "cost": 0, "tags": ["free"]}],
        "food": [{"name": "Quán ăn địa phương", "cost": 80_000, "tags": ["local-food"]}],
        "culture": [{"name": "Bảo tàng địa phương", "cost": 50_000, "tags": ["museum"]}],
        "indoor_rainy": [{"name": "Cafe trong nhà", "cost": 70_000, "tags": []}],
    },
}


WEATHER_OVERRIDES = {
    ("Đà Nẵng", "2026-06-15"): {
        "temperature": 32,
        "rain": False,
        "condition": "sunny",
        "description": "Trời nắng đẹp, phù hợp với biển và hoạt động ngoài trời.",
    },
    ("Đà Lạt", "2026-07-10"): {
        "temperature": 22,
        "rain": True,
        "condition": "rainy",
        "description": "Se lạnh và có mưa nhẹ, nên ưu tiên quán cafe, bảo tàng và các điểm trong nhà.",
    },
    ("Hà Nội", "2026-12-01"): {
        "temperature": 18,
        "rain": False,
        "condition": "cloudy",
        "description": "Trời mát, phù hợp tham quan văn hóa và ăn uống.",
    },
}


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value or "")
    stripped = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return stripped.replace("đ", "d").replace("Đ", "D").lower()


def _get_destination_record(destination: str) -> Dict[str, Any]:
    return DESTINATION_DB.get(destination, FALLBACK_DESTINATION)


def _flatten_activities(record: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    flattened: Dict[str, Dict[str, Any]] = {}
    for items in record["activities"].values():
        for item in items:
            flattened[item["name"]] = item
    return flattened


def get_weather(destination: str, date: str) -> Dict[str, Any]:
    if not destination or not date:
        raise ValueError("destination và date là bắt buộc.")

    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("date phải theo định dạng YYYY-MM-DD.") from exc

    override = WEATHER_OVERRIDES.get((destination, date))
    if override:
        return override

    rainy_months = {9, 10, 11}
    is_rainy = parsed_date.month in rainy_months
    has_known_destination = destination in DESTINATION_DB

    return {
        "temperature": 30 if not is_rainy else 25,
        "rain": is_rainy,
        "condition": "rainy" if is_rainy else "sunny",
        "description": (
            "Dữ liệu thời tiết đang được mock theo mùa cho điểm đến này."
            if has_known_destination
            else "Điểm đến chưa có trong knowledge base chi tiết, đang dùng dự báo mock mặc định."
        ),
    }


def recommend_activities(destination: str, weather: Dict[str, Any], preference: str, travel_style: str = "standard") -> List[Dict[str, Any]]:
    if not destination or weather is None:
        raise ValueError("destination và weather là bắt buộc.")

    record = _get_destination_record(destination)
    preference_text = _normalize_text(preference)
    selected: List[Dict[str, Any]] = []

    if weather.get("rain"):
        selected.extend(record["activities"]["indoor_rainy"])

    if "van hoa" in preference_text:
        selected.extend(record["activities"]["culture"])
    if "thien nhien" in preference_text or "nui" in preference_text or "trek" in preference_text or "bien" in preference_text:
        selected.extend(record["activities"]["nature"])
    if "an" in preference_text or "am thuc" in preference_text or "food" in preference_text:
        selected.extend(record["activities"]["food"])

    if not selected:
        selected.extend(record["activities"]["culture"])
        selected.extend(record["activities"]["food"])
        if not weather.get("rain"):
            selected.extend(record["activities"]["nature"])

    deduped: List[Dict[str, Any]] = []
    seen = set()
    for item in selected:
        if item["name"] not in seen:
            seen.add(item["name"])
            deduped.append(item)

    if travel_style == "budget":
        ranked = sorted(deduped, key=lambda item: (item["cost"] > 0, item["cost"]))
    elif travel_style == "premium":
        ranked = sorted(deduped, key=lambda item: item["cost"], reverse=True)
    else:
        ranked = sorted(deduped, key=lambda item: (item["cost"] == 0, item["cost"]))

    return ranked[:5]


def estimate_trip_cost(destination: str, days: int, activities: List[Dict[str, Any]], travel_style: str = "standard") -> Dict[str, Any]:
    if not destination or days <= 0:
        raise ValueError("destination và days hợp lệ là bắt buộc.")
    if travel_style not in FOOD_COST_BY_STYLE:
        raise ValueError("travel_style phải là budget, standard hoặc premium.")

    record = _get_destination_record(destination)
    hotel_cost = record["hotel_cost"][travel_style] * days
    food_cost = FOOD_COST_BY_STYLE[travel_style] * days
    transport_cost = record["transport_cost"]
    activity_cost = sum(activity.get("cost", 0) for activity in activities)

    breakdown = {
        "hotel": hotel_cost,
        "food": food_cost,
        "transport": transport_cost,
        "activities": activity_cost,
        "activity_items": {activity["name"]: activity.get("cost", 0) for activity in activities},
    }
    total_cost = hotel_cost + food_cost + transport_cost + activity_cost
    return {"total_cost": total_cost, "breakdown": breakdown}


def check_budget(total_cost: int, budget: int) -> Dict[str, Any]:
    if budget is None:
        raise ValueError("budget là bắt buộc.")
    within_budget = total_cost <= budget
    difference = abs(budget - total_cost)
    return {"within_budget": within_budget, "difference": difference}
