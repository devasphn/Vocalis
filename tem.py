#!/usr/bin/env python3
"""Quick system status check"""

import json
import os
from pathlib import Path

def check_system_status():
    print('=== VOCALIS + ORPHEUS-FASTAPI SYSTEM STATUS ===\n')
    
    issues = []
    
    # Check frontend audio configuration
    frontend_path = Path('frontend/src/services/audio.ts')
    if frontend_path.exists():
        content = frontend_path.read_text()
        if 'sampleRate: 24000' in content:
            print('✅ Frontend: 24kHz sample rate configured')
        else:
            print('❌ Frontend: Sample rate needs verification')
            issues.append('Frontend sample rate')
        
        if 'interruptPlayback()' in content:
            print('✅ Frontend: Audio interruption implemented')
        else:
            print('❌ Frontend: Audio interruption missing')
            issues.append('Frontend interruption')
            
        if 'voiceThreshold: number = 0.015' in content:
            print('✅ Frontend: VAD threshold optimized (0.015)')
        else:
            print('⚠️ Frontend: VAD threshold may need optimization')
            issues.append('VAD threshold')
    else:
        print('❌ Frontend audio.ts not found')
        issues.append('Frontend file missing')

    # Check Orpheus configuration
    orpheus_path = Path('../Orpheus-FastAPI/tts_engine/inference.py')
    if orpheus_path.exists():
        content = orpheus_path.read_text()
        if 'DEFAULT_VOICE = "ऋतिका"' in content:
            print('✅ Orpheus: Hindi voice ऋतिका configured')
        else:
            print('❌ Orpheus: Voice needs verification')
            issues.append('Orpheus voice')
        
        if '24000' in content:
            print('✅ Orpheus: 24kHz sample rate configured')
        else:
            print('❌ Orpheus: Sample rate needs verification')
            issues.append('Orpheus sample rate')
    else:
        print('❌ Orpheus inference.py not found')
        issues.append('Orpheus file missing')

    # Check backend TTS service
    backend_tts_path = Path('backend/services/tts.py')
    if backend_tts_path.exists():
        content = backend_tts_path.read_text()
        if 'sample_rate = 24000' in content:
            print('✅ Backend: TTS service 24kHz configured')
        else:
            print('⚠️ Backend: TTS sample rate may need verification')
            issues.append('Backend TTS sample rate')
    else:
        print('❌ Backend TTS service not found')
        issues.append('Backend TTS missing')

    print(f'\n=== SUMMARY ===')
    if not issues:
        print('🎉 All critical components are properly configured!')
        print('System appears ready for production use.')
    else:
        print(f'⚠️ Found {len(issues)} potential issues:')
        for issue in issues:
            print(f'  - {issue}')
    
    return len(issues) == 0

if __name__ == "__main__":
    success = check_system_status()
    exit(0 if success else 1)
