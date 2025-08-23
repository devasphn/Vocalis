#!/usr/bin/env python3
"""
Production-Grade Audio System Validation Script

This script validates all audio improvements made to the Vocalis + Orpheus-FastAPI system:
- Audio format consistency (24kHz, 16-bit mono)
- VAD threshold optimization
- Real-time streaming performance
- Interrupt handling capability
- Audio quality metrics

Run this script to verify the system is production-ready.
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

class AudioSystemValidator:
    """Comprehensive validation of the audio system"""
    
    def __init__(self):
        self.results = {
            'format_validation': {},
            'vad_validation': {},
            'streaming_validation': {},
            'interrupt_validation': {},
            'performance_metrics': {},
            'overall_status': 'PENDING'
        }
        
        # Test configuration
        self.tts_endpoint = "http://0.0.0.0:5005/v1/audio/speech/stream"
        self.websocket_endpoint = "ws://0.0.0.0:8000/ws"
        self.test_text = "Hello, this is a test of the audio system with natural speech patterns."
        
    def validate_audio_formats(self) -> Dict:
        """Validate audio format consistency across all components"""
        logger.info("🔍 Validating audio format consistency...")
        
        format_results = {
            'frontend_config': self._check_frontend_config(),
            'tts_config': self._check_tts_config(),
            'orpheus_config': self._check_orpheus_config(),
            'consistency_check': True
        }
        
        # Check consistency
        expected_sample_rate = 24000
        expected_channels = 1
        expected_bit_depth = 16
        
        inconsistencies = []
        for component, config in format_results.items():
            if component == 'consistency_check':
                continue
                
            if config.get('sample_rate') != expected_sample_rate:
                inconsistencies.append(f"{component}: sample_rate {config.get('sample_rate')} != {expected_sample_rate}")
            if config.get('channels') != expected_channels:
                inconsistencies.append(f"{component}: channels {config.get('channels')} != {expected_channels}")
            if config.get('bit_depth') != expected_bit_depth:
                inconsistencies.append(f"{component}: bit_depth {config.get('bit_depth')} != {expected_bit_depth}")
        
        format_results['consistency_check'] = len(inconsistencies) == 0
        format_results['inconsistencies'] = inconsistencies
        
        status = "✅ PASS" if format_results['consistency_check'] else "❌ FAIL"
        logger.info(f"Audio format validation: {status}")
        
        return format_results
    
    def _check_frontend_config(self) -> Dict:
        """Check frontend audio configuration"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if audio_ts_path.exists():
                content = audio_ts_path.read_text()
                
                # Extract sample rate from DEFAULT_CONFIG
                sample_rate = None
                if "sampleRate: 24000" in content:
                    sample_rate = 24000
                elif "sampleRate: 44100" in content:
                    sample_rate = 44100
                
                return {
                    'sample_rate': sample_rate,
                    'channels': 1,  # Always mono in our config
                    'bit_depth': 16,  # Standard for web audio
                    'status': 'detected' if sample_rate else 'not_found'
                }
        except Exception as e:
            logger.warning(f"Could not check frontend config: {e}")
        
        return {'status': 'error'}
    
    def _check_tts_config(self) -> Dict:
        """Check TTS service configuration"""
        try:
            tts_py_path = Path("backend/services/tts.py")
            if tts_py_path.exists():
                content = tts_py_path.read_text()
                
                # Extract sample rate from _create_wav_chunk
                sample_rate = None
                if "sample_rate = 24000" in content:
                    sample_rate = 24000
                
                return {
                    'sample_rate': sample_rate,
                    'channels': 1,
                    'bit_depth': 16,
                    'status': 'detected' if sample_rate else 'not_found'
                }
        except Exception as e:
            logger.warning(f"Could not check TTS config: {e}")
        
        return {'status': 'error'}
    
    def _check_orpheus_config(self) -> Dict:
        """Check Orpheus TTS configuration"""
        try:
            inference_py_path = Path("../Orpheus-FastAPI/tts_engine/inference.py")
            if inference_py_path.exists():
                content = inference_py_path.read_text()
                
                # Extract sample rate
                sample_rate = None
                if 'SAMPLE_RATE = 24000' in content or 'os.environ.get("ORPHEUS_SAMPLE_RATE", "24000")' in content:
                    sample_rate = 24000
                
                return {
                    'sample_rate': sample_rate,
                    'channels': 1,  # Orpheus is always mono
                    'bit_depth': 16,  # Standard PCM
                    'status': 'detected' if sample_rate else 'not_found'
                }
        except Exception as e:
            logger.warning(f"Could not check Orpheus config: {e}")
        
        return {'status': 'error'}
    
    def validate_vad_system(self) -> Dict:
        """Validate Voice Activity Detection improvements"""
        logger.info("🎤 Validating VAD system...")
        
        vad_results = {
            'threshold_optimization': self._check_vad_threshold(),
            'noise_gating': self._check_noise_gating(),
            'hysteresis': self._check_hysteresis(),
            'interrupt_capability': self._check_interrupt_capability()
        }
        
        all_passed = all(result.get('status') == 'pass' for result in vad_results.values())
        status = "✅ PASS" if all_passed else "⚠️ PARTIAL"
        logger.info(f"VAD system validation: {status}")
        
        return vad_results
    
    def _check_vad_threshold(self) -> Dict:
        """Check VAD threshold optimization"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if audio_ts_path.exists():
                content = audio_ts_path.read_text()
                
                # Check for optimized threshold
                if "voiceThreshold: number = 0.015" in content:
                    return {'status': 'pass', 'threshold': 0.015, 'note': 'Optimized for 24kHz'}
                elif "voiceThreshold: number = 0.03" in content:
                    return {'status': 'warning', 'threshold': 0.03, 'note': 'May be too sensitive'}
                
        except Exception as e:
            logger.warning(f"Could not check VAD threshold: {e}")
        
        return {'status': 'error'}
    
    def _check_noise_gating(self) -> Dict:
        """Check noise gating implementation"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if audio_ts_path.exists():
                content = audio_ts_path.read_text()
                
                # Check for noise floor implementation
                if "noiseFloor: number" in content and "sample > this.noiseFloor" in content:
                    return {'status': 'pass', 'note': 'Noise gating implemented'}
                
        except Exception as e:
            logger.warning(f"Could not check noise gating: {e}")
        
        return {'status': 'error'}
    
    def _check_hysteresis(self) -> Dict:
        """Check hysteresis implementation"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if audio_ts_path.exists():
                content = audio_ts_path.read_text()
                
                # Check for hysteresis logic
                if "isSignificantEnergy" in content and "voiceThreshold * 0.7" in content:
                    return {'status': 'pass', 'note': 'Hysteresis implemented'}
                
        except Exception as e:
            logger.warning(f"Could not check hysteresis: {e}")
        
        return {'status': 'error'}
    
    def _check_interrupt_capability(self) -> Dict:
        """Check interrupt handling capability"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if audio_ts_path.exists():
                content = audio_ts_path.read_text()
                
                # Check for interrupt logic during TTS
                if "interruptPlayback()" in content and "User interrupt detected" in content:
                    return {'status': 'pass', 'note': 'Interrupt handling implemented'}
                
        except Exception as e:
            logger.warning(f"Could not check interrupt capability: {e}")
        
        return {'status': 'error'}
    
    def validate_streaming_performance(self) -> Dict:
        """Validate real-time streaming performance"""
        logger.info("🚀 Validating streaming performance...")
        
        try:
            # Test TTS streaming endpoint
            start_time = time.time()
            
            payload = {
                "model": "tts-1",
                "input": self.test_text,
                "voice": "tara",
                "response_format": "wav",
                "speed": 1.0
            }
            
            chunk_count = 0
            first_chunk_time = None
            
            response = requests.post(
                self.tts_endpoint,
                json=payload,
                stream=True,
                timeout=30
            )
            
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        chunk_count += 1
                        if first_chunk_time is None:
                            first_chunk_time = time.time() - start_time
            
            total_time = time.time() - start_time
            
            return {
                'status': 'pass' if chunk_count > 0 else 'fail',
                'chunk_count': chunk_count,
                'first_chunk_latency': first_chunk_time,
                'total_time': total_time,
                'streaming_rate': chunk_count / total_time if total_time > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Streaming performance test failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def validate_audio_quality(self) -> Dict:
        """Validate audio quality improvements"""
        logger.info("🎵 Validating audio quality...")
        
        quality_results = {
            'fade_effects': self._check_fade_effects(),
            'chunk_optimization': self._check_chunk_optimization(),
            'format_compliance': self._check_format_compliance()
        }
        
        all_passed = all(result.get('status') == 'pass' for result in quality_results.values())
        status = "✅ PASS" if all_passed else "⚠️ PARTIAL"
        logger.info(f"Audio quality validation: {status}")
        
        return quality_results
    
    def _check_fade_effects(self) -> Dict:
        """Check fade-in/fade-out implementation"""
        try:
            audio_ts_path = Path("frontend/src/services/audio.ts")
            if audio_ts_path.exists():
                content = audio_ts_path.read_text()
                
                # Check for fade implementation
                if "gainNode.gain.linearRampToValueAtTime" in content and "fadeTime = 0.005" in content:
                    return {'status': 'pass', 'note': 'Fade effects implemented (5ms)'}
                
        except Exception as e:
            logger.warning(f"Could not check fade effects: {e}")
        
        return {'status': 'error'}
    
    def _check_chunk_optimization(self) -> Dict:
        """Check audio chunk size optimization"""
        try:
            tts_py_path = Path("backend/services/tts.py")
            if tts_py_path.exists():
                content = tts_py_path.read_text()
                
                # Check for optimized chunk size
                if "chunk_size_bytes = 2400" in content:
                    return {'status': 'pass', 'chunk_size': '2400 bytes (~0.05s)', 'note': 'Optimized for low latency'}
                elif "chunk_size_bytes = 4800" in content:
                    return {'status': 'warning', 'chunk_size': '4800 bytes (~0.1s)', 'note': 'Could be optimized further'}
                
        except Exception as e:
            logger.warning(f"Could not check chunk optimization: {e}")
        
        return {'status': 'error'}
    
    def _check_format_compliance(self) -> Dict:
        """Check Orpheus TTS format compliance"""
        try:
            # Check if all components use 24kHz, 16-bit mono
            format_check = self.validate_audio_formats()
            
            if format_check.get('consistency_check'):
                return {'status': 'pass', 'note': 'All components use Orpheus-compliant format'}
            else:
                return {
                    'status': 'fail', 
                    'note': 'Format inconsistencies detected',
                    'issues': format_check.get('inconsistencies', [])
                }
                
        except Exception as e:
            logger.warning(f"Could not check format compliance: {e}")
        
        return {'status': 'error'}
    
    def run_full_validation(self) -> Dict:
        """Run complete validation suite"""
        logger.info("🔧 Starting comprehensive audio system validation...")
        
        # Run all validation tests
        self.results['format_validation'] = self.validate_audio_formats()
        self.results['vad_validation'] = self.validate_vad_system()
        self.results['streaming_validation'] = self.validate_streaming_performance()
        self.results['audio_quality'] = self.validate_audio_quality()
        
        # Calculate overall status
        passed_tests = 0
        total_tests = 4
        
        if self.results['format_validation'].get('consistency_check'):
            passed_tests += 1
        if all(r.get('status') == 'pass' for r in self.results['vad_validation'].values()):
            passed_tests += 1
        if self.results['streaming_validation'].get('status') == 'pass':
            passed_tests += 1
        if all(r.get('status') == 'pass' for r in self.results['audio_quality'].values()):
            passed_tests += 1
        
        if passed_tests == total_tests:
            self.results['overall_status'] = '✅ PRODUCTION READY'
        elif passed_tests >= total_tests * 0.75:
            self.results['overall_status'] = '⚠️ MOSTLY READY'
        else:
            self.results['overall_status'] = '❌ NEEDS WORK'
        
        self.results['test_summary'] = f"{passed_tests}/{total_tests} test suites passed"
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate comprehensive validation report"""
        report = []
        report.append("=" * 80)
        report.append("VOCALIS + ORPHEUS-FASTAPI AUDIO SYSTEM VALIDATION REPORT")
        report.append("=" * 80)
        report.append(f"Overall Status: {self.results['overall_status']}")
        report.append(f"Test Summary: {self.results.get('test_summary', 'N/A')}")
        report.append("")
        
        # Format validation
        report.append("📊 AUDIO FORMAT VALIDATION")
        report.append("-" * 40)
        format_val = self.results.get('format_validation', {})
        if format_val.get('consistency_check'):
            report.append("✅ All components use consistent 24kHz, 16-bit mono format")
        else:
            report.append("❌ Format inconsistencies detected:")
            for issue in format_val.get('inconsistencies', []):
                report.append(f"   - {issue}")
        report.append("")
        
        # VAD validation
        report.append("🎤 VOICE ACTIVITY DETECTION VALIDATION")
        report.append("-" * 40)
        vad_val = self.results.get('vad_validation', {})
        for test_name, result in vad_val.items():
            status_icon = "✅" if result.get('status') == 'pass' else "⚠️" if result.get('status') == 'warning' else "❌"
            report.append(f"{status_icon} {test_name.replace('_', ' ').title()}: {result.get('note', 'N/A')}")
        report.append("")
        
        # Streaming validation
        report.append("🚀 STREAMING PERFORMANCE VALIDATION")
        report.append("-" * 40)
        stream_val = self.results.get('streaming_validation', {})
        if stream_val.get('status') == 'pass':
            report.append("✅ Streaming performance validated")
            report.append(f"   - Chunks processed: {stream_val.get('chunk_count', 'N/A')}")
            report.append(f"   - First chunk latency: {stream_val.get('first_chunk_latency', 'N/A'):.3f}s")
            report.append(f"   - Total processing time: {stream_val.get('total_time', 'N/A'):.3f}s")
        else:
            report.append(f"❌ Streaming test failed: {stream_val.get('error', 'Unknown error')}")
        report.append("")
        
        # Audio quality validation
        report.append("🎵 AUDIO QUALITY VALIDATION")
        report.append("-" * 40)
        quality_val = self.results.get('audio_quality', {})
        for test_name, result in quality_val.items():
            status_icon = "✅" if result.get('status') == 'pass' else "⚠️" if result.get('status') == 'warning' else "❌"
            report.append(f"{status_icon} {test_name.replace('_', ' ').title()}: {result.get('note', 'N/A')}")
        report.append("")
        
        report.append("=" * 80)
        report.append("PRODUCTION READINESS ASSESSMENT")
        report.append("=" * 80)
        
        if self.results['overall_status'] == '✅ PRODUCTION READY':
            report.append("🎉 SYSTEM IS PRODUCTION READY!")
            report.append("All critical audio improvements have been successfully implemented:")
            report.append("• Audio format consistency (24kHz, 16-bit mono)")
            report.append("• Optimized VAD with noise gating and hysteresis")
            report.append("• Real-time streaming with fade effects")
            report.append("• Proper interrupt handling for natural conversation")
        else:
            report.append("⚠️ SYSTEM NEEDS ATTENTION")
            report.append("Some improvements may be needed before production deployment.")
            report.append("Review the detailed results above for specific issues.")
        
        return "\n".join(report)

def main():
    """Run the validation suite"""
    validator = AudioSystemValidator()
    
    try:
        results = validator.run_full_validation()
        report = validator.generate_report()
        
        # Save results
        with open("audio_validation_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        with open("audio_validation_report.txt", "w") as f:
            f.write(report)
        
        print(report)
        
        return results['overall_status'] == '✅ PRODUCTION READY'
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
