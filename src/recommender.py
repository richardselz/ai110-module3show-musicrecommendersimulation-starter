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
    """
    Loads songs from a CSV file and returns them as a list of dicts.
    Required by src/main.py

    Numeric fields are cast to their appropriate types:
      - id         → int
      - tempo_bpm  → int
      - energy, valence, danceability, acousticness → float
    """
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
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Scoring weights:
      - Genre match      40%  (binary: full 0.40 or nothing)
      - Mood match       25%  (binary: full 0.25 or nothing)
      - Energy proximity 20%  (1 - abs(song.energy - target_energy)) * 0.20
      - Acousticness fit 15%  (song.acousticness if likes_acoustic else 1 - song.acousticness) * 0.15

    Returns: (total_score, reasons)
      - total_score: float in [0.0, 1.0]
      - reasons: list of strings describing each signal that contributed
    """
    score = 0.0
    reasons = []

    # Genre match — 40% weight
    if song["genre"] == user_prefs.get("genre", ""):
        contribution = 0.40
        score += contribution
        reasons.append(f"genre match (+{contribution:.2f})")

    # Mood match — 25% weight
    if song["mood"] == user_prefs.get("mood", ""):
        contribution = 0.25
        score += contribution
        reasons.append(f"mood match (+{contribution:.2f})")

    # Energy proximity — 20% weight
    target_energy = user_prefs.get("energy", 0.5)
    energy_contribution = (1.0 - abs(song["energy"] - target_energy)) * 0.20
    score += energy_contribution
    reasons.append(f"energy proximity (+{energy_contribution:.2f})")

    # Acousticness fit — 15% weight
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acoustic_raw = song["acousticness"] if likes_acoustic else (1.0 - song["acousticness"])
    acoustic_contribution = acoustic_raw * 0.15
    score += acoustic_contribution
    reasons.append(f"acousticness fit (+{acoustic_contribution:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
