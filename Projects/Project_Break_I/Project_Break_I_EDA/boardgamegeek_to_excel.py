"""Convierte `data/boardgamegeek.json` a Excel con columnas planas.

Este script está pensado para el JSON local del proyecto, no para la API XML.
Extrae y normaliza la mayor cantidad posible de campos en estas columnas:

row_id, boardgame, release_year, min_players, max_players, min_playtime,
max_playtime, minimum_age, avg_rating, num_ratings, complexity, rank_overall,
item_type, owned, wishlisted, fans, page_views, amazon_price,
std_deviation, comments, previously_owned, for_trade, want_trade, rating_1,
rating_2, rating_3, rating_4, rating_5, rating_6, rating_7, rating_8,
rating_9, rating_10, categories, mechanics, families, designers, artists,
publishers, solo_designers, developers, graphic_designers, sculptors,
editors, writers, insert_designers, rank_strategy, rank_thematic,
rank_family, rank_war, rank_customizable, rank_abstract, rank_party,
rank_childrens, suggested_numplayers, url, description

Instalación:
    pip install pandas openpyxl

Uso:
    python boardgamegeek_to_excel.py --input data/boardgamegeek.json --output boardgamegeek.xlsx
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd


EXPECTED_COLUMNS = [
    "row_id",
    "boardgame",
    "release_year",
    "min_players",
    "max_players",
    "min_playtime",
    "max_playtime",
    "minimum_age",
    "avg_rating",
    "num_ratings",
    "complexity",
    "rank_overall",
    "item_type",
    "owned",
    "wishlisted",
    "fans",
    "page_views",
    "amazon_price",
    "std_deviation",
    "comments",
    "previously_owned",
    "for_trade",
    "want_trade",
    "rating_1",
    "rating_2",
    "rating_3",
    "rating_4",
    "rating_5",
    "rating_6",
    "rating_7",
    "rating_8",
    "rating_9",
    "rating_10",
    "categories",
    "mechanics",
    "families",
    "designers",
    "artists",
    "publishers",
    "solo_designers",
    "developers",
    "graphic_designers",
    "sculptors",
    "editors",
    "writers",
    "insert_designers",
    "rank_strategy",
    "rank_thematic",
    "rank_family",
    "rank_war",
    "rank_customizable",
    "rank_abstract",
    "rank_party",
    "rank_childrens",
    "suggested_numplayers",
    "url",
    "description",
]


def _join_list(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value if item is not None)
    if value is None:
        return ""
    return str(value)


def _first_market_price(entry: Dict[str, Any], store_name: str = "Amazon") -> Optional[float]:
    marketplace = entry.get("marketplace", [])
    if not isinstance(marketplace, list):
        return None

    for item in marketplace:
        if not isinstance(item, dict):
            continue
        if str(item.get("store", "")).strip().lower() == store_name.lower():
            price = item.get("base_price_usd", item.get("base_price"))
            try:
                return float(price)
            except (TypeError, ValueError):
                return None
    return None


def _rating_bucket_value(ratings: Dict[str, Any], rating_number: int) -> Any:
    return ratings.get(f"rating_{rating_number}", ratings.get(f"rated_{rating_number}"))


def _flatten_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    player_counts = entry.get("player_counts", {}) if isinstance(entry.get("player_counts"), dict) else {}
    playtime = entry.get("playtime", {}) if isinstance(entry.get("playtime"), dict) else {}
    game_info = entry.get("game_info", {}) if isinstance(entry.get("game_info"), dict) else {}
    credits = entry.get("credits", {}) if isinstance(entry.get("credits"), dict) else {}
    game_stats = entry.get("game_stats", {}) if isinstance(entry.get("game_stats"), dict) else {}
    ranks = entry.get("ranks", {}) if isinstance(entry.get("ranks"), dict) else {}
    collection_stats = entry.get("collection_stats", {}) if isinstance(entry.get("collection_stats"), dict) else {}
    ratings = entry.get("ratings", {}) if isinstance(entry.get("ratings"), dict) else {}
    item = entry.get("item", {}) if isinstance(entry.get("item"), dict) else {}
    suggested_numplayers = entry.get("suggested_numplayers", {}) if isinstance(entry.get("suggested_numplayers"), dict) else {}

    flattened = {
        "row_id": entry.get("row_id"),
        "boardgame": entry.get("boardgame", ""),
        "release_year": game_info.get("release_year"),
        "item_type": item.get("type") or entry.get("item_type"),
        "min_players": player_counts.get("min_players"),
        "max_players": player_counts.get("max_players"),
        "min_playtime": playtime.get("min_playtime"),
        "max_playtime": playtime.get("max_playtime"),
        "minimum_age": entry.get("minimum_age"),
        "avg_rating": game_stats.get("average_rating"),
        "num_ratings": game_stats.get("num_of_ratings"),
        "complexity": game_stats.get("weight"),
        "rank_overall": ranks.get("overall"),
        "owned": collection_stats.get("own"),
        "wishlisted": collection_stats.get("wishlist"),
        "fans": game_stats.get("fans"),
        "page_views": game_stats.get("page_views"),
        "amazon_price": _first_market_price(entry, "Amazon"),
        "std_deviation": game_stats.get("std_deviation"),
        "comments": game_stats.get("comments"),
        "previously_owned": collection_stats.get("previously_owned"),
        "for_trade": collection_stats.get("for_trade"),
        "want_trade": collection_stats.get("want_in_trade"),
        "rating_1": _rating_bucket_value(ratings, 1),
        "rating_2": _rating_bucket_value(ratings, 2),
        "rating_3": _rating_bucket_value(ratings, 3),
        "rating_4": _rating_bucket_value(ratings, 4),
        "rating_5": _rating_bucket_value(ratings, 5),
        "rating_6": _rating_bucket_value(ratings, 6),
        "rating_7": _rating_bucket_value(ratings, 7),
        "rating_8": _rating_bucket_value(ratings, 8),
        "rating_9": _rating_bucket_value(ratings, 9),
        "rating_10": _rating_bucket_value(ratings, 10),
        "categories": _join_list(game_info.get("categories")),
        "mechanics": _join_list(game_info.get("mechanisms")),
        "families": _join_list(game_info.get("family")),
        "designers": _join_list(credits.get("designers")),
        "artists": _join_list(credits.get("artists")),
        "publishers": _join_list(credits.get("publishers")),
        "solo_designers": credits.get("solo_designer"),
        "developers": credits.get("developer"),
        "graphic_designers": credits.get("graphic_designer"),
        "sculptors": credits.get("sculptor"),
        "editors": credits.get("editor"),
        "writers": credits.get("writer"),
        "insert_designers": credits.get("insert_designer"),
        "rank_strategy": ranks.get("strategy"),
        "rank_thematic": ranks.get("thematic"),
        "rank_family": ranks.get("family"),
        "rank_war": ranks.get("war"),
        "rank_customizable": ranks.get("customizable"),
        "rank_abstract": ranks.get("abstract"),
        "rank_party": ranks.get("party"),
        "rank_childrens": ranks.get("childrens"),
        "suggested_numplayers": json.dumps(suggested_numplayers, ensure_ascii=False) if suggested_numplayers else None,
        "url": entry.get("link_to_game", ""),
        "description": entry.get("description", ""),
    }

    for column in EXPECTED_COLUMNS:
        flattened.setdefault(column, None)

    return flattened


def load_json(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    raise ValueError("El JSON raíz debe ser una lista de juegos.")


def build_dataframe(items: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    rows = [_flatten_entry(item) for item in items]
    df = pd.DataFrame(rows)
    for column in EXPECTED_COLUMNS:
        if column not in df.columns:
            df[column] = None
    return df[EXPECTED_COLUMNS]


def save_excel(df: pd.DataFrame, output_path: Path) -> None:
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="BGG", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convierte boardgamegeek.json a Excel plano")
    parser.add_argument("--input", default="data/boardgamegeek.json", help="Ruta del JSON de entrada")
    parser.add_argument("--output", required=True, help="Ruta del Excel de salida")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    items = load_json(input_path)
    df = build_dataframe(items)
    save_excel(df, output_path)

    print(f"Exportado {len(df)} registros a {output_path}")
    print(f"Columnas: {len(df.columns)}")


if __name__ == "__main__":
    main()