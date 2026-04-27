import random
import requests
from .parser import parse_prompt
from .catalog import ANIME_CATALOG


class AnimeRecommender:

    def recommend(self, prompt, top_n=6):
        parsed = parse_prompt(prompt)

        # 1. Catalog (main source)
        catalog_results = self.search_catalog(prompt, parsed)

        # 2. Jikan backup (for classics)
        jikan_results = self.search_jikan(prompt)

        new_gen = []
        old_gen = []

        # Split catalog
        for anime in catalog_results:
            if anime.get("year", 2020) >= 2018:
                new_gen.append(anime)
            else:
                old_gen.append(anime)

        # Add Jikan classics ONLY
        for anime in jikan_results:
            if anime.get("year", 2000) < 2018:
                old_gen.append(anime)

        # Remove duplicates
        new_gen = self.dedupe(new_gen)
        old_gen = self.dedupe(old_gen)

        return parsed, {
            "new_gen": new_gen[:top_n],
            "old_gen": old_gen[:top_n]
        }


    # CATALOG SEARCH (PRIMARY)
    def search_catalog(self, prompt, parsed):
        results = []
        prompt_lower = prompt.lower()

        for anime in ANIME_CATALOG:
            genres = [g.lower() for g in anime.get("genres", [])]
            moods = [m.lower() for m in anime.get("moods", [])]

            score = anime.get("rating", 8.0)
            reasons = []

            # GENRE MATCH
            for pref in parsed.get("include", []):
                if pref in genres:
                    score += 5
                    reasons.append(f"{pref} match")

            # SPORTS FIX
            if "sports" in prompt_lower and "sports" in genres:
                score += 8
                reasons.append("sports anime")

            # TITLE MATCH
            if anime["title"].lower() in prompt_lower:
                score += 6
                reasons.append("title match")

            # FILTER OUT IRRELEVANT GENRES
            if parsed.get("include"):
                if not any(pref in genres for pref in parsed["include"]):
                    continue

            results.append({
                "title": anime["title"],
                "description": anime.get("description", "Curated anime recommendation."),
                "genres": genres,
                "rating": anime.get("rating", 8.0),
                "year": anime.get("year", 2020),
                "score": round(score + random.uniform(0, 1), 2),
                "reason": ", ".join(reasons) if reasons else "catalog match"
            })

        return sorted(results, key=lambda x: x["score"], reverse=True)


    # JIKAN BACKUP (CLASSICS ONLY)
    def search_jikan(self, prompt):
        results = []

        try:
            # 🔥 SEARCH RELATED
            search_url = "https://api.jikan.moe/v4/anime"
            search_params = {"q": prompt, "limit": 20}

            search_res = requests.get(search_url, params=search_params, timeout=10).json()

            for item in search_res.get("data", []):
                if item.get("type") not in ["TV", "ONA"]:
                    continue

                year = item.get("year") or 2005

                if year < 2018:
                    results.append({
                        "title": item.get("title"),
                        "description": item.get("synopsis") or "Classic anime.",
                        "genres": [g["name"].lower() for g in item.get("genres", [])],
                        "rating": item.get("score") or 7.5,
                        "year": year,
                        "score": item.get("score") or 7.5,
                        "reason": "classic match (search)"
                    })

            # TOP ANIME (guarantees classics exist)
            top_url = "https://api.jikan.moe/v4/top/anime"
            top_params = {"limit": 20}

            top_res = requests.get(top_url, params=top_params, timeout=10).json()

            for item in top_res.get("data", []):
                if item.get("type") not in ["TV", "ONA"]:
                    continue

                year = item.get("year") or 2005

                if year < 2018:
                    results.append({
                        "title": item.get("title"),
                        "description": item.get("synopsis") or "Top classic anime.",
                        "genres": [g["name"].lower() for g in item.get("genres", [])],
                        "rating": item.get("score") or 8.0,
                        "year": year,
                        "score": item.get("score") or 8.0,
                        "reason": "top classic anime"
                    })

            return results

        except Exception as e:
            print("JIKAN ERROR:", e)
            return []


    # REMOVE DUPLICATES
    def dedupe(self, anime_list):
        seen = set()
        result = []

        for anime in anime_list:
            title = anime["title"]

            if title not in seen:
                seen.add(title)
                result.append(anime)

        return result