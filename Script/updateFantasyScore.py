from config import config
import psycopg2
from getFantasyPointsByPlayer import get_fantasy_points_by_player
from nba_py import player
from nba_py.constants import League, CURRENT_SEASON


def update_fantasy_score(player_name):
    print("Loading : Updating Player " + player_name + " Fantasy Score")
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()

        # execute a statement
        cur.execute("""
                    UPDATE Player
                    SET fantasypoints = %s
                    WHERE playername = %s
                    """,
                    (get_fantasy_points_by_player(player_name.split(" ")[0],
                                                  # For multiple last names
                                                  " ".join(str(names) for names in player_name.split(" ")[1:])),
                     player_name))

        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def update_all_player_fantasy_score():
    player_from_list = player.PlayerList(League.NBA, CURRENT_SEASON, 1).info()
    for nba_player in player_from_list:
        update_fantasy_score(nba_player['DISPLAY_FIRST_LAST'])


if __name__ == '__main__':
    update_all_player_fantasy_score()
