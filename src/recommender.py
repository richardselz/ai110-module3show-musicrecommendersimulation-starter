from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a songs CSV and return a list of dicts with numeric fields cast to int or float."""
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["tempo_bpm"] = int(float(row["tempo_bpm"]))
            row["energy"] = float(row["energy"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences using weighted genre, mood, energy, and acousticness signals."""
    score = 0.0
    reasons = []

    # Genre match — 40% weight
    if song["genre"] == user_prefs.get("genre", ""):
        contribution = 0.40
        score += contribution
        reasons.append(f"genre match (100% match → +{contribution * 100:.1f}% of score)")

    # Mood match — 25% weight
    if song["mood"] == user_prefs.get("mood", ""):
        contribution = 0.25
        score += contribution
        reasons.append(f"mood match (100% match → +{contribution * 100:.1f}% of score)")

    # Energy proximity — 20% weight
    target_energy = user_prefs.get("energy", 0.5)
    energy_raw = 1.0 - abs(song["energy"] - target_energy)
    energy_contribution = energy_raw * 0.20
    score += energy_contribution
    reasons.append(f"energy proximity ({energy_raw * 100:.1f}% match → +{energy_contribution * 100:.1f}% of score)")

    # Acousticness fit — 15% weight
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acoustic_raw = song["acousticness"] if likes_acoustic else (1.0 - song["acousticness"])
    acoustic_contribution = acoustic_raw * 0.15
    score += acoustic_contribution
    reasons.append(f"acousticness fit ({acoustic_raw * 100:.1f}% match → +{acoustic_contribution * 100:.1f}% of score)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank highest to lowest, and return the top k as (song, score, explanation) tuples."""
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [
        (song, score, "; ".join(reasons))
        for song, score, reasons in ranked[:k]
    ]
