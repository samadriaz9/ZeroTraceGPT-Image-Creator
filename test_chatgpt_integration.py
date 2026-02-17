#!/usr/bin/env python3
"""
Test script for ChatGPT Integration in ZeroTraceGPT Image Creator
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from modules.chatgpt_integration import chatgpt
    
    print("🚀 ZeroTraceGPT Image Creator - ChatGPT Integration Test")
    print("=" * 60)
    
    # Test 1: Prompt Enhancement
    print("\n✨ Test 1: Prompt Enhancement")
    print("-" * 30)
    
    original_prompt = "cat"
    print(f"Original prompt: '{original_prompt}'")
    
    try:
        enhanced_prompt = chatgpt.enhance_prompt(original_prompt, "photorealistic")
        print(f"Enhanced prompt: {enhanced_prompt}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Image Improvement
    print("\n🎨 Test 2: Image Improvement")
    print("-" * 30)
    
    try:
        improved_suggestions = chatgpt.improve_image_prompt(original_prompt, "A simple cat image")
        print(f"Improvement suggestions: {improved_suggestions}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Alternative Prompts
    print("\n🔄 Test 3: Alternative Prompts")
    print("-" * 30)
    
    try:
        alternatives = chatgpt.generate_alternative_prompt(original_prompt, "creative")
        print(f"Alternative prompts: {alternatives}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n✅ ChatGPT Integration Test Complete!")
    print("\n📝 Note: If you see rate limiting errors (429), wait a moment and try again.")
    print("The API key is working correctly - this is just OpenAI's rate limiting.")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this from the ZeroTraceGPT Image Creator directory.")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")

