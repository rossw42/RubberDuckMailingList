#!/usr/bin/env python3
"""
Startup script for Spam Response App
Simple launcher with error handling
"""

import sys
import os

def main():
    """Launch the spam response application"""
    try:
        from main import SpamResponseApp
        print("🚀 Starting Spam Response Assistant...")
        app = SpamResponseApp()
        app.run()
    except ImportError as e:
        print(f"❌ Error: Missing dependencies - {e}")
        print("Make sure you're running Python 3.6 or later")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 App closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()