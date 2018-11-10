import sys
from nba_py import player
from nba_py.constants import CURRENT_SEASON, League


def get_fantasy_points_by_player(player_first_name, player_last_name):
    print("Loading ...")
    player_stats = None

    try:
        player_id = player.get_player(player_first_name, player_last_name, CURRENT_SEASON, 0, True)
        player_stats = player.PlayerYearOverYearSplits(player_id, 0, "Base", "PerGame", "N", "N", "N", League.Default,
                                                       CURRENT_SEASON, 'Regular Season', "0", "", "", "0", "", '', '', '0',
                                                       '', '', '', '0', '', '0').overall()[0]
    except StopIteration:
        print("Player not found")
        exit()

    fgm = player_stats["FGM"]
    fgmi = -0.5 * (player_stats["FGA"] - player_stats["FGM"])
    ftm = player_stats["FTM"]
    ftmi = -0.5 * (player_stats["FTA"] - player_stats["FTM"])
    fg3m = player_stats["FG3M"]
    reb = player_stats["REB"]
    ast = player_stats["AST"]
    stl = player_stats["STL"]
    blk = player_stats["BLK"]
    to = -0.25 * (player_stats["TOV"])
    pts = player_stats["PTS"]

    fantasy_points = round(fgm + fgmi + ftm + ftmi + fg3m + reb + ast + stl + blk + to + pts, 1)
    print(fantasy_points)

    return fantasy_points


if __name__ == '__main__':
    PlayerFirstName = sys.argv[1]
    PlayerLastName = sys.argv[2]
    get_fantasy_points_by_player(PlayerFirstName, PlayerLastName)
