from comandos.partida import extraer_cantidad_de_jugadores


def test_extraer_cantidad_de_jugadores():
    assert extraer_cantidad_de_jugadores("!crear 10") == 10
