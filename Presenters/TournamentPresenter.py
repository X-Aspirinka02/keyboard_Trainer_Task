import curses

from Models.TournamentModel import TournamentModel
from Views.TournamentView import TournamentView


class TournamentPresenter:
    def __init__(self, stdscr: curses.window, tour_model: TournamentModel):
        self.stdscr = stdscr
        self.tournament_view = TournamentView()
        self.tour_model = tour_model
        self.gamers_count = 0

    def show_tournament_begin(self):
        self.gamers_count = self.tournament_view.draw(self.stdscr)
        gamers = self.tournament_view.show_init_gamer(self.stdscr, self.gamers_count)


