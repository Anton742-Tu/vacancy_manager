from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Salary:
    from_amount: Optional[int] = None
    to_amount: Optional[int] = None
    currency: str = "RUB"
    gross: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"from": self.from_amount, "to": self.to_amount, "currency": self.currency, "gross": self.gross}

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Salary"]:
        if not data:
            return None

        return cls(
            from_amount=data.get("from"),
            to_amount=data.get("to"),
            currency=data.get("currency", "RUB"),
            gross=data.get("gross"),
        )


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
    source: str = "hh.ru"

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
        salary = Salary.from_dict(salary_data) if salary_data else None

        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            company=str(data["company"]),
            salary=salary,
            area=str(data.get("area", "")),
            url=str(data.get("url", "")),
            published_at=str(data.get("published_at", "")),
            snippet=str(data.get("snippet", "")),
            experience=str(data.get("experience", "")),
            employment=str(data.get("employment", "")),
            source=str(data.get("source", "hh.ru")),
        )
