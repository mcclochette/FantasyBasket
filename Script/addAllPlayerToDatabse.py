from config import config
import psycopg2
from getFantasyPointsByPlayer import get_fantasy_points_by_player
from nba_py import player
from nba_py.constants import League, CURRENT_SEASON
from pprint import pprint
from time import sleep


def add_player_to_database(player_name, owner_id, position1, position2, current_team_abbr):

    print("Loading : Adding Player " + player_name + " to database")
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()

        # execute a statement
        cur.execute("""
                    INSERT INTO Player
                    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT ON CONSTRAINT noPlayerDuplicate 
                    DO NOTHING
                    """,
                    (player_name, owner_id, position1, position2,
                     get_fantasy_points_by_player(player_name.split(" ")[0],
                                                  # For multiple last names
                                                  " ".join(str(names) for names in player_name.split(" ")[1:])),
                     current_team_abbr))

        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def insert_all_players():
    playerFromList = player.PlayerList(League.NBA, CURRENT_SEASON, 1).info()
    for nba_player in playerFromList:
        add_player_to_database(nba_player['DISPLAY_FIRST_LAST'], None, None, None, nba_player['TEAM_ABBREVIATION'])
        sleep(1)


if __name__ == '__main__':
    insert_all_players()
