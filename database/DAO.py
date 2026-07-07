from database.DB_connect import DBConnect
from model.Artista import Artista


class DAO:

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select a.ArtistId as ArtistId, a.Name as Name, group_concat(t.TrackId, " " ) as tracce, group_concat(p2.PlaylistId, "" ) as playlist
                from artist a
                join album al on al.ArtistId = a.ArtistId 
                join track t on t.AlbumId = al.AlbumId 
                join playlisttrack p on p.TrackId = t.TrackId 
                join playlist p2 on p2.PlaylistId = p.PlaylistId 
                group by ArtistId, Name 
                having count(*)>1
                """

        cursor.execute(query)

        for row in cursor:
            track_str = row.pop("tracce")
            row["tracce"] = track_str.split(" ") if track_str else []
            playlist_str = row.pop("playlist")
            row["playlist"] = track_str.split(" ") if playlist_str else []
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select a.ArtistId as A1, a2.ArtistId as A2, count(pl.PlaylistId ) as peso
                    from artist a
                    join album al on al.ArtistId = a.ArtistId 
                    join track t on t.AlbumId = al.AlbumId 
                    join playlisttrack p on p.TrackId = t.TrackId 
                    join playlist pl on pl.PlaylistId = p.PlaylistId 
                    join playlisttrack p2 on p2.PlaylistId = p.PlaylistId 
                    join track t2 on t2.TrackId = p2.TrackId 
                    join album al2 on al2.AlbumId = t2.AlbumId 
                    join artist a2 on al2.ArtistId = a2.ArtistId
                    where a.ArtistId < a2.ArtistId
                    group by a.ArtistId , a2.ArtistId

                    """

        cursor.execute(query)

        for row in cursor:
            results.append((row["A1"], row["A2"], row["peso"]))

        cursor.close()
        conn.close()
        return results

