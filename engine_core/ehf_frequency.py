"""
EHF (Efficient Human Frequency) Core Engine
Biometric-driven optimization for peak human performance
Synchronized with TRON rhythm and circadian biology
"""

import asyncio
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import math

class CognitiveState(Enum):
    """Human cognitive performance states"""
    PEAK_FOCUS = "peak_focus"          # 8-12 Hz (alpha waves)
    DEEP_WORK = "deep_work"            # 4-8 Hz (theta waves)
    CREATIVE = "creative"              # 12-30 Hz (beta waves)
    RECOVERY = "recovery"              # 0.5-4 Hz (delta waves)
    RELAXED = "relaxed"                # 8-12 Hz (alpha)
    SLEEP = "sleep"                    # 0.5-4 Hz (delta/theta)

class CircadianPhase(Enum):
    """24-hour biological rhythm phases"""
    DEEP_SLEEP = "deep_sleep"          # 22:00-02:00
    LIGHT_SLEEP = "light_sleep"        # 02:00-06:00
    WAKE_UP = "wake_up"                # 06:00-07:00 (cortisol spike)
    MORNING_PEAK = "morning_peak"      # 07:00-09:00 (peak alertness)
    FOCUS_WINDOW = "focus_window"      # 09:00-12:00 (peak cognition)
    POST_LUNCH_DIP = "post_lunch_dip"  # 13:00-15:00 (energy drop)
    AFTERNOON_PEAK = "afternoon_peak"  # 15:00-17:00 (2nd peak)
    EVENING_WIND = "evening_wind"      # 17:00-21:00 (gradual decline)

@dataclass
class BioMetrics:
    """Real-time human biomarkers"""
    heart_rate: int = 60              # BPM
    heart_rate_variability: float = 50.0  # HRV (ms)
    blood_pressure: Tuple[int, int] = (120, 80)  # Systolic/Diastolic
    blood_oxygen: float = 98.0        # %
    body_temperature: float = 36.8    # Celsius
    cortisol_level: float = 50.0      # ng/mL
    glucose_level: float = 100.0      # mg/dL
    sleep_quality: float = 85.0       # % (0-100)
    sleep_duration: float = 8.0       # hours
    stress_score: float = 30.0        # 0-100
    energy_level: float = 80.0        # 0-100
    mental_clarity: float = 85.0      # 0-100
    
    def to_dict(self) -> Dict:
        return {
            'heart_rate': self.heart_rate,
            'heart_rate_variability': self.heart_rate_variability,
            'blood_pressure': f"{self.blood_pressure[0]}/{self.blood_pressure[1]}",
            'blood_oxygen': self.blood_oxygen,
            'body_temperature': self.body_temperature,
            'cortisol': self.cortisol_level,
            'glucose': self.glucose_level,
            'sleep_quality': self.sleep_quality,
            'sleep_duration': self.sleep_duration,
            'stress_score': self.stress_score,
            'energy_level': self.energy_level,
            'mental_clarity': self.mental_clarity,
        }

class CircadianRhythmEngine:
    """24-hour biological clock synchronization"""
    
    def __init__(self, sleep_time: float = 22.0, wake_time: float = 6.0):
        self.sleep_time = sleep_time      # Hours (0-24)
        self.wake_time = wake_time        # Hours (0-24)
        self.sleep_duration = 8.0         # Target hours
        self.current_phase = CircadianPhase.WAKE_UP
        
        # Hormone cycles
        self.cortisol_rhythm = {}  # Cortisol curve throughout day
        self.melatonin_rhythm = {}  # Melatonin curve throughout day
        self.core_temp_rhythm = {}  # Body temperature curve
        self._initialize_rhythms()
    
    def _initialize_rhythms(self):
        """Initialize biological hormone rhythms"""
        for hour in range(24):
            # Cortisol: High at wake, low at sleep
            cortisol_peak = 6.5  # Peak at 6:30 AM
            cortisol = 50 * math.exp(-((hour - cortisol_peak) ** 2) / 6)
            self.cortisol_rhythm[hour] = max(10, cortisol)
            
            # Melatonin: High at night, low during day
            melatonin_peak = 2.0  # Peak at 2 AM
            melatonin = 80 * math.exp(-((hour - melatonin_peak) ** 2) / 8)
            self.melatonin_rhythm[hour] = max(5, melatonin)
            
            # Body temperature: Low at night, high in afternoon
            temp_peak = 17.0  # Peak at 5 PM
            temp = 0.8 * math.sin((hour - 5) * math.pi / 12) + 36.8
            self.core_temp_rhythm[hour] = temp
    
    def get_circadian_phase(self, current_hour: float = None) -> CircadianPhase:
        """Get current circadian phase"""
        if current_hour is None:
            current_hour = datetime.now().hour + datetime.now().minute / 60
        
        if 22 <= current_hour or current_hour < 2:
            return CircadianPhase.DEEP_SLEEP
        elif 2 <= current_hour < 6:
            return CircadianPhase.LIGHT_SLEEP
        elif 6 <= current_hour < 7:
            return CircadianPhase.WAKE_UP
        elif 7 <= current_hour < 9:
            return CircadianPhase.MORNING_PEAK
        elif 9 <= current_hour < 12:
            return CircadianPhase.FOCUS_WINDOW
        elif 12 <= current_hour < 13:
            return CircadianPhase.POST_LUNCH_DIP
        elif 13 <= current_hour < 15:
            return CircadianPhase.POST_LUNCH_DIP
        elif 15 <= current_hour < 17:
            return CircadianPhase.AFTERNOON_PEAK
        else:
            return CircadianPhase.EVENING_WIND
    
    def get_cortisol_level(self, hour: float = None) -> float:
        """Get expected cortisol level for hour"""
        if hour is None:
            hour = datetime.now().hour
        return self.cortisol_rhythm.get(int(hour), 30.0)
    
    def get_melatonin_level(self, hour: float = None) -> float:
        """Get expected melatonin level for hour"""
        if hour is None:
            hour = datetime.now().hour
        return self.melatonin_rhythm.get(int(hour), 20.0)
    
    def get_optimal_sleep_time(self) -> Tuple[str, str]:
        """Get optimal sleep and wake times"""
        return (f"{int(self.sleep_time):02d}:00", f"{int(self.wake_time):02d}:00")

class EHFFrequencyEngine:
    """
    Efficient Human Frequency Engine
    Optimizes human performance through biometric synchronization
    """
    
    def __init__(self):
        self.circadian = CircadianRhythmEngine()
        self.current_metrics = BioMetrics()
        self.frequency_history: List[Dict] = []
        self.performance_score = 0.0
        self.optimization_level = 0.0
        
        # EHF frequency bands (Hz)
        self.efh_frequencies = {
            CognitiveState.PEAK_FOCUS: 10.0,     # 8-12 Hz (alpha-beta)
            CognitiveState.DEEP_WORK: 6.0,       # 4-8 Hz (theta)
            CognitiveState.CREATIVE: 20.0,       # 12-30 Hz (beta-gamma)
            CognitiveState.RECOVERY: 2.0,        # 0.5-4 Hz (delta)
            CognitiveState.RELAXED: 10.0,        # 8-12 Hz (alpha)
            CognitiveState.SLEEP: 1.0,           # 0.5-4 Hz (delta)
        }
        
        # Performance optimization targets
        self.targets = {
            'heart_rate': 60,              # Resting HR
            'hrv': 60.0,                   # HRV > 60ms is healthy
            'cortisol': 'circadian',       # Follow natural rhythm
            'glucose': 100.0,              # Fasting glucose
            'stress_score': 30.0,          # Low stress
            'sleep_quality': 85.0,         # 85%+ quality
        }
    
    def analyze_biometrics(self, metrics: BioMetrics = None) -> Dict:
        """Analyze current biometrics against optimal ranges"""
        if metrics:
            self.current_metrics = metrics
        
        m = self.current_metrics
        
        # Heart rate variability score (higher = better)
        hrv_score = min(100, (m.heart_rate_variability / 100) * 100)
        
        # Stress score analysis
        stress_score = m.stress_score
        
        # Sleep quality
        sleep_score = m.sleep_quality
        
        # Energy level
        energy_score = m.energy_level
        
        # Overall performance
        overall = (hrv_score + (100 - stress_score) + sleep_score + energy_score) / 4
        self.performance_score = overall
        
        return {
            'hrv_score': hrv_score,
            'stress_score': stress_score,
            'sleep_score': sleep_score,
            'energy_score': energy_score,
            'overall_performance': overall,
            'status': self._get_performance_status(overall),
        }
    
    def _get_performance_status(self, score: float) -> str:
        """Get performance status description"""
        if score >= 90:
            return "PEAK_PERFORMANCE"
        elif score >= 80:
            return "OPTIMAL"
        elif score >= 70:
            return "GOOD"
        elif score >= 60:
            return "FAIR"
        else:
            return "BELOW_OPTIMAL"
    
    def get_cognitive_state(self, circadian_phase: CircadianPhase = None) -> CognitiveState:
        """Determine optimal cognitive state for current time"""
        if not circadian_phase:
            circadian_phase = self.circadian.get_circadian_phase()
        
        # Map circadian phase to cognitive state
        phase_to_cognitive = {
            CircadianPhase.DEEP_SLEEP: CognitiveState.SLEEP,
            CircadianPhase.LIGHT_SLEEP: CognitiveState.SLEEP,
            CircadianPhase.WAKE_UP: CognitiveState.RELAXED,
            CircadianPhase.MORNING_PEAK: CognitiveState.PEAK_FOCUS,
            CircadianPhase.FOCUS_WINDOW: CognitiveState.DEEP_WORK,
            CircadianPhase.POST_LUNCH_DIP: CognitiveState.RECOVERY,
            CircadianPhase.AFTERNOON_PEAK: CognitiveState.PEAK_FOCUS,
            CircadianPhase.EVENING_WIND: CognitiveState.RELAXED,
        }
        
        return phase_to_cognitive.get(circadian_phase, CognitiveState.RELAXED)
    
    def get_optimal_frequency(self, cognitive_state: CognitiveState = None) -> float:
        """Get optimal EHF frequency for cognitive state"""
        if not cognitive_state:
            cognitive_state = self.get_cognitive_state()
        
        return self.efh_frequencies.get(cognitive_state, 10.0)
    
    def get_recommendations(self) -> List[str]:
        """Get personalized recommendations for optimal performance"""
        m = self.current_metrics
        circadian = self.circadian.get_circadian_phase()
        recommendations = []
        
        # Heart rate recommendations
        if m.heart_rate > 100:
            recommendations.append("🫀 High HR: Take deep breathing breaks (4-7-8 technique)")
        elif m.heart_rate < 50:
            recommendations.append("🫀 Low HR: Light movement to increase circulation")
        
        # Sleep recommendations
        if m.sleep_quality < 70:
            recommendations.append("😴 Poor sleep: Avoid screens 1hr before bed, cool room (16-18°C)")
        
        # Stress recommendations
        if m.stress_score > 60:
            recommendations.append("🧘 High stress: 5-min meditation or cold exposure (15s)")
        
        # Energy recommendations
        if m.energy_level < 50:
            recommendations.append("⚡ Low energy: Hydrate (500ml water), take 10-min walk")
        
        # Glucose recommendations
        if m.glucose_level > 130:
            recommendations.append("🍎 High glucose: Light activity after meals, vinegar before eating")
        
        # Circadian recommendations
        if circadian == CircadianPhase.POST_LUNCH_DIP:
            recommendations.append("☀️ Afternoon dip: 10-min sunlight exposure, short walk")
        
        # Cognitive state recommendations
        cognitive = self.get_cognitive_state(circadian)
        if cognitive == CognitiveState.PEAK_FOCUS:
            recommendations.append("🎯 Peak focus time: Start deep work now (90-min blocks)")
        elif cognitive == CognitiveState.RECOVERY:
            recommendations.append("🔄 Recovery phase: Switch to admin tasks, light meetings")
        
        return recommendations if recommendations else ["✅ Optimal conditions - maintain current state"]
    
    def get_ehf_status(self) -> Dict:
        """Get complete EHF status"""
        circadian = self.circadian.get_circadian_phase()
        cognitive = self.get_cognitive_state(circadian)
        frequency = self.get_optimal_frequency(cognitive)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'performance_score': round(self.performance_score, 1),
            'performance_status': self._get_performance_status(self.performance_score),
            'circadian_phase': circadian.value,
            'cognitive_state': cognitive.value,
            'optimal_frequency': f"{frequency} Hz",
            'biomarkers': self.current_metrics.to_dict(),
            'recommendations': self.get_recommendations(),
            'sleep_window': self.circadian.get_optimal_sleep_time(),
        }

# Example usage
if __name__ == "__main__":
    engine = EHFFrequencyEngine()
    
    # Simulate different metrics
    metrics = BioMetrics(
        heart_rate=65,
        heart_rate_variability=55,
        cortisol_level=45,
        glucose_level=95,
        stress_score=25,
        energy_level=85,
        sleep_quality=90,
        mental_clarity=88,
    )
    
    # Analyze
    analysis = engine.analyze_biometrics(metrics)
    status = engine.get_ehf_status()
    
    print("[EHF] Efficient Human Frequency Engine")
    print(f"Performance Score: {analysis['overall_performance']:.1f}%")
    print(f"Status: {analysis['status']}")
    print(f"\nCircadian Phase: {status['circadian_phase']}")
    print(f"Cognitive State: {status['cognitive_state']}")
    print(f"Optimal Frequency: {status['optimal_frequency']}")
    print(f"\nRecommendations:")
    for rec in status['recommendations']:
        print(f"  {rec}")
