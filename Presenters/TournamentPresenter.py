import curses
import time

from Models.GameModel import GameModel
from Models.SettingsModel import SettingsModel
from Models.tournament.TournamentModel import TournamentStatsModel
from Models.tournament.TournamentTable import TournamentTable
from Presenters.GamePresenter import GamePresenter
from Presenters.TournamentStatPresenter import TournamentStatPresenter
from Views.TournamentView import TournamentView


class TournamentPresenter:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.settings_model = None
        self.game_model = GameModel()
        self.stat_presenter = None
        self.tournament_view = TournamentView()
        self.tour_model = None
        self.gamers_count = 0


    def show_tournament_begin(self, settings_model: SettingsModel):

        self.stat_presenter = TournamentStatPresenter(self.stdscr, self.game_model,
                 settings_model, TournamentStatsModel())
        self.settings_model = settings_model

        self.gamers_count = self.tournament_view.draw(self.stdscr)
        gamers = self.tournament_view.show_init_gamer(self.stdscr, self.gamers_count)
        is_big_text = self.tournament_view.is_big_text(self.stdscr)
        self.tour_model = TournamentTable(gamers, self.settings_model, is_big_text)

        game_tournament_presenter = GamePresenter(self.stdscr, self.game_model, self.settings_model)

        current_round = 1
        current_gamers = gamers.copy()
        self.tournament_view.show_start(self.stdscr)
        best_results = {gamer: {} for gamer in gamers}

        while len(current_gamers) > 1:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, f"Раунд {current_round}")
            self.stdscr.refresh()
            time.sleep(3)
            curses.flushinp()
            winners = []
            for i in range(0, len(current_gamers), 2):

                gamer1 = current_gamers[i]
                gamer2 = current_gamers[i + 1]

                self.tournament_view.show_vs(self.stdscr, gamer1, gamer2)
                time.sleep(3)

                curses.flushinp()
                gamer_result1 = game_tournament_presenter.start_game()
                curses.flushinp()
                gamer_result2 = game_tournament_presenter.start_game()

                if ("correct_keystrokes" not in best_results[gamer1]) or (gamer_result1['correct_keystrokes'] > best_results[gamer1]['correct_keystrokes']):
                    best_results[gamer1] = gamer_result1

                if ("correct_keystrokes" not in best_results[gamer2]) or (gamer_result2['correct_keystrokes'] > best_results[gamer2]['correct_keystrokes']):
                    best_results[gamer2] = gamer_result2

                if gamer_result1['correct_keystrokes'] > gamer_result2['correct_keystrokes']:
                    winners.append(gamer1)
                elif gamer_result1['correct_keystrokes'] < gamer_result2['correct_keystrokes']:
                    winners.append(gamer2)
                elif gamer_result1['uniformity_score'] > gamer_result2['uniformity_score']:
                    winners.append(gamer1)
                else:
                    winners.append(gamer2)
                if is_big_text is False:
                    self.settings_model.set_random_level()

            current_gamers = winners
            current_round += 1
        curses.flushinp()
        self.tournament_view.show_winer(self.stdscr, current_gamers[0].decode("utf-8"))
        time.sleep(3 )
        self.stat_presenter.save_winner(settings_model.current_language,
                                        settings_model.current_difficulty, current_gamers[0].decode("utf-8"),
                                        best_results[current_gamers[0]])
