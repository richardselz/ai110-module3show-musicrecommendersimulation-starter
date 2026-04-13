"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

# Standard profiles
HIGH_ENERGY_POP = {
    "label": "High-Energy Pop",
    "genre": "pop",
    "mood": "happy",
    "energy": 0.9,
    "likes_acoustic": False,
}

CHILL_LOFI = {
    "label": "Chill Lofi",
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.35,
    "likes_acoustic": True,
}

DEEP_INTENSE_ROCK = {
    "label": "Deep Intense Rock",
    "genre": "rock",
    "mood": "intense",
    "energy": 0.95,
    "likes_acoustic": False,
}

# Adversarial / edge case profiles
GENRE_NOT_IN_CATALOG = {
    "label": "Adversarial: Genre Not in Catalog (country)",
    "genre": "country",
    "mood": "happy",
    "energy": 0.7,
    "likes_acoustic": False,
}

CONFLICTING_PREFS = {
    "label": "Adversarial: Conflicting Preferences (ambient + intense + high energy)",
    "genre": "ambient",
    "mood": "intense",
    "energy": 0.9,
    "likes_acoustic": False,
}

ALL_MID = {
    "label": "Adversarial: All Midrange (no strong preference)",
    "genre": "jazz",
    "mood": "focused",
    "energy": 0.5,
    "likes_acoustic": False,
}

PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    GENRE_NOT_IN_CATALOG,
    CONFLICTING_PREFS,
    ALL_MID,
]


def print_recommendations(label: str, recommendations: list) -> None:
    """Print a formatted recommendations block for a single user profile."""
    divider = "=" * 52
    print(f"\n{divider}")
    print(f"  PROFILE: {label}")
    print(f"  TOP {len(recommendations)} RECOMMENDATIONS")
    print(divider)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score: {round(score * 100)}")
        print(f"       Why:")
        for reason in explanation.split("; "):
            print(f"         - {reason}")

    print(f"\n{divider}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        user_prefs = {k: v for k, v in profile.items() if k != "label"}
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile["label"], recommendations)


if __name__ == "__main__":
    main()
