"""
Implement baseball elimination
"""
from part2_week3.maxflow import FlowEdge, FlowNetwork, FordFulkerson
from itertools import combinations
from functools import reduce


class Standing(object):
    """standing of a team"""
    def __init__(self, standing, idx):
        self._idx = idx
        self._total_team = len(standing[4:])
        self._team = standing[0]
        self._wins = int(standing[1])
        self._losses = int(standing[2])
        self._left = int(standing[3])
        self._against = [int(x) for x in standing[4:]]

    def wins(self):
        return self._wins

    def losses(self):
        return self._losses

    def left(self):
        return self._left

    def against(self, idx):
        if idx == self._idx:
            raise ValueError("No games against oneself")

        return self._against[idx]

    def team(self):
        return self._team

    def __repr__(self):
        return "{}: {}W{}L{}R".format(self.team(), self.wins(), self.losses(), self.left())


class BaseballElimination(object):
    """main class"""
    def __init__(self, filename):
        self._team = dict()
        self._flow_network = None
        self._game_vertices = None
        self._max_flow = None
        with open(filename, 'r') as f:
            self._total_team = int(f.readline().strip())
            self._standings = [None]*self._total_team
            for idx, l in enumerate(f):
                standing = Standing(l.split(), idx)
                self._standings[idx] = standing
                self._team[standing.team()] = idx
        num_game_vertices = (self._total_team-1)*(self._total_team-2)//2
        self._total_vertices = self._total_team+num_game_vertices+1

    def numberOfTeams(self):
        return self._total_team

    def teams(self):
        return list(self._team.keys())

    def wins(self, team):
        idx = self._get_team_idx(team)
        return self._standings[idx].wins()

    def losses(self, team):
        idx = self._get_team_idx(team)
        return self._standings[idx].losses()

    def against(self, team1, team2):
        idx1 = self._get_team_idx(team1)
        idx2 = self._get_team_idx(team2)
        return self._standings[idx1].against(idx2)

    def isEliminated(self, team):
        simply_eliminated, _ = self._simply_eliminated(team)
        if simply_eliminated:
            return True

        idx = self._get_team_idx(team)
        # Step 1: construct flow network
        total_games = self._standings[idx].wins() + self._standings[idx].left()
        self._flow_network = FlowNetwork(self._total_vertices)
        # 0 ~ self._total_team-1 are team vertices, where source is idx of target 'team',
        # sink is self._flow_network.V()-1
        self._game_vertices = dict()
        k = self._total_team
        remaining_team = [i for i in range(self._total_team) if i != idx]
        for g in combinations(remaining_team, 2):
            self._game_vertices[k] = g
            self._flow_network.addEdge(FlowEdge(idx, k, self._standings[g[0]].against(g[1])))
            self._flow_network.addEdge(FlowEdge(k, g[0], float('inf')))
            self._flow_network.addEdge(FlowEdge(k, g[1], float('inf')))
            k += 1

        for i in remaining_team:
            self._flow_network.addEdge(FlowEdge(i, self._total_vertices-1, total_games-self._standings[i].wins()))

        self._max_flow = FordFulkerson(self._flow_network, idx, self._total_vertices-1)

        is_full_capacity = reduce(lambda x, y: x and y,
                                  [e.flow == e.capacity for e in self._flow_network.adj(idx)],
                                  True)
        return not is_full_capacity

    def certificateOfElimination(self, team):
        simply_eliminated, simply_eliminated_by = self._simply_eliminated(team)
        if simply_eliminated:
            return simply_eliminated_by

        is_eliminated = self.isEliminated(team)
        target_team_idx = self._get_team_idx(team)
        max_wins = self._standings[target_team_idx].wins() + self._standings[target_team_idx].left()
        if is_eliminated:
            min_cut = self._max_flow.min_cut()
            team = set()
            for idx in min_cut:
                if idx < self._total_team-1 and idx != target_team_idx:
                    team.add(self._standings[idx].team())

            return list(team)

        else:
            return None

    def _simply_eliminated(self, team):
        idx = self._get_team_idx(team)
        potential_wins = self._standings[idx].wins() + self._standings[idx].left()
        fewest_losses = self._standings[idx].losses()
        max_win = max([s.wins() for s in self._standings])
        max_winning_team = [s for s in self._standings if s.wins() == max_win]
        min_lossed_in_max_win = min([s.losses()+s.left() for s in max_winning_team])
        weakest_winner = [s for s in max_winning_team if s.losses()+s.left() == min_lossed_in_max_win][0]
        fewest_win, most_losses = weakest_winner.wins(), weakest_winner.losses()+weakest_winner.left()
        if potential_wins < fewest_win or (potential_wins == fewest_win and fewest_losses > most_losses):
            return True, {weakest_winner.team()}
        else:
            return False, None

    def _get_team_idx(self, team):
        try:
            idx = self._team[team]
        except KeyError:
            raise KeyError("{} is not a valid team.".format(team))

        return idx
