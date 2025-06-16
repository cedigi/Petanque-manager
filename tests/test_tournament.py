import os
import sys
import random

# Ensure project module is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'project'))
from petanque_manager.tournament import Tournament


def create_tournament(num_teams, tournament_type="doublette"):
    t = Tournament(name="Test", tournament_type=tournament_type, terrain_count=2)
    for i in range(num_teams):
        t.add_team([f"Player {i*2+1}", f"Player {i*2+2}"])
    return t


def test_generate_first_round_matches_even():
    random.seed(0)
    t = create_tournament(4)
    matches = t.generate_first_round_matches()
    assert t.current_round == 1
    assert len(matches) == 2
    assert all(m.round_number == 1 for m in matches)
    assert not any(m.is_bye for m in matches)


def test_generate_first_round_matches_odd():
    random.seed(0)
    t = create_tournament(3)
    matches = t.generate_first_round_matches()
    assert t.current_round == 1
    assert len(matches) == 2
    bye_matches = [m for m in matches if m.is_bye]
    assert len(bye_matches) == 1
    assert bye_matches[0].completed


def test_generate_next_round_matches_standard():
    random.seed(0)
    t = create_tournament(4)
    first = t.generate_first_round_matches()
    # all team1 win
    for match in first:
        t.update_match_score(match.id, 13, 7)
    next_matches = t.generate_next_round_matches()
    assert t.current_round == 2
    assert len(next_matches) == 2
    winners = {m.team1.id for m in first}
    group_subsets = [set([m.team1.id, m.team2.id]) for m in next_matches]
    assert any(g.issubset(winners) for g in group_subsets)
    assert any(g.isdisjoint(winners) for g in group_subsets)


def test_get_all_stats_and_is_round_complete():
    random.seed(1)
    t = create_tournament(2)
    matches = t.generate_first_round_matches()
    m = matches[0]
    assert not t.is_round_complete(1)
    t.update_match_score(m.id, 13, 7)
    assert t.is_round_complete(1)
    assert not t.is_round_complete(2)
    stats = t.get_all_stats()
    assert len(stats) == 2
    assert stats[0].team.id == m.team1.id
    assert stats[0].wins == 1
    assert stats[0].losses == 0
    assert stats[0].points_for == 13
    assert stats[0].points_against == 7
    assert stats[1].team.id == m.team2.id
    assert stats[1].wins == 0
    assert stats[1].losses == 1

