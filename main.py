#!/usr/bin/env python3
"""
Main entry point for Claude Optimization Suite
"""

import os
import sys
from claude_optimizer import ClaudeOptimizer, RevenueGenerator, WorkflowAutomation
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""

    # Get API key from environment
    api_key = os.getenv("CLAUDE_API_KEY")

    if not api_key:
        logger.error("CLAUDE_API_KEY environment variable not set")
        logger.info("Please set your API key: export CLAUDE_API_KEY='your-key-here'")
        sys.exit(1)

    # Initialize optimizer
    optimizer = ClaudeOptimizer(api_key)

    # Example usage
    print("🚀 Claude Optimization Suite - Ready!")
    print("\nTesting connection to Claude API...")

    try:
        response = optimizer.send_message("Hello! Please respond with 'OK' if you're working.")
        print(f"✅ Connection successful!")
        print(f"Response: {response['content'][0]['text'][:100]}...")

        # Show performance stats
        stats = optimizer.analyze_performance()
        print(f"\n📊 Performance Stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()