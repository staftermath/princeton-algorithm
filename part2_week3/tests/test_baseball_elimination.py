import pytest
import os


TEST_NAME = "princeton_algoritm_part2_week3_baseball_elimination"


@pytest.fixture()
def tmp_folder(tmpdir):
    if not tmpdir.join(TEST_NAME).exists():
        tmpdir.mkdir(TEST_NAME)
    return tmpdir.join(TEST_NAME)


@pytest.fixture()
def resources():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")


@pytest.fixture()
def team4(resources):
    from part2_week3.baseball_elimination import BaseballElimination
    path = os.path.join(resources, "teams4.txt")
    baseball = BaseballElimination(path)
    return baseball


@pytest.fixture()
def team5(resources):
    from part2_week3.baseball_elimination import BaseballElimination
    path = os.path.join(resources, "teams5.txt")
    baseball = BaseballElimination(path)
    return baseball


@pytest.mark.parametrize(("teams", "expected_game_left"),
                         [
                             (("Atlanta", "New_York"), 6),
                             (("New_York", "Montreal"), 0),
                             (("Philadelphia", "Atlanta"), 1)
                         ])
def test_baseball_elimination_against(team4, teams, expected_game_left):
    assert expected_game_left == team4.against(*teams)


@pytest.mark.parametrize(("team", "expected_wins"),
                         [
                             ("Atlanta", 83),
                             ("Philadelphia", 80),
                             ("New_York", 78),
                             ("Montreal", 77)
                         ])
def test_baseball_elimination_wins(team4, team, expected_wins):
    assert expected_wins == team4.wins(team)


@pytest.mark.parametrize(("team", "expected_losses"),
                         [
                             ("Atlanta", 71),
                             ("Philadelphia", 79),
                             ("New_York", 78),
                             ("Montreal", 82)
                         ])
def test_baseball_elimination_losses(team4, team, expected_losses):
    assert expected_losses == team4.losses(team)


def test_baseball_elimination_team_total(team4):
    assert ["Atlanta", "Montreal", "New_York", "Philadelphia"] == sorted(team4.teams())
    assert 4 == team4.numberOfTeams()


@pytest.mark.parametrize(("team", "expected_eliminated", "expected_eliminated_by"),
                         [
                             ("Atlanta", False, None),
                             ("Philadelphia", True, ["Atlanta", "New_York"]),
                             ("New_York", False, None),
                             ("Montreal", True, ["Atlanta"])
                         ])
def test_baseball_elimination_is_eliminated_team4(team4, team, expected_eliminated, expected_eliminated_by):
    assert team4.isEliminated(team) == expected_eliminated
    eliminated_by = team4.certificateOfElimination(team)
    assert (
            (eliminated_by is None and expected_eliminated_by is None) or
            sorted(team4.certificateOfElimination(team)) == sorted(expected_eliminated_by)
    )


@pytest.mark.parametrize(("team", "expected_eliminated", "expected_eliminated_by"),
                         [
                             ("New_York", False, None),
                             ("Baltimore", False, None),
                             ("Boston", False, None),
                             ("Toronto", False, None),
                             ("Detroit", True, ["New_York", "Baltimore", "Boston", "Toronto"])
                         ])
def test_baseball_elimination_is_eliminated_team5(team5, team, expected_eliminated, expected_eliminated_by):
    assert team5.isEliminated(team) == expected_eliminated
    eliminated_by = team5.certificateOfElimination(team)
    assert (
            (eliminated_by is None and expected_eliminated_by is None) or
            sorted(team5.certificateOfElimination(team)) == sorted(expected_eliminated_by)
    )
