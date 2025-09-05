#!/usr/bin/env python3
"""
Quick Spam Response - One-Click Integration
Automatically detects phone number from active Messages conversation
"""

import subprocess
import sys
import os

def get_active_messages_phone():
    """Get phone number from currently active Messages conversation"""
    
    applescript = '''
    tell application "Messages"
        try
            -- Get the frontmost conversation
            set activeChat to item 1 of chats
            
            -- Get the participants (phone numbers/emails)
            set participants to participants of activeChat
            
            -- Get the first participant that's not the current user
            repeat with participant in participants
                set participantID to id of participant
                -- Skip if it's the current user (usually starts with "mailto:" for iMessage)
                if participantID does not start with "mailto:" and length of participantID > 5 then
                    -- Clean up the phone number
                    set phoneNumber to participantID
                    
                    -- Remove common prefixes
                    if phoneNumber starts with "tel:" then
                        set phoneNumber to text 5 thru -1 of phoneNumber
                    end if
                    
                    return phoneNumber
                end if
            end repeat
            
            -- If no phone found, return the first participant anyway
            if (count of participants) > 0 then
                set firstParticipant to id of item 1 of participants
                if firstParticipant starts with "tel:" then
                    return text 5 thru -1 of firstParticipant
                else
                    return firstParticipant
                end if
            end if
            
            return "No active conversation found"
            
        on error errorMessage
            return "Error: " & errorMessage
        end try
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            phone = result.stdout.strip()
            if phone and not phone.startswith("Error:") and not phone.startswith("No active"):
                return phone
            else:
                return None
        else:
            return None
    except Exception:
        return None

def launch_spam_app_with_phone(phone_number):
    """Launch the spam response app with pre-filled phone number"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    launch_script = f'''
import sys
sys.path.append('{script_dir}')
from main import SpamResponseApp
import tkinter as tk

# Create app
app = SpamResponseApp()

# Pre-fill phone number  
app.phone_var.set('{phone_number}')
app.status_var.set('🎯 Auto-detected from Messages: {phone_number}')

# Focus on app and response selection
app.root.lift()
app.root.attributes('-topmost', True)
app.root.after_idle(app.root.attributes, '-topmost', False)

# Auto-select first duck response for even faster sending
if app.responses:
    app.response_listbox.selection_set(2)  # Select first duck response
    app.response_listbox.event_generate('<<ListboxSelect>>')
    app.response_listbox.focus_set()

app.run()
'''
    
    subprocess.Popen([sys.executable, '-c', launch_script])

def main():
    """Main quick response launcher"""
    print("🦆 Quick Spam Response - Detecting active Messages conversation...")
    
    # Get phone number from active Messages conversation
    phone = get_active_messages_phone()
    
    if phone:
        print(f"📱 Detected phone number: {phone}")
        print("🚀 Launching Spam Response App...")
        launch_spam_app_with_phone(phone)
        print("✅ App launched with phone number pre-filled!")
    else:
        print("❌ Could not detect phone number from Messages.")
        print("📱 Make sure Messages app is open with a conversation active.")
        print("🔄 Launching app normally...")
        
        # Launch app normally
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.run([sys.executable, os.path.join(script_dir, 'run_app.py')])

if __name__ == "__main__":
    main()