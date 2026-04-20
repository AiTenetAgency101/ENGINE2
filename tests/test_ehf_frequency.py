from engine_core.ehf_frequency import (
    BioMetrics,
    CircadianPhase,
    CircadianRhythmEngine,
    CognitiveState,
    EHFFrequencyEngine,
)


def test_biometrics_to_dict_formats_blood_pressure():
    data = BioMetrics(blood_pressure=(118, 76)).to_dict()

    assert data["blood_pressure"] == "118/76"


def test_circadian_phase_boundaries_cover_all_primary_windows():
    circadian = CircadianRhythmEngine()

    assert circadian.get_circadian_phase(1.5) == CircadianPhase.DEEP_SLEEP
    assert circadian.get_circadian_phase(3.0) == CircadianPhase.LIGHT_SLEEP
    assert circadian.get_circadian_phase(6.5) == CircadianPhase.WAKE_UP
    assert circadian.get_circadian_phase(8.0) == CircadianPhase.MORNING_PEAK
    assert circadian.get_circadian_phase(10.0) == CircadianPhase.FOCUS_WINDOW
    assert circadian.get_circadian_phase(12.5) == CircadianPhase.POST_LUNCH_DIP
    assert circadian.get_circadian_phase(15.5) == CircadianPhase.AFTERNOON_PEAK
    assert circadian.get_circadian_phase(20.0) == CircadianPhase.EVENING_WIND


def test_optimal_sleep_time_uses_zero_padded_hours():
    circadian = CircadianRhythmEngine(sleep_time=23, wake_time=7)

    assert circadian.get_optimal_sleep_time() == ("23:00", "07:00")


def test_analyze_biometrics_calculates_overall_performance():
    engine = EHFFrequencyEngine()
    metrics = BioMetrics(
        heart_rate_variability=80,
        stress_score=20,
        sleep_quality=90,
        energy_level=85,
    )

    analysis = engine.analyze_biometrics(metrics)

    assert analysis["hrv_score"] == 80
    assert analysis["overall_performance"] == 83.75
    assert analysis["status"] == "OPTIMAL"


def test_performance_status_thresholds():
    engine = EHFFrequencyEngine()

    assert engine._get_performance_status(90) == "PEAK_PERFORMANCE"
    assert engine._get_performance_status(80) == "OPTIMAL"
    assert engine._get_performance_status(70) == "GOOD"
    assert engine._get_performance_status(60) == "FAIR"
    assert engine._get_performance_status(59.9) == "BELOW_OPTIMAL"


def test_cognitive_mapping_and_frequency_selection():
    engine = EHFFrequencyEngine()

    assert engine.get_cognitive_state(CircadianPhase.FOCUS_WINDOW) == CognitiveState.DEEP_WORK
    assert engine.get_optimal_frequency(CognitiveState.CREATIVE) == 20.0


def test_recommendations_include_contextual_guidance_and_optimal_fallback(monkeypatch):
    engine = EHFFrequencyEngine()
    engine.current_metrics = BioMetrics(
        heart_rate=110,
        sleep_quality=65,
        stress_score=75,
        energy_level=40,
        glucose_level=150,
    )
    monkeypatch.setattr(engine.circadian, "get_circadian_phase", lambda: CircadianPhase.POST_LUNCH_DIP)

    recommendations = engine.get_recommendations()

    assert any("High HR" in r for r in recommendations)
    assert any("Poor sleep" in r for r in recommendations)
    assert any("High stress" in r for r in recommendations)
    assert any("Low energy" in r for r in recommendations)
    assert any("High glucose" in r for r in recommendations)
    assert any("Afternoon dip" in r for r in recommendations)

    optimal_engine = EHFFrequencyEngine()
    optimal_engine.current_metrics = BioMetrics()
    monkeypatch.setattr(optimal_engine.circadian, "get_circadian_phase", lambda: CircadianPhase.WAKE_UP)

    assert optimal_engine.get_recommendations() == ["✅ Optimal conditions - maintain current state"]


def test_get_ehf_status_returns_complete_payload(monkeypatch):
    engine = EHFFrequencyEngine()
    engine.analyze_biometrics(BioMetrics())
    monkeypatch.setattr(engine.circadian, "get_circadian_phase", lambda: CircadianPhase.MORNING_PEAK)

    status = engine.get_ehf_status()

    assert "timestamp" in status
    assert status["circadian_phase"] == "morning_peak"
    assert status["cognitive_state"] == "peak_focus"
    assert status["optimal_frequency"] == "10.0 Hz"
    assert "biomarkers" in status
    assert "recommendations" in status
    assert "sleep_window" in status
