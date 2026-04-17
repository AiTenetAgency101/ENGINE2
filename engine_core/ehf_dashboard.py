"""
EHF Performance Dashboard API
Real-time human performance optimization with TRON synchronization
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
from engine_core.ehf_frequency import EHFFrequencyEngine, BioMetrics
from engine_core.ehf_tron_alignment import EHFTRONAlignment, AdaptiveUIOptimization

class EHFDashboardAPI:
    """EHF Performance Dashboard - REST API"""
    
    def __init__(self, ehf_engine: EHFFrequencyEngine = None):
        self.ehf_engine = ehf_engine or EHFFrequencyEngine()
        self.alignment = EHFTRONAlignment(ehf_engine=self.ehf_engine)
        self.ui_optimizer = AdaptiveUIOptimization(self.ehf_engine)
        
        self.app = Flask(__name__)
        CORS(self.app)
        self._register_routes()

    def _register_routes(self):
        """Register API endpoints"""
        
        @self.app.route('/api/ehf/health', methods=['GET'])
        def health():
            return jsonify({'status': 'healthy', 'service': 'EHF'}), 200

        @self.app.route('/api/ehf/status', methods=['GET'])
        def ehf_status():
            """Get complete EHF status"""
            return jsonify(self.ehf_engine.get_ehf_status()), 200

        @self.app.route('/api/ehf/performance', methods=['GET'])
        def performance():
            """Get performance metrics"""
            analysis = self.ehf_engine.analyze_biometrics()
            return jsonify({
                'timestamp': datetime.now().isoformat(),
                'analysis': analysis,
                'metrics': self.ehf_engine.current_metrics.to_dict(),
            }), 200

        @self.app.route('/api/ehf/biomarkers', methods=['GET', 'POST'])
        def biomarkers():
            """Get or update biomarkers"""
            if request.method == 'POST':
                data = request.json
                metrics = BioMetrics(
                    heart_rate=data.get('heart_rate', 60),
                    heart_rate_variability=data.get('hrv', 50),
                    stress_score=data.get('stress', 30),
                    energy_level=data.get('energy', 80),
                    sleep_quality=data.get('sleep_quality', 85),
                    cortisol_level=data.get('cortisol', 50),
                    glucose_level=data.get('glucose', 100),
                )
                self.ehf_engine.current_metrics = metrics
                return jsonify({'updated': True, 'metrics': metrics.to_dict()}), 200
            
            return jsonify({
                'timestamp': datetime.now().isoformat(),
                'biomarkers': self.ehf_engine.current_metrics.to_dict(),
            }), 200

        @self.app.route('/api/ehf/circadian', methods=['GET'])
        def circadian():
            """Get circadian phase and recommendations"""
            phase = self.ehf_engine.circadian.get_circadian_phase()
            return jsonify({
                'current_phase': phase.value,
                'cortisol_expected': round(self.ehf_engine.circadian.get_cortisol_level(), 1),
                'melatonin_expected': round(self.ehf_engine.circadian.get_melatonin_level(), 1),
                'sleep_window': self.ehf_engine.circadian.get_optimal_sleep_time(),
                'recommendations': self.ehf_engine.get_recommendations(),
            }), 200

        @self.app.route('/api/ehf/cognitive-state', methods=['GET'])
        def cognitive_state():
            """Get optimal cognitive state"""
            state = self.ehf_engine.get_cognitive_state()
            frequency = self.ehf_engine.get_optimal_frequency(state)
            return jsonify({
                'cognitive_state': state.value,
                'optimal_frequency': f"{frequency} Hz",
                'frequency_band': self._get_frequency_band(frequency),
                'brain_wave_activity': self._get_brain_waves(state),
            }), 200

        @self.app.route('/api/ehf/recommendations', methods=['GET'])
        def recommendations():
            """Get personalized recommendations"""
            return jsonify({
                'timestamp': datetime.now().isoformat(),
                'recommendations': self.ehf_engine.get_recommendations(),
                'priority': self._prioritize_recommendations(self.ehf_engine.get_recommendations()),
            }), 200

        @self.app.route('/api/ehf/alignment', methods=['GET'])
        def alignment():
            """Get EHF-TRON alignment status"""
            metrics = self.ehf_engine.current_metrics
            alignment_result = {
                'alignment_score': self.alignment.alignment_score,
                'synchronization': self.alignment.synchronization_accuracy,
                'decision_window': self.alignment.get_optimal_decision_window(),
                'readiness': self.alignment.get_system_readiness(),
            }
            return jsonify(alignment_result), 200

        @self.app.route('/api/ehf/ui-complexity', methods=['GET'])
        def ui_complexity():
            """Get optimal UI complexity"""
            return jsonify(self.ui_optimizer.get_optimal_ui_complexity()), 200

        @self.app.route('/api/ehf/focus-mode', methods=['GET'])
        def focus_mode():
            """Get focus mode settings"""
            return jsonify(self.ui_optimizer.get_focus_mode_settings()), 200

        @self.app.route('/api/ehf/dashboard', methods=['GET'])
        def dashboard():
            """Get complete dashboard data"""
            return jsonify({
                'timestamp': datetime.now().isoformat(),
                'performance': self.ehf_engine.analyze_biometrics(),
                'status': self.ehf_engine.get_ehf_status(),
                'recommendations': self.ehf_engine.get_recommendations(),
                'readiness': self.alignment.get_system_readiness(),
                'ui_config': self.ui_optimizer.get_optimal_ui_complexity(),
            }), 200

    def _get_frequency_band(self, frequency: float) -> str:
        """Get frequency band description"""
        if frequency <= 4:
            return "Delta (0.5-4 Hz) - Deep sleep, recovery"
        elif frequency <= 8:
            return "Theta (4-8 Hz) - Deep work, meditation"
        elif frequency <= 12:
            return "Alpha (8-12 Hz) - Relaxed focus, creative"
        elif frequency <= 30:
            return "Beta (12-30 Hz) - Analytical, problem-solving"
        else:
            return "Gamma (30+ Hz) - Peak focus, insight"
    
    def _get_brain_waves(self, state) -> Dict:
        """Get brain wave characteristics"""
        waves = {
            'delta': 0,
            'theta': 0,
            'alpha': 0,
            'beta': 0,
            'gamma': 0,
        }
        
        state_waves = {
            'peak_focus': {'beta': 60, 'alpha': 30, 'gamma': 10},
            'deep_work': {'theta': 70, 'alpha': 20, 'delta': 10},
            'creative': {'beta': 50, 'alpha': 30, 'gamma': 20},
            'recovery': {'delta': 60, 'theta': 30, 'alpha': 10},
            'relaxed': {'alpha': 80, 'beta': 15, 'theta': 5},
            'sleep': {'delta': 60, 'theta': 30, 'alpha': 10},
        }
        
        state_key = state.value.lower().replace('_', '_')
        for key, val in state_waves.get(state_key, {}).items():
            waves[key] = val
        
        return waves
    
    def _prioritize_recommendations(self, recs: list) -> list:
        """Prioritize recommendations by importance"""
        priority_order = {
            '🛏️': 1,    # Sleep
            '💧': 2,    # Hydration
            '🧘': 3,    # Stress management
            '⚡': 4,    # Energy
            '☀️': 5,    # Light exposure
            '🍎': 6,    # Nutrition
            '🎯': 7,    # Focus
        }
        
        def get_priority(rec):
            for symbol, priority in priority_order.items():
                if rec.startswith(symbol):
                    return priority
            return 99
        
        return sorted(recs, key=get_priority)

    def run(self, host='0.0.0.0', port=9001, debug=False):
        """Run the EHF dashboard API"""
        print(f"\n[EHF] Efficient Human Frequency Dashboard")
        print(f"[EHF] Listening on http://{host}:{port}")
        print(f"[EHF] API Endpoints:")
        print(f"  GET /api/ehf/status              - Complete EHF status")
        print(f"  GET /api/ehf/performance         - Performance metrics")
        print(f"  GET /api/ehf/biomarkers          - Current biomarkers")
        print(f"  POST /api/ehf/biomarkers         - Update biomarkers")
        print(f"  GET /api/ehf/circadian           - Circadian phase & timing")
        print(f"  GET /api/ehf/cognitive-state     - Brain waves & frequency")
        print(f"  GET /api/ehf/recommendations     - Personalized recommendations")
        print(f"  GET /api/ehf/alignment           - EHF-TRON alignment")
        print(f"  GET /api/ehf/ui-complexity       - Optimal UI config")
        print(f"  GET /api/ehf/focus-mode          - Focus mode settings")
        print(f"  GET /api/ehf/dashboard           - Complete dashboard")
        print(f"\n")
        
        self.app.run(host=host, port=port, debug=debug)


# EHF Dashboard HTML
EHF_DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>EHF - Efficient Human Frequency Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%);
            color: #e0e0e0;
            padding: 20px;
        }
        .container { max-width: 1600px; margin: 0 auto; }
        h1 {
            text-align: center;
            color: #4ade80;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(20, 30, 20, 0.8);
            border: 2px solid #4ade80;
            border-radius: 8px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        .card h2 {
            color: #4ade80;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(74, 222, 128, 0.2);
        }
        .metric:last-child { border-bottom: none; }
        .metric-label { color: #a0a0a0; }
        .metric-value { 
            color: #4ade80;
            font-weight: bold;
            font-family: monospace;
        }
        .status {
            padding: 12px;
            border-radius: 4px;
            text-align: center;
            font-weight: bold;
            margin: 10px 0;
        }
        .status.optimal { background: #1e4620; color: #4ade80; }
        .status.good { background: #2d5a3d; color: #86efac; }
        .status.fair { background: #663300; color: #fbbf24; }
        .status.poor { background: #7f1d1d; color: #fca5a5; }
        .progress {
            width: 100%;
            height: 8px;
            background: #2d5a3d;
            border-radius: 4px;
            overflow: hidden;
            margin: 5px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4ade80 0%, #86efac 100%);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 EHF - Efficient Human Frequency</h1>
        
        <div class="grid" id="dashboard">
            <div class="card">
                <h2>Performance Score</h2>
                <div id="performance">Loading...</div>
            </div>
            
            <div class="card">
                <h2>Circadian Phase</h2>
                <div id="circadian">Loading...</div>
            </div>
            
            <div class="card">
                <h2>Cognitive State</h2>
                <div id="cognitive">Loading...</div>
            </div>
            
            <div class="card">
                <h2>System Readiness</h2>
                <div id="readiness">Loading...</div>
            </div>
            
            <div class="card">
                <h2>Biomarkers</h2>
                <div id="biomarkers">Loading...</div>
            </div>
            
            <div class="card">
                <h2>Recommendations</h2>
                <div id="recommendations">Loading...</div>
            </div>
        </div>
    </div>
    
    <script>
        async function updateDashboard() {
            try {
                const status = await fetch('/api/ehf/status').then(r => r.json());
                const perf = await fetch('/api/ehf/performance').then(r => r.json());
                const readiness = await fetch('/api/ehf/alignment').then(r => r.json());
                
                // Performance
                const perfHtml = `
                    <div class="metric">
                        <span class="metric-label">Overall Score</span>
                        <span class="metric-value">${perf.analysis.overall_performance.toFixed(1)}%</span>
                    </div>
                    <div class="progress">
                        <div class="progress-fill" style="width: ${perf.analysis.overall_performance}%"></div>
                    </div>
                    <div class="status ${getStatusClass(perf.analysis.overall_performance)}">
                        ${perf.analysis.status}
                    </div>
                `;
                document.getElementById('performance').innerHTML = perfHtml;
                
                // Circadian
                const circHtml = `
                    <div class="metric">
                        <span class="metric-label">Phase</span>
                        <span class="metric-value">${status.circadian_phase}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Frequency</span>
                        <span class="metric-value">${status.optimal_frequency}</span>
                    </div>
                `;
                document.getElementById('circadian').innerHTML = circHtml;
                
                // Cognitive
                const cogHtml = `
                    <div class="metric">
                        <span class="metric-label">State</span>
                        <span class="metric-value">${status.cognitive_state}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Optimal Frequency</span>
                        <span class="metric-value">${status.optimal_frequency}</span>
                    </div>
                `;
                document.getElementById('cognitive').innerHTML = cogHtml;
                
                // Readiness
                const readHtml = `
                    <div class="metric">
                        <span class="metric-label">Overall</span>
                        <span class="metric-value">${readiness.readiness.overall_readiness.toFixed(1)}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Status</span>
                        <span class="metric-value">${readiness.readiness.readiness_level}</span>
                    </div>
                `;
                document.getElementById('readiness').innerHTML = readHtml;
                
                // Biomarkers
                const bioHtml = `
                    <div class="metric">
                        <span class="metric-label">Heart Rate</span>
                        <span class="metric-value">${perf.metrics.heart_rate} BPM</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">HRV</span>
                        <span class="metric-value">${perf.metrics.heart_rate_variability.toFixed(1)} ms</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Stress</span>
                        <span class="metric-value">${perf.metrics.stress_score.toFixed(0)}/100</span>
                    </div>
                `;
                document.getElementById('biomarkers').innerHTML = bioHtml;
                
                // Recommendations
                const recHtml = status.recommendations.slice(0, 3).map(r => 
                    `<div style="padding: 5px 0; font-size: 0.9em;">${r}</div>`
                ).join('');
                document.getElementById('recommendations').innerHTML = recHtml;
                
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        function getStatusClass(score) {
            if (score >= 85) return 'optimal';
            if (score >= 70) return 'good';
            if (score >= 50) return 'fair';
            return 'poor';
        }
        
        updateDashboard();
        setInterval(updateDashboard, 10000);
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    dashboard = EHFDashboardAPI()
    dashboard.run(host='0.0.0.0', port=9001)
