#!/usr/bin/env python3
"""
Test script for ChatGPT Rate Limiting in ZeroTraceGPT Image Creator
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from modules.chatgpt_integration import chatgpt
    
    print("🚀 ZeroTraceGPT Image Creator - Rate Limiting Test")
    print("=" * 60)
    
    # Test rate limiting protection
    print("\n⏱️ Testing Rate Limiting Protection")
    print("-" * 40)
    
    test_prompts = ["cat", "dog", "landscape", "portrait", "abstract"]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}/5: Enhancing prompt '{prompt}'")
        start_time = time.time()
        
        try:
            result = chatgpt.enhance_prompt(prompt, "photorealistic")
            end_time = time.time()
            
            if "Rate limited" in result:
                print(f"⚠️ Rate limited: {result}")
                print("⏳ Waiting 30 seconds before next attempt...")
                time.sleep(30)
                # Retry once
                result = chatgpt.enhance_prompt(prompt, "photorealistic")
                end_time = time.time()
            
            if "Error" in result:
                print(f"❌ Error: {result}")
            else:
                print(f"✅ Success: {result[:100]}...")
            
            elapsed = end_time - start_time
            print(f"⏱️ Time elapsed: {elapsed:.2f} seconds")
            
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Small delay between requests
        if i < len(test_prompts):
            print("⏳ Waiting 3 seconds before next request...")
            time.sleep(3)
    
    print("\n✅ Rate Limiting Test Complete!")
    print("\n📝 Tips for avoiding rate limits:")
    print("   • Wait 2-3 seconds between requests")
    print("   • Don't spam the enhance button")
    print("   • Use the built-in rate limiting protection")
    print("   • If you get 429 errors, wait 1-2 minutes")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this from the ZeroTraceGPT Image Creator directory.")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")

