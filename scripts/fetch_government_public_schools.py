import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


SOURCE_URL = "https://dmdc.ngsp.gov.vn/WebPortal/Mining?CategoryId=908bd577-49a1-4dca-b0a5-c6d9a40ea7c8"
OUTPUT_FILE = Path("data/government-public-universities-colleges.json")


class TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        cleaned = " ".join(data.split())
        if cleaned:
            self.parts.append(cleaned)


def fetch_html(url: str) -> str:
    request = Request(url, headers={"User-Agent": "schools-api-data-import/1.0"})
    with urlopen(request, timeout=30) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(encoding, errors="replace")


def strip_accents(value: str) -> str:
    value = value.replace("Đ", "D").replace("đ", "d")
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def slugify(value: str) -> str:
    value = strip_accents(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def school_kind(code: str, name: str) -> str:
    if code.startswith("CĐ") or "CAO ĐẲNG" in name:
        return "college"
    if "HỌC VIỆN" in name:
        return "academy"
    if name.startswith("KHOA "):
        return "faculty"
    return "university"


def build_school(record: tuple[str, str], source_url: str) -> dict:
    code, name = record
    today = date.today().isoformat()
    kind = school_kind(code, name)
    return {
        "id": slugify(code),
        "code": code,
        "name": name,
        "logo_url": None,
        "description": (
            f"{name} trong Danh mục mã các trường đại học, cao đẳng công lập "
            "của Hệ thống danh mục điện tử dùng chung của các cơ quan nhà nước."
        ),
        "type": "public",
        "country": "VN",
        "contact": {
            "website": None,
            "email": None,
            "phone": None,
        },
        "campuses": [
            {
                "name": "Cơ sở chính",
                "address": "Việt Nam",
                "is_main": True,
            }
        ],
        "faculties": [],
        "metadata": {
            "verified": True,
            "created_at": today,
            "updated_at": today,
            "source_url": source_url,
            "source_name": "Hệ thống danh mục điện tử dùng chung của các cơ quan nhà nước",
            "source_category": "Danh mục mã các trường đại học, cao đẳng công lập",
            "institution_kind": kind,
        },
    }


def parse_records(html: str) -> list[tuple[str, str]]:
    parser = TextParser()
    parser.feed(html)
    text = "\n".join(parser.parts)
    pattern = re.compile(r"^\s*\d+\s+((?:ĐH|CĐ)\.[^\s]+)\s+(.+?)\s*$", re.MULTILINE)

    records: dict[str, str] = {}
    for code, name in pattern.findall(text):
        if name in {"Tên trường Thao tác", "Tên trường"}:
            continue
        records.setdefault(code, name.strip())
    return sorted(records.items(), key=lambda item: slugify(item[0]))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch public university and college codes from the government shared catalog."
    )
    parser.add_argument("--source", default=SOURCE_URL)
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE)
    args = parser.parse_args()

    records = parse_records(fetch_html(args.source))
    if not records:
        print("No school records found in source page.", file=sys.stderr)
        return 1

    schools = [build_school(record, args.source) for record in records]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps({"schools": schools}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(schools)} schools to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
