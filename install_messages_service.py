#!/usr/bin/env python3
"""
Installer for Messages app integration service
Creates an Automator service for right-clicking phone numbers
"""

import os
import subprocess
import tempfile

def create_automator_service():
    """Create Automator service for Messages integration"""
    
    # AppleScript for the service
    applescript_content = '''
on run {input, parameters}
    set phoneNumber to (input as string)
    
    -- Clean up the phone number (remove extra whitespace)
    set phoneNumber to do shell script "echo " & quoted form of phoneNumber & " | tr -d '[:space:]'"
    
    -- Try to launch our spam response app with the phone number
    try
        do shell script "cd ~/Documents/Notes/Personal/Rubber\\ Ducks/spam_response_app && python3 -c \\"
import sys
sys.path.append('.')
from main import SpamResponseApp
import tkinter as tk

# Create app
app = SpamResponseApp()

# Pre-fill phone number
app.phone_var.set('" & phoneNumber & "')
app.status_var.set('Phone number from Messages: " & phoneNumber & "')

# Show window and focus on responses
app.root.lift()
app.root.attributes('-topmost', True)
app.root.after_idle(app.root.attributes, '-topmost', False)
if app.responses:
    app.response_listbox.focus_set()

# Run app
app.run()
\\" &" in background
        
        return phoneNumber
    on error errorMessage
        display dialog "Could not launch Spam Response App: " & errorMessage buttons {"OK"} default button "OK"
        return input
    end try
end run
'''
    
    # Create the service directory
    services_dir = os.path.expanduser("~/Library/Services")
    service_path = os.path.join(services_dir, "Send to Spam Response App.workflow")
    
    if not os.path.exists(services_dir):
        os.makedirs(services_dir)
    
    print("🔧 Creating Automator service...")
    print(f"📁 Service will be installed to: {service_path}")
    
    # Create workflow directory structure
    workflow_dir = service_path
    contents_dir = os.path.join(workflow_dir, "Contents")
    
    os.makedirs(contents_dir, exist_ok=True)
    
    # Create Info.plist
    info_plist = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSServices</key>
    <array>
        <dict>
            <key>NSMenuItem</key>
            <dict>
                <key>default</key>
                <string>Send to Spam Response App</string>
            </dict>
            <key>NSMessage</key>
            <string>runWorkflowAsService</string>
            <key>NSRequiredContext</key>
            <dict>
                <key>NSApplicationIdentifier</key>
                <string>com.apple.iChat</string>
            </dict>
            <key>NSSendTypes</key>
            <array>
                <string>public.plain-text</string>
            </array>
        </dict>
    </array>
</dict>
</plist>'''
    
    with open(os.path.join(contents_dir, "Info.plist"), 'w') as f:
        f.write(info_plist)
    
    # Create document.wflow
    document_wflow = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>AMApplicationBuild</key>
    <string>512</string>
    <key>AMApplicationVersion</key>
    <string>2.10</string>
    <key>AMDocumentVersion</key>
    <string>2</string>
    <key>actions</key>
    <array>
        <dict>
            <key>action</key>
            <dict>
                <key>AMAccepts</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Optional</key>
                    <true/>
                    <key>Types</key>
                    <array>
                        <string>com.apple.cocoa.string</string>
                    </array>
                </dict>
                <key>AMActionVersion</key>
                <string>1.0.2</string>
                <key>AMApplication</key>
                <array>
                    <string>Automator</string>
                </array>
                <key>AMParameterProperties</key>
                <dict>
                    <key>source</key>
                    <dict>
                        <key>tokenizedValue</key>
                        <array>
                            <string>{applescript_content}</string>
                        </array>
                    </dict>
                </dict>
                <key>AMProvides</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Types</key>
                    <array>
                        <string>com.apple.cocoa.string</string>
                    </array>
                </dict>
                <key>ActionBundlePath</key>
                <string>/System/Library/Automator/Run AppleScript.action</string>
                <key>ActionName</key>
                <string>Run AppleScript</string>
                <key>ActionParameters</key>
                <dict>
                    <key>source</key>
                    <string>{applescript_content}</string>
                </dict>
                <key>BundleIdentifier</key>
                <string>com.apple.Automator.RunScript</string>
                <key>CFBundleVersion</key>
                <string>1.0.2</string>
                <key>CanShowSelectedItemsWhenRun</key>
                <false/>
                <key>CanShowWhenRun</key>
                <true/>
                <key>Category</key>
                <array>
                    <string>AMCategoryUtilities</string>
                </array>
                <key>Class Name</key>
                <string>RunScriptAction</string>
                <key>InputUUID</key>
                <string>12345678-1234-5678-9012-123456789012</string>
                <key>Keywords</key>
                <array>
                    <string>Run</string>
                </array>
                <key>OutputUUID</key>
                <string>87654321-4321-8765-2109-876543210987</string>
                <key>UUID</key>
                <string>ABCDEF12-3456-7890-ABCD-EF1234567890</string>
                <key>UnlocalizedApplications</key>
                <array>
                    <string>Automator</string>
                </array>
                <key>arguments</key>
                <dict>
                    <key>0</key>
                    <dict>
                        <key>default value</key>
                        <string>on run {{input, parameters}}
	
	(* Your script goes here *)
	
	return input
end run</string>
                        <key>name</key>
                        <string>source</string>
                        <key>required</key>
                        <string>0</string>
                        <key>type</key>
                        <string>0</string>
                        <key>uuid</key>
                        <string>0</string>
                    </dict>
                </dict>
                <key>isViewVisible</key>
                <true/>
                <key>location</key>
                <string>449.000000:316.000000</string>
                <key>nibPath</key>
                <string>/System/Library/Automator/Run AppleScript.action/Contents/Resources/Base.lproj/main.nib</string>
            </dict>
            <key>isViewVisible</key>
            <true/>
        </dict>
    </array>
    <key>connectors</key>
    <dict/>
    <key>workflowMetaData</key>
    <dict>
        <key>serviceInputTypeIdentifier</key>
        <string>com.apple.Automator.text</string>
        <key>serviceOutputTypeIdentifier</key>
        <string>com.apple.Automator.nothing</string>
        <key>serviceProcessesInput</key>
        <integer>0</integer>
        <key>workflowTypeIdentifier</key>
        <string>com.apple.Automator.servicesMenu</string>
    </dict>
</dict>
</plist>'''
    
    with open(os.path.join(workflow_dir, "Contents", "document.wflow"), 'w') as f:
        f.write(document_wflow)
    
    print("✅ Automator service created successfully!")
    print("\n🔄 Refreshing system services...")
    
    # Refresh system services
    try:
        subprocess.run(["/System/Library/CoreServices/pbs", "-flush"], check=True)
        print("✅ System services refreshed!")
    except subprocess.CalledProcessError:
        print("⚠️  Could not refresh services automatically. You may need to restart or log out and back in.")
    
    print("\n📱 SETUP COMPLETE!")
    print("\n🎯 How to use:")
    print("1. Open Messages app")
    print("2. Select/highlight a phone number")
    print("3. Right-click and choose 'Send to Spam Response App'")
    print("4. The app will open with the number pre-filled!")
    
    return service_path

def main():
    """Main installer function"""
    print("🦆 Spam Response App - Messages Integration Installer")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: Please run this from the spam_response_app directory")
        print("Current directory:", os.getcwd())
        return
    
    try:
        service_path = create_automator_service()
        print(f"\n🎉 Installation complete! Service installed to:")
        print(f"📂 {service_path}")
        
        print(f"\n💡 Pro tip: You can also manually copy phone numbers and use the '📋 Paste' button in the app!")
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        print("You can still use the app by manually copying phone numbers.")

if __name__ == "__main__":
    main()