
from roadvision.tracking import VehicleTracker


class ModeloSimulado:
    def track(self, *args, **kwargs):
        raise NotImplementedError


def criar_rastreador():
    return VehicleTracker(
        model=ModeloSimulado(),
        limite_inatividade=3,
        intervalo_limpeza=1,
    )


def test_limpar_dados_de_id_inativo():
    tracker = criar_rastreador()

    tracker.frame_index = 10
    tracker.history[7].extend([(10, 20), (15, 25)])
    tracker.states[7] = "MOVENDO"
    tracker.pending_states[7] = "PARADO"
    tracker.state_streaks[7] = 2
    tracker.last_seen[7] = 5
    tracker.unique_ids.add(7)

    removidos = tracker.limpar_inativos()

    assert removidos == 1
    assert 7 not in tracker.history
    assert 7 not in tracker.states
    assert 7 not in tracker.pending_states
    assert 7 not in tracker.state_streaks
    assert 7 not in tracker.last_seen


def test_preservar_id_recente():
    tracker = criar_rastreador()

    tracker.frame_index = 10
    tracker.history[8].append((10, 20))
    tracker.states[8] = "MOVENDO"
    tracker.last_seen[8] = 9
    tracker.unique_ids.add(8)

    removidos = tracker.limpar_inativos()

    assert removidos == 0
    assert tracker.get_trajectory(8) == [(10, 20)]
    assert tracker.get_vehicle_state(8) == "MOVENDO"


def test_preservar_historico_de_ids_unicos():
    tracker = criar_rastreador()

    tracker.frame_index = 10
    tracker.history[9].append((10, 20))
    tracker.states[9] = "PARADO"
    tracker.last_seen[9] = 5
    tracker.unique_ids.add(9)

    tracker.limpar_inativos()

    assert tracker.get_unique_count() == 1
    assert 9 in tracker.unique_ids
