from dataclasses import dataclass

@dataclass
class Artista:
    ArtistId: int
    Name: str
    tracce: list
    playlist: list

    def __hash__(self):
        return hash(self.ArtistId)
    def __eq__(self, other):
        return self.ArtistId==other.ArtistId
    def __str__(self):
        return f"{self.Name}"

