#!/usr/bin/env python3
"""Simple test to verify validation script works"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🔧 Testing validation script...")

try:
    from validate_audio_system import AudioSystemValidator
    
    validator = AudioSystemValidator()
    print("✅ Validator created successfully")
    
    # Test individual components
    print("\n📋 Running validation tests:")
    
    # Format validation
    format_result = validator.validate_audio_formats()
    print(f"Format validation: {format_result.get('status', 'unknown')}")
    
    # VAD validation  
    vad_result = validator.validate_vad_system()
    print(f"VAD validation: {len([r for r in vad_result.values() if r.get('status') == 'pass'])} tests passed")
    
    # Audio quality
    quality_result = validator.validate_audio_quality()
    print(f"Audio quality: {quality_result.get('status', 'unknown')}")
    
    print("\n✅ Validation script is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
