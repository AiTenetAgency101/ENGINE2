from engine_core import xyo_invariants as xyo


def test_xyo_invariant_unknown_type_uses_fallback_kanji():
    invariant = xyo.XYOInvariant("custom", "v", "device-1")

    assert invariant.kanji == "不明"
    assert len(invariant.hash) == 64


def test_bound_witness_contains_three_invariants_and_hash():
    witness = xyo.BoundWitness("10,20", "dev-1", "container-a")
    payload = witness.to_dict()["bound_witness"]

    assert payload["location"]["type"] == "location"
    assert payload["time"]["type"] == "time"
    assert payload["identity"]["type"] == "identity"
    assert payload["container"] == "container-a"
    assert len(payload["witness_hash"]) == 64


def test_solve_container_health_caps_at_one_for_large_coordinates():
    result = xyo.SymPyLocationSync.solve_container_health(5000, 5000, 0)

    assert result["container_health"] == 1.0
    assert result["status"] == "healthy"


def test_solve_container_health_returns_fallback_when_symbolic_math_fails(monkeypatch):
    monkeypatch.setattr(xyo, "simplify", lambda *_: (_ for _ in ()).throw(RuntimeError("boom")))

    result = xyo.SymPyLocationSync.solve_container_health(1, 1, 0.1)

    assert result["container_health"] == 0.5
    assert result["status"] == "degraded"


def test_engine_xyo_sync_register_and_manifest_generation(monkeypatch):
    monkeypatch.setattr(xyo.time, "time", lambda: 1000.0)

    sync = xyo.ENGINEXYOSync("Auckland", "device-99")
    registration = sync.register_container("app", "cid-1", 12.0, 24.0)

    assert registration["synchronized"] is True
    assert registration["container"] == "app"
    assert sync.to_kanji_string() == "位置 時間 身分"

    manifest = sync.generate_sync_manifest()

    assert manifest["engine_location"] == "Auckland"
    assert manifest["device_id"] == "device-99"
    assert manifest["kanji_sync"] == "位置 時間 身分"
    assert len(manifest["containers"]) == 1
    assert manifest["total_health_score"] == 0.5
