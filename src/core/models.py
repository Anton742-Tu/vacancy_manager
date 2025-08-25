from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Salary:
    from_amount: Optional[int] = None
    to_amount: Optional[int] = None
    currency: str = "RUB"
    gross: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"from": self.from_amount, "to": self.to_amount, "currency": self.currency, "gross": self.gross}


@dataclass
class Vacancy:
    id: str
    name: str
    company: str
    salary: Optional[Salary] = None
    area: str = ""
    url: str = ""
    published_at: str = ""
    snippet: str = ""
    experience: str = ""
    employment: str = ""
    source: str = "hh.ru"  # или "manual"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "salary": self.salary.to_dict() if self.salary else None,
            "area": self.area,
            "url": self.url,
            "published_at": self.published_at,
            "snippet": self.snippet,
            "experience": self.experience,
            "employment": self.employment,
            "source": self.source,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        salary_data = data.get("salary")
        salary = None
        if salary_data:
            salary = Salary(
                from_amount=salary_data.get("from"),
                to_amount=salary_data.get("to"),
                currency=salary_data.get("currency", "RUB"),
                gross=salary_data.get("gross"),
            )

        return cls(
            id=data["id"],
            name=data["name"],
            company=data["company"],
            salary=salary,
            area=data.get("area", ""),
            url=data.get("url", ""),
            published_at=data.get("published_at", ""),
            snippet=data.get("snippet", ""),
            experience=data.get("experience", ""),
            employment=data.get("employment", ""),
            source=data.get("source", "hh.ru"),
        )
