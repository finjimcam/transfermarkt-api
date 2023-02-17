from dataclasses import dataclass
from typing import Optional
from xml.etree import ElementTree

from app.services.commons.search import TransfermarktSearch
from app.utils.xpath import Players


@dataclass
class TransfermarktPlayerSearch(TransfermarktSearch):
    def search_players(self) -> Optional[list]:
        result_players: ElementTree = self.search_page.xpath(Players.Search.RESULT)

        if not result_players:
            return None

        result_nationalities: ElementTree = result_players[0].xpath(Players.Search.RESULT_NATIONALITIES)

        players_names: list = result_players[0].xpath(Players.Search.NAMES)
        players_urls: list = result_players[0].xpath(Players.Search.URLS)
        players_clubs: list = result_players[0].xpath(Players.Search.CLUB)
        players_market_values: list = result_players[0].xpath(Players.Search.MARKET_VALUES)
        player_nationalities: list = [
            nationality.xpath(Players.Search.NATIONALITIES) for nationality in result_nationalities
        ]
        players_ids: list = [url.split("/")[-1] for url in players_urls]

        return [
            {
                "id": idx,
                "url": url,
                "name": name,
                "market_value": market_value,
                "nationality": nationality,
                "current_club": club,
            }
            for idx, url, name, market_value, nationality, club, in zip(
                players_ids,
                players_urls,
                players_names,
                players_market_values,
                player_nationalities,
                players_clubs,
            )
        ]
