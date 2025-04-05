from utils.matar_ciudadano import extraer_nick_de_la_victima


def test_extraer_cantidad_de_jugadores():
    assert extraer_nick_de_la_victima("!matar NPC_1") == "NPC_1"
