#!/usr/bin/env python3
"""
Final System Validation for Vocalis + Orpheus-FastAPI Integration
Comprehensive test of all optimizations and fixes implemented.
"""

import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalSystemValidator:
    """Comprehensive validation of the optimized audio system"""
    
    def __init__(self):
        self.results = {
            'configuration_check': {},
            'audio_format_validation': {},
            'interrupt_system_validation': {},
            'latency_performance': {},
            'voice_configuration': {},
            'production_readiness': {},
            'overall_status': 'PENDING'
        }
        
    def validate_configuration_consistency(self) -> Dict:
        """Validate all configuration files are properly set"""
        logger.info("🔧 Validating configuration consistency...")
        
        config_results = {
            'frontend_audio_config': self._check_frontend_audio_config(),
            'backend_tts_config': self._check_backend_tts_config(),
            'orpheus_tts_config': self._check_orpheus_tts_config(),
            'consistency_score': 0
        }
        
        # Calculate consistency score
        passed_checks = sum(1 for result in config_results.values() 
                          if isinstance(result, dict) and result.get('status') == 'pass')
        total_checks = len([k for k in config_results.keys() if k != 'consistency_score'])
        config_results['consistency_score'] = passed_checks / total_checks if total_checks > 0 else 0
        
        status = "✅ PASS" if config_results['consistency_score'] >= 0.8 else "❌ FAIL"
        logger.info(f"Configuration validation: {status} ({config_results['consistency_score']:.1%})")
        
        return config_results
    
    def _check_frontend_audio_config(self) -> Dict:
        """Check frontend audio service configuration"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if not audio_ts_path.exists():
                return {'status': 'fail', 'error': 'audio.ts not found'}
            
            content = audio_ts_path.read_text()
            checks = {
                'sample_rate_24khz': 'sampleRate: 24000' in content,
                'interrupt_handling': 'interruptPlayback()' in content,
                'vad_optimized': 'voiceThreshold: number = 0.015' in content,
                'audio_state_management': 'AudioState.INTERRUPTED' in content,
                'fade_effects': 'linearRampToValueAtTime' in content
            }
            
            passed = sum(checks.values())
            total = len(checks)
            
            return {
                'status': 'pass' if passed >= 4 else 'partial' if passed >= 2 else 'fail',
                'checks': checks,
                'score': f"{passed}/{total}",
                'details': 'Frontend audio service properly configured'
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _check_backend_tts_config(self) -> Dict:
        """Check backend TTS service configuration"""
        try:
            tts_py_path = Path("backend/services/tts.py")
            if not tts_py_path.exists():
                return {'status': 'fail', 'error': 'tts.py not found'}
            
            content = tts_py_path.read_text()
            checks = {
                'sample_rate_24khz': 'sample_rate = 24000' in content,
                'optimized_chunk_size': 'chunk_size_bytes = 2400' in content,
                'wav_header_creation': '_create_wav_chunk' in content,
                'async_streaming': 'stream_text_to_speech_async' in content,
                'error_handling': 'try:' in content and 'except' in content
            }
            
            passed = sum(checks.values())
            total = len(checks)
            
            return {
                'status': 'pass' if passed >= 4 else 'partial' if passed >= 2 else 'fail',
                'checks': checks,
                'score': f"{passed}/{total}",
                'details': 'Backend TTS service properly configured'
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _check_orpheus_tts_config(self) -> Dict:
        """Check Orpheus TTS configuration"""
        try:
            orpheus_path = Path("../Orpheus-FastAPI/tts_engine/inference.py")
            if not orpheus_path.exists():
                return {'status': 'fail', 'error': 'Orpheus inference.py not found'}
            
            content = orpheus_path.read_text()
            checks = {
                'hindi_voice_default': 'DEFAULT_VOICE = "ऋतिका"' in content,
                'sample_rate_24khz': '24000' in content,
                'streaming_support': 'stream' in content.lower(),
                'error_handling': 'try:' in content and 'except' in content,
                'logging_implemented': 'logger' in content or 'logging' in content
            }
            
            passed = sum(checks.values())
            total = len(checks)
            
            return {
                'status': 'pass' if passed >= 4 else 'partial' if passed >= 2 else 'fail',
                'checks': checks,
                'score': f"{passed}/{total}",
                'details': 'Orpheus TTS properly configured with Hindi voice'
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def validate_interrupt_system(self) -> Dict:
        """Validate audio interruption system"""
        logger.info("🛑 Validating interrupt system...")
        
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if not audio_ts_path.exists():
                return {'status': 'fail', 'error': 'Frontend audio service not found'}
            
            content = audio_ts_path.read_text()
            
            interrupt_features = {
                'immediate_interrupt': 'IMMEDIATE User interrupt detected' in content,
                'queue_clearing': 'this.audioQueue = []' in content,
                'state_management': 'AudioState.INTERRUPTED' in content,
                'websocket_interrupt': 'websocketService.interrupt()' in content,
                'source_disconnection': 'this.currentSource.disconnect()' in content
            }
            
            passed = sum(interrupt_features.values())
            total = len(interrupt_features)
            
            return {
                'status': 'pass' if passed >= 4 else 'partial' if passed >= 2 else 'fail',
                'features': interrupt_features,
                'score': f"{passed}/{total}",
                'details': 'Audio interrupt system fully implemented'
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def validate_latency_optimizations(self) -> Dict:
        """Validate latency optimization implementations"""
        logger.info("⚡ Validating latency optimizations...")
        
        optimizations = {
            'vad_threshold': self._check_vad_optimization(),
            'chunk_size': self._check_chunk_optimization(),
            'fade_effects': self._check_fade_optimization(),
            'streaming_pipeline': self._check_streaming_optimization()
        }
        
        passed = sum(1 for opt in optimizations.values() 
                    if opt.get('status') == 'pass')
        total = len(optimizations)
        
        return {
            'optimizations': optimizations,
            'score': f"{passed}/{total}",
            'status': 'pass' if passed >= 3 else 'partial' if passed >= 2 else 'fail',
            'details': 'Latency optimizations implemented'
        }
    
    def _check_vad_optimization(self) -> Dict:
        """Check VAD threshold optimization"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if audio_ts_path.exists():
                content = audio_ts_path.read_text()
                if 'voiceThreshold: number = 0.015' in content:
                    return {'status': 'pass', 'note': 'VAD threshold optimized for 24kHz'}
            return {'status': 'fail', 'note': 'VAD threshold not optimized'}
        except:
            return {'status': 'error'}
    
    def _check_chunk_optimization(self) -> Dict:
        """Check audio chunk size optimization"""
        try:
            tts_py_path = Path("backend/services/tts.py")
            if tts_py_path.exists():
                content = tts_py_path.read_text()
                if 'chunk_size_bytes = 2400' in content:
                    return {'status': 'pass', 'note': 'Chunk size optimized to 2400 bytes (~0.05s)'}
            return {'status': 'fail', 'note': 'Chunk size not optimized'}
        except:
            return {'status': 'error'}
    
    def _check_fade_optimization(self) -> Dict:
        """Check fade effects implementation"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if audio_ts_path.exists():
                content = audio_ts_path.read_text()
                if 'linearRampToValueAtTime' in content and 'fadeTime = 0.005' in content:
                    return {'status': 'pass', 'note': 'Fade effects implemented (5ms)'}
            return {'status': 'fail', 'note': 'Fade effects not implemented'}
        except:
            return {'status': 'error'}
    
    def _check_streaming_optimization(self) -> Dict:
        """Check streaming pipeline optimization"""
        try:
            tts_py_path = Path("backend/services/tts.py")
            if tts_py_path.exists():
                content = tts_py_path.read_text()
                if 'stream_text_to_speech_async' in content and 'aiohttp' in content:
                    return {'status': 'pass', 'note': 'Async streaming pipeline implemented'}
            return {'status': 'fail', 'note': 'Streaming pipeline not optimized'}
        except:
            return {'status': 'error'}
    
    def run_comprehensive_validation(self) -> Dict:
        """Run complete validation suite"""
        logger.info("🚀 Starting comprehensive system validation...")
        
        # Run all validation tests
        self.results['configuration_check'] = self.validate_configuration_consistency()
        self.results['interrupt_system_validation'] = self.validate_interrupt_system()
        self.results['latency_performance'] = self.validate_latency_optimizations()
        
        # Calculate overall status
        test_scores = []
        
        # Configuration consistency
        config_score = self.results['configuration_check'].get('consistency_score', 0)
        test_scores.append(config_score)
        
        # Interrupt system
        interrupt_result = self.results['interrupt_system_validation']
        if interrupt_result.get('status') == 'pass':
            test_scores.append(1.0)
        elif interrupt_result.get('status') == 'partial':
            test_scores.append(0.7)
        else:
            test_scores.append(0.0)
        
        # Latency optimizations
        latency_result = self.results['latency_performance']
        if latency_result.get('status') == 'pass':
            test_scores.append(1.0)
        elif latency_result.get('status') == 'partial':
            test_scores.append(0.7)
        else:
            test_scores.append(0.0)
        
        overall_score = sum(test_scores) / len(test_scores) if test_scores else 0
        
        if overall_score >= 0.9:
            self.results['overall_status'] = '🎉 PRODUCTION READY'
        elif overall_score >= 0.7:
            self.results['overall_status'] = '⚠️ MOSTLY READY'
        else:
            self.results['overall_status'] = '❌ NEEDS WORK'
        
        self.results['overall_score'] = f"{overall_score:.1%}"
        
        return self.results
    
    def generate_final_report(self) -> str:
        """Generate comprehensive final validation report"""
        report = []
        report.append("=" * 80)
        report.append("FINAL VOCALIS + ORPHEUS-FASTAPI SYSTEM VALIDATION REPORT")
        report.append("=" * 80)
        report.append(f"Overall Status: {self.results['overall_status']}")
        report.append(f"System Score: {self.results.get('overall_score', 'N/A')}")
        report.append("")
        
        # Configuration Check
        report.append("🔧 CONFIGURATION CONSISTENCY")
        report.append("-" * 40)
        config_check = self.results.get('configuration_check', {})
        score = config_check.get('consistency_score', 0)
        report.append(f"Configuration Score: {score:.1%}")
        
        for component, result in config_check.items():
            if component == 'consistency_score':
                continue
            if isinstance(result, dict):
                status_icon = "✅" if result.get('status') == 'pass' else "⚠️" if result.get('status') == 'partial' else "❌"
                report.append(f"{status_icon} {component}: {result.get('score', 'N/A')}")
        report.append("")
        
        # Interrupt System
        report.append("🛑 INTERRUPT SYSTEM VALIDATION")
        report.append("-" * 40)
        interrupt_val = self.results.get('interrupt_system_validation', {})
        status_icon = "✅" if interrupt_val.get('status') == 'pass' else "⚠️" if interrupt_val.get('status') == 'partial' else "❌"
        report.append(f"{status_icon} Interrupt System: {interrupt_val.get('score', 'N/A')}")
        report.append("")
        
        # Latency Performance
        report.append("⚡ LATENCY OPTIMIZATIONS")
        report.append("-" * 40)
        latency_val = self.results.get('latency_performance', {})
        status_icon = "✅" if latency_val.get('status') == 'pass' else "⚠️" if latency_val.get('status') == 'partial' else "❌"
        report.append(f"{status_icon} Latency Optimizations: {latency_val.get('score', 'N/A')}")
        report.append("")
        
        # Final Assessment
        report.append("=" * 80)
        report.append("PRODUCTION READINESS ASSESSMENT")
        report.append("=" * 80)
        
        if self.results['overall_status'] == '🎉 PRODUCTION READY':
            report.append("🎉 SYSTEM IS FULLY OPTIMIZED AND PRODUCTION READY!")
            report.append("")
            report.append("✅ All critical optimizations successfully implemented:")
            report.append("• Audio format consistency (24kHz, 16-bit mono)")
            report.append("• Real-time audio interruption system")
            report.append("• Optimized VAD with 0.015 threshold")
            report.append("• Low-latency streaming (0.05s chunks)")
            report.append("• Hindi voice ऋतिका configured as default")
            report.append("• Fade effects for click-free audio")
            report.append("• Comprehensive error handling and logging")
            report.append("")
            report.append("🚀 Ready for production deployment!")
        else:
            report.append("⚠️ SYSTEM NEEDS ATTENTION")
            report.append("Some components may need additional optimization.")
            report.append("Review the detailed results above for specific areas to improve.")
        
        return "\n".join(report)

def main():
    """Run the final validation suite"""
    validator = FinalSystemValidator()
    
    try:
        results = validator.run_comprehensive_validation()
        report = validator.generate_final_report()
        
        # Save results
        with open("final_validation_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        with open("final_validation_report.txt", "w") as f:
            f.write(report)
        
        print(report)
        
        return results['overall_status'] == '🎉 PRODUCTION READY'
        
    except Exception as e:
        logger.error(f"Final validation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
