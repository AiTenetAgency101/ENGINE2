"""
EHF-TRON Frequency Alignment Protocol
Synchronizes human efficient frequencies with TRON distributed consensus
Optimizes decision-making, automation execution, and system coordination
"""

import asyncio
from typing import Dict, List
from datetime import datetime
import json
from engine_core.ehf_frequency import EHFFrequencyEngine, BioMetrics, CognitiveState


class EHFTRONAlignment:
    """
    EHF-TRON Frequency Alignment
    Synchronizes human cognitive performance with distributed consensus cycles
    """

    def __init__(self, ehf_engine: EHFFrequencyEngine = None, tron_engine=None):
        self.ehf_engine = ehf_engine or EHFFrequencyEngine()
        self.tron_engine = tron_engine

        # Alignment metrics
        self.alignment_score = 0.0
        self.synchronization_accuracy = 0.0
        self.decision_quality = 0.0
        self.execution_efficiency = 0.0

        # History
        self.alignment_history: List[Dict] = []

    async def align_human_tron_cycles(self, human_metrics: BioMetrics) -> Dict:
        """
        Align human performance cycles with TRON consensus cycles
        Returns optimization parameters for both systems
        """

        # Analyze human state
        human_analysis = self.ehf_engine.analyze_biometrics(human_metrics)
        human_cognitive = self.ehf_engine.get_cognitive_state()
        human_frequency = self.ehf_engine.get_optimal_frequency(human_cognitive)

        # Get TRON state
        tron_status = self.tron_engine.get_grid_status() if self.tron_engine else {}
        tron_cycle = tron_status.get("cycle", 0)
        tron_sync_accuracy = tron_status.get("sync_accuracy", 100.0)

        # Calculate alignment
        # Peak human performance (cognitive state optimal) + TRON consensus = best decisions
        self.alignment_score = self._calculate_alignment(human_analysis, tron_status)
        self.synchronization_accuracy = min(
            100, human_analysis["overall_performance"] * tron_sync_accuracy / 100
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "human": {
                "performance": human_analysis["overall_performance"],
                "cognitive_state": human_cognitive.value,
                "optimal_frequency": f"{human_frequency} Hz",
                "status": human_analysis["status"],
            },
            "tron": {
                "cycle": tron_cycle,
                "sync_accuracy": tron_sync_accuracy,
                "consensus_efficiency": tron_status.get("consensus_efficiency", 100.0),
            },
            "alignment": {
                "alignment_score": round(self.alignment_score, 1),
                "synchronization_accuracy": round(self.synchronization_accuracy, 1),
                "recommendation": self._get_alignment_recommendation(),
            },
        }

    def _calculate_alignment(self, human_analysis: Dict, tron_status: Dict) -> float:
        """Calculate alignment score between human and TRON systems"""
        human_perf = human_analysis["overall_performance"]
        tron_sync = tron_status.get("sync_accuracy", 50)

        # Both need to be high for good alignment
        alignment = (human_perf + tron_sync) / 2

        return alignment

    def _get_alignment_recommendation(self) -> str:
        """Get alignment recommendation"""
        if self.alignment_score >= 85:
            return "🎯 OPTIMAL - Critical decisions and executions can proceed"
        elif self.alignment_score >= 70:
            return "✅ GOOD - Normal operations recommended"
        elif self.alignment_score >= 50:
            return "⚠️  FAIR - Wait for better alignment before critical decisions"
        else:
            return "❌ POOR - Rest and recovery recommended, delay important decisions"

    def get_optimal_decision_window(self) -> Dict:
        """Get optimal time window for critical human decision-making"""
        circadian = self.ehf_engine.circadian.get_circadian_phase()

        # Optimal windows for decision-making
        windows = {
            "decision_making": {
                "best": ["morning_peak", "afternoon_peak"],  # 7-9 AM, 3-5 PM
                "acceptable": ["focus_window"],  # 9 AM-12 PM
                "avoid": ["post_lunch_dip", "evening_wind"],  # 1-3 PM, 5-9 PM
            },
            "creative_thinking": {
                "best": ["morning_peak"],  # Early morning, fresh
                "acceptable": ["focus_window"],
                "avoid": ["post_lunch_dip"],
            },
            "execution": {
                "best": ["afternoon_peak", "evening_wind"],  # Afternoon + evening
                "acceptable": ["focus_window"],
                "avoid": ["post_lunch_dip"],
            },
        }

        return {
            "current_phase": circadian.value,
            "windows": windows,
            "current_suitability": self._get_phase_suitability(circadian),
        }

    def _get_phase_suitability(self, phase) -> Dict:
        """Get suitability of current phase for different tasks"""
        suitabilities = {
            "decision_making": 0,
            "creative_thinking": 0,
            "execution": 0,
            "routine_tasks": 0,
        }

        phase_value = phase.value

        if "morning_peak" in phase_value or "afternoon_peak" in phase_value:
            suitabilities["decision_making"] = 95
            suitabilities["creative_thinking"] = 90
            suitabilities["execution"] = 80
            suitabilities["routine_tasks"] = 70
        elif "focus_window" in phase_value:
            suitabilities["decision_making"] = 80
            suitabilities["creative_thinking"] = 75
            suitabilities["execution"] = 90
            suitabilities["routine_tasks"] = 85
        elif "post_lunch_dip" in phase_value:
            suitabilities["decision_making"] = 40
            suitabilities["creative_thinking"] = 35
            suitabilities["execution"] = 50
            suitabilities["routine_tasks"] = 60
        elif "evening_wind" in phase_value:
            suitabilities["decision_making"] = 50
            suitabilities["creative_thinking"] = 45
            suitabilities["execution"] = 70
            suitabilities["routine_tasks"] = 80
        elif "sleep" in phase_value:
            suitabilities["decision_making"] = 0
            suitabilities["creative_thinking"] = 0
            suitabilities["execution"] = 0
            suitabilities["routine_tasks"] = 0

        return suitabilities

    def get_system_readiness(self) -> Dict:
        """Get overall system readiness for critical operations"""
        human_perf = self.ehf_engine.performance_score
        alignment = self.alignment_score

        readiness_score = human_perf * 0.6 + alignment * 0.4

        return {
            "timestamp": datetime.now().isoformat(),
            "overall_readiness": round(readiness_score, 1),
            "readiness_level": self._get_readiness_level(readiness_score),
            "human_performance": round(human_perf, 1),
            "ehf_tron_alignment": round(alignment, 1),
            "recommendations": self._get_readiness_recommendations(readiness_score),
        }

    def _get_readiness_level(self, score: float) -> str:
        """Get readiness level"""
        if score >= 90:
            return "🟢 CRITICAL_READY - Proceed with high-impact decisions"
        elif score >= 75:
            return "🟢 READY - Standard operations"
        elif score >= 60:
            return "🟡 CAUTION - Hold major decisions, monitor metrics"
        else:
            return "🔴 NOT_READY - Rest and recovery required"

    def _get_readiness_recommendations(self, score: float) -> List[str]:
        """Get readiness recommendations"""
        recs = []

        if score < 70:
            recs.append("🛏️  Rest: 20-min power nap (16°C room)")
            recs.append("💧 Hydrate: 500ml water + electrolytes")
            recs.append("☀️  Sunlight: 10-min outdoor exposure")

        if self.ehf_engine.current_metrics.stress_score > 60:
            recs.append("🧘 Breathwork: 4-7-8 breathing (4in, 7hold, 8out)")

        if self.ehf_engine.current_metrics.energy_level < 60:
            recs.append("🍎 Nutrition: Low-glycemic snack (nuts, berries)")

        return recs if recs else ["✅ Continue current activities"]


class AdaptiveUIOptimization:
    """
    Adaptive UI/UX optimization based on human cognitive load
    Reduces cognitive burden during low-performance periods
    """

    def __init__(self, ehf_engine: EHFFrequencyEngine):
        self.ehf_engine = ehf_engine
        self.ui_complexity_levels = {
            "minimal": {"elements": 3, "animations": False, "notifications": False},
            "simple": {"elements": 8, "animations": True, "notifications": "critical"},
            "standard": {"elements": 15, "animations": True, "notifications": "all"},
            "advanced": {"elements": 30, "animations": True, "notifications": "all"},
            "expert": {"elements": 50, "animations": True, "notifications": "all"},
        }

    def get_optimal_ui_complexity(self) -> Dict:
        """Get optimal UI complexity for current cognitive state"""
        perf_score = self.ehf_engine.performance_score

        if perf_score >= 85:
            level = "expert"
        elif perf_score >= 75:
            level = "advanced"
        elif perf_score >= 65:
            level = "standard"
        elif perf_score >= 50:
            level = "simple"
        else:
            level = "minimal"

        config = self.ui_complexity_levels[level]

        return {
            "complexity_level": level,
            "config": config,
            "rationale": f"Cognitive load: {perf_score:.1f}% (optimal UI: {level})",
        }

    def get_focus_mode_settings(self) -> Dict:
        """Get focus mode settings based on cognitive state"""
        cognitive = self.ehf_engine.get_cognitive_state()

        settings = {
            "notification_silence": True,
            "minimize_visual_distractions": True,
            "show_only_essential_info": True,
            "focus_duration": 90,  # 90-minute focus blocks
            "break_duration": 15,  # 15-minute breaks
            "auto_save": True,
        }

        if cognitive == CognitiveState.CREATIVE:
            settings["focus_duration"] = 120
            settings["ambient_music_suggestion"] = "binaural_beats_40hz"

        return settings


# Example usage
if __name__ == "__main__":
    import asyncio

    async def demo():
        # Initialize
        ehf = EHFFrequencyEngine()
        alignment = EHFTRONAlignment(ehf_engine=ehf)

        # Simulate human metrics
        metrics = BioMetrics(
            heart_rate=68,
            heart_rate_variability=60,
            stress_score=20,
            energy_level=90,
            sleep_quality=92,
            mental_clarity=90,
        )

        # Get alignment
        align_result = await alignment.align_human_tron_cycles(metrics)
        print("[EHF-TRON] Frequency Alignment")
        print(json.dumps(align_result, indent=2))

        # Get decision window
        window = alignment.get_optimal_decision_window()
        print(f"\nOptimal Decision Window: {window['current_suitability']}")

        # Get readiness
        readiness = alignment.get_system_readiness()
        print(f"\nSystem Readiness: {readiness['overall_readiness']}%")
        print(f"Status: {readiness['readiness_level']}")

    asyncio.run(demo())
