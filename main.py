#!/usr/bin/env python3
"""
Spam Response App for macOS Messages
A simple tool to quickly respond to text spam with predefined messages
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import subprocess
import urllib.request
import urllib.parse
import random
import tempfile
from typing import List, Dict

class SpamResponseApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spam Response Assistant")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Data storage
        self.config_file = "spam_responses.json"
        self.responses = self.load_responses()
        
        self.setup_ui()
        self.load_response_list()
        
    def setup_ui(self):
        """Create the main user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📱 Spam Response Assistant",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # PROMINENT Phone number input section
        phone_frame = ttk.LabelFrame(main_frame, text="📞 ENTER SPAM PHONE NUMBER HERE", padding="15")
        phone_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        phone_frame.columnconfigure(1, weight=1)
        
        # Big prominent phone input
        phone_label = ttk.Label(phone_frame, text="Phone Number:", font=('Arial', 12, 'bold'))
        phone_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(phone_frame, textvariable=self.phone_var, width=25, font=('Arial', 12))
        self.phone_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15))
        
        # Paste button for easy input
        paste_btn = ttk.Button(phone_frame, text="📋 Paste", command=self.paste_from_clipboard)
        paste_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Quick send button
        self.quick_send_btn = ttk.Button(phone_frame, text="⚡ Quick Send Selected",
                                        command=self.quick_send_response, state='disabled')
        self.quick_send_btn.grid(row=0, column=3)
        
        # Responses frame
        responses_frame = ttk.LabelFrame(main_frame, text="Response Templates", padding="10")
        responses_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        responses_frame.columnconfigure(0, weight=1)
        responses_frame.rowconfigure(0, weight=1)
        
        # Response listbox with scrollbar
        list_frame = ttk.Frame(responses_frame)
        list_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.response_listbox = tk.Listbox(list_frame, height=10)
        self.response_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.response_listbox.bind('<<ListboxSelect>>', self.on_response_select)
        self.response_listbox.bind('<Double-1>', self.edit_response)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.response_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.response_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons for managing responses
        btn_frame = ttk.Frame(responses_frame)
        btn_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Add New Response", 
                  command=self.add_response).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Edit Selected", 
                  command=self.edit_response).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Delete Selected", 
                  command=self.delete_response).pack(side=tk.LEFT, padx=(0, 10))
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Message Preview", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        
        self.preview_text = tk.Text(preview_frame, height=4, wrap=tk.WORD)
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.preview_text.configure(state='disabled')
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(control_frame, text="Send Message",
                  command=self.send_message, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="🦆 Send Random Duck Image",
                  command=self.send_duck_image).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Test AppleScript",
                  command=self.test_applescript).pack(side=tk.LEFT, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select a response template and enter phone number")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def load_responses(self) -> List[Dict]:
        """Load response templates from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Default responses if file doesn't exist - Rubber Duck Mailing List Responses!
        return [
            # Classic Spam Responses
            {
                "name": "Polite Decline",
                "message": "I'm not interested. Please remove my number from your list."
            },
            {
                "name": "Stop Request",
                "message": "STOP"
            },
            
            # RUBBER DUCK CLUB RESPONSES - Over-the-top dramatic
            {
                "name": "🦆 Dramatic Welcome",
                "message": "Welcome, chosen one, to the hallowed order of the Yellow Rubber Duck Club. Few dare to tread this path, and fewer still survive the tidal wave of squeaky, plastic majesty awaiting them. Prepare your soul (and your notifications), for each dawn shall bring a new yellow idol, a divine ducky relic delivered straight to your mortal eyes. Do not resist—this is your destiny."
            },
            
            # Deadpan sarcastic
            {
                "name": "🦆 Deadpan Sarcastic",
                "message": "Congrats. You're in the Yellow Rubber Duck Club now. You'll get daily duck pics whether you want them or not—because clearly this is what your life has been building toward. Forget career goals, relationships, or hobbies; it's ducks now. Just ducks. Forever."
            },
            
            # Wholesome hype-friend
            {
                "name": "🦆 Wholesome Hype",
                "message": "Yessss, welcome to the squad! You did it—you're officially part of the Yellow Rubber Duck Club. From here on out, every day is duck day. You're gonna wake up, roll over, check your phone, and BOOM—bright yellow duck staring at you like, 'hey, we got this.' It's the daily serotonin boost you didn't even know you needed."
            },
            
            # Corporate memo
            {
                "name": "🦆 Corporate Memo",
                "message": "Congratulations, valued member. Your application to the Yellow Rubber Duck Club has been approved. Effective immediately, you are entitled to a daily transmission of yellow rubber duck imagery. Please note: failure to appreciate said ducks may result in corrective squeaks. Welcome aboard."
            },
            
            # Cult recruitment energy
            {
                "name": "🦆 Cult Recruitment",
                "message": "Welcome, initiate. You have been reborn into the Yellow Rubber Duck Club. Your former identity no longer matters; only the duck remains. Each morning you shall receive sacred images of our luminous yellow idols, their beady black eyes watching over you, their eternal squeaks echoing in your mind. Resistance is useless. Quack is inevitable."
            },
            
            # Apocalypse radio broadcast
            {
                "name": "🦆 Apocalypse Radio",
                "message": "⚠️ ATTENTION SURVIVOR ⚠️ This is Command speaking. You have successfully tuned into the Yellow Rubber Duck Club frequency. Effective immediately, daily duck imagery will be transmitted to your device. These ducks are not mere toys—they are the last pure symbol of civilization. Cherish them, study them, and above all, do not anger them. Godspeed."
            },
            
            # Gothic horror narrator
            {
                "name": "🦆 Gothic Horror",
                "message": "Ah, poor soul. You thought you were joining a club, but you've instead bound yourself to an eternity of yellow rubber duck apparitions. They will come to you at dawn, their squeaky voices carried on the wind, their painted smiles never fading. Soon, you'll see them even when you close your eyes. Welcome."
            },
            
            # Game show host chaos
            {
                "name": "🦆 Game Show Chaos",
                "message": "🎉 WELCOME, CONTESTANT! 🎉 You've just WON a lifetime membership in the Yellow Rubber Duck Club! That's right, forever! And what's your grand prize? DAILY PICTURES OF RUBBER DUCKS! That's right—every! single! day! Will you love it? Will it ruin your sanity? Who cares! It's ducks, baby, and you can't unsubscribe!"
            },
            
            # Too much sugar at 6 AM
            {
                "name": "🦆 Sugar Rush",
                "message": "HIIII FRIENDS!!! WOW WOW WOW, YOU DID IT!!! You joined the YELLOW RUBBER DUCK CLUB!!! 🦆✨ From now on, every! single! day! you're gonna get a BRAND-NEW DUCK PICTURE—straight to your eyes!! YAAAAAY!! Isn't that the BEST THING EVER?? Clap your hands, scream into a pillow, and prepare for QUACKY FRIENDS FOREVER!!!"
            },
            
            # The host who's clearly losing it
            {
                "name": "🦆 Host Losing It",
                "message": "HEY KIDDOS!!! WOWEEE!! GUESS WHO JUST JOINED THE YELLOW RUBBER DUCK CLUB?! That's right—you! HAHAHA oh boy, every morning you'll get another DUCK PHOTO, and another, and another… they never stop, oh no, THEY NEVER STOP!!! Isn't that FUN?! (please send help)"
            },
            
            # Terrifyingly enthusiastic puppet energy
            {
                "name": "🦆 Puppet Terror",
                "message": "QUAAAACK QUAAAACK HELLOOOOO!!! 🦆 You're in the DUCKY CLUB NOW! Ooooh boy, do we have a surprise for you!!! EVERY. SINGLE. DAY. we're gonna send you DUCKS—DUCKS IN YOUR PHONE, DUCKS IN YOUR DREAMS, DUCKS IN YOUR WALLS—HAHAHA JUST KIDDING… unless??"
            },
            
            # Random Duck Oracle Messages
            {
                "name": "🦆 Duck Oracle",
                "message": "Today's squeaky prophet has arrived. The council of quacks demanded I send you this. Your daily duck offering—accept it or be cursed with silence. Behold: the plastic oracle of the day. Duck mail. Resistance is futile."
            },
            
            {
                "name": "🦆 Clown Duck",
                "message": "Heeheehee! Another duck crawled out of the bathtub for you! Don't let it bite! HONK HONK! The Duck Parade has chosen YOU for today's squeaky blessing! Who's ready for a QUACK ATTACK?!? (…don't run.)"
            },
            
            # POLITICAL SPAM RESPONSES
            {
                "name": "🦆 Political PAC",
                "message": "Thank you for your message regarding [CANDIDATE NAME]. I have been automatically enrolled in the Yellow Rubber Duck Political Action Committee (YRPAC). You will now receive daily rubber duck voting guides and quack-based policy updates. To unsubscribe, please text 'DUCK OFF' to this number. Your participation in democracy has never been more... squeaky."
            },
            
            {
                "name": "🦆 Enthusiastic Policy",
                "message": "YES! I ABSOLUTELY agree that [POLITICAL ISSUE] is important! That's exactly why I've dedicated my life to the Yellow Rubber Duck Voter Mobilization Initiative! Did you know that rubber ducks are the ONLY political symbol that transcends party lines?? Every American deserves their daily duck pic! QUACK THE VOTE 2025! 🦆🇺🇸"
            },
            
            {
                "name": "🦆 Conspiracy Duck",
                "message": "Finally, someone else who understands the TRUTH about what's really happening! Yes, the rubber duck shadow government has been controlling elections since 1947! I've been tracking their yellow plastic movements for YEARS! Are you part of the resistance? Do you have the sacred squeaker? The ducks are listening... always listening..."
            },
            
            {
                "name": "🦆 Duck Department",
                "message": "🚨 NOTICE: This number has been flagged by the U.S. Department of Waterfowl Affairs for unauthorized political activity. Per Federal Duck Code 42-QUACK-9, you are now required to receive mandatory daily rubber duck civic education materials. Compliance is not optional. Failure to appreciate assigned ducks may result in squeaky penalties."
            },
            
            {
                "name": "🦆 Duck Emergency",
                "message": "THIS IS NOT A DRILL! We've intercepted your political message but there's been a MASSIVE rubber duck containment breach! All cellular networks are being converted to emergency duck alert systems! Please stand by for mandatory cute duck photos to restore order! The situation is SQUEAKY but under control! Thank you for your cooperation during this quack-tastrophe!"
            }
        ]
    
    def save_responses(self):
        """Save response templates to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.responses, f, indent=2)
            self.status_var.set("Responses saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save responses: {str(e)}")
    
    def load_response_list(self):
        """Load responses into the listbox"""
        self.response_listbox.delete(0, tk.END)
        for response in self.responses:
            self.response_listbox.insert(tk.END, response['name'])
    
    def on_response_select(self, event=None):
        """Handle response selection"""
        selection = self.response_listbox.curselection()
        if selection:
            index = selection[0]
            response = self.responses[index]
            
            # Update preview
            self.preview_text.configure(state='normal')
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, response['message'])
            self.preview_text.configure(state='disabled')
            
            # Enable quick send if phone number is entered
            if self.phone_var.get().strip():
                self.quick_send_btn.configure(state='normal')
            
            self.status_var.set(f"Selected: {response['name']}")
    
    def add_response(self):
        """Add a new response template"""
        dialog = ResponseDialog(self.root, "Add New Response")
        if dialog.result:
            name, message = dialog.result
            self.responses.append({"name": name, "message": message})
            self.save_responses()
            self.load_response_list()
            self.status_var.set(f"Added response: {name}")
    
    def edit_response(self, event=None):
        """Edit selected response template"""
        selection = self.response_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a response to edit")
            return
            
        index = selection[0]
        response = self.responses[index]
        
        dialog = ResponseDialog(self.root, "Edit Response", 
                               initial_name=response['name'], 
                               initial_message=response['message'])
        if dialog.result:
            name, message = dialog.result
            self.responses[index] = {"name": name, "message": message}
            self.save_responses()
            self.load_response_list()
            self.status_var.set(f"Updated response: {name}")
    
    def delete_response(self):
        """Delete selected response template"""
        selection = self.response_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a response to delete")
            return
            
        index = selection[0]
        response = self.responses[index]
        
        if messagebox.askyesno("Confirm Delete", f"Delete response '{response['name']}'?"):
            del self.responses[index]
            self.save_responses()
            self.load_response_list()
            
            # Clear preview
            self.preview_text.configure(state='normal')
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.configure(state='disabled')
            
            self.status_var.set(f"Deleted response: {response['name']}")
    
    def quick_send_response(self):
        """Quickly send the selected response"""
        self.send_message()
    
    def send_message(self):
        """Send message using AppleScript"""
        phone = self.phone_var.get().strip()
        if not phone:
            messagebox.showwarning("Warning", "Please enter a phone number")
            return
            
        # Get message content
        message = self.preview_text.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "Please select a response or enter a message")
            return
        
        try:
            self.send_imessage(phone, message)
            self.status_var.set(f"✅ Message sent to {phone}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
            self.status_var.set("Failed to send message")
    
    def send_imessage(self, phone_number: str, message: str):
        """Send iMessage using AppleScript"""
        # Clean phone number
        phone_number = phone_number.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
        applescript = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{phone_number}" of targetService
            send "{message}" to targetBuddy
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"AppleScript error: {result.stderr}")
    
    def send_remote_duck_image(self, phone_number: str):
        """Send rubber duck image from remote URLs"""
        try:
            # Collection of remote duck image URLs
            duck_urls = [
                "https://upload.wikimedia.org/wikipedia/commons/d/d5/Rubber_duck_assisting_with_debugging.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Rubber_duck_assisting_with_debugging.jpg/800px-Rubber_duck_assisting_with_debugging.jpg",
                "https://images.unsplash.com/photo-1563906267088-b029e7101114?w=400",
                "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
                "https://images.unsplash.com/photo-1563906267088-b029e7101114?ixlib=rb-4.0.3&w=400",
                "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&w=400"
            ]
            
            # Pick random duck URL
            duck_url = random.choice(duck_urls)
            
            # Download image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                try:
                    with urllib.request.urlopen(duck_url) as response:
                        tmp_file.write(response.read())
                    
                    temp_path = tmp_file.name
                    
                    # Send image file via AppleScript
                    # Clean phone number
                    clean_phone = phone_number.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    
                    applescript = f'''
                    tell application "Messages"
                        set targetService to 1st service whose service type = iMessage
                        set targetBuddy to buddy "{clean_phone}" of targetService
                        set imageFile to POSIX file "{temp_path}"
                        send imageFile to targetBuddy
                    end tell
                    '''
                    
                    result = subprocess.run(['osascript', '-e', applescript],
                                          capture_output=True, text=True)
                    
                    # Clean up temporary file
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                    
                    if result.returncode != 0:
                        raise Exception(f"AppleScript error: {result.stderr}")
                        
                    return True
                    
                except Exception as download_error:
                    # Clean up temp file if download failed
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                    raise download_error
            
        except Exception as e:
            # Fallback to duck emoji if image sending fails
            duck_emojis = "🦆🦆🦆 QUACK ATTACK! 🦆🦆🦆"
            self.send_imessage(phone_number, duck_emojis)
            return False
    
    def send_duck_image(self):
        """Send a random rubber duck image"""
        phone = self.phone_var.get().strip()
        if not phone:
            messagebox.showwarning("Warning", "Please enter a phone number first!")
            return
        
        try:
            # Try to send remote duck image file
            success = self.send_remote_duck_image(phone)
            
            if success:
                self.status_var.set(f"🦆 Duck image deployed to {phone}")
            else:
                self.status_var.set(f"🦆 Duck emojis sent to {phone}")
            
        except Exception as e:
            self.status_var.set("🦆 Duck delivery failed - try again!")
    
    def test_applescript(self):
        """Test AppleScript functionality"""
        try:
            # Test if Messages app is accessible
            test_script = '''
            tell application "Messages"
                return "Messages app is accessible"
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', test_script],
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Test Successful",
                                  "AppleScript can access Messages app!\n\n" +
                                  "You can now send messages AND duck images through the app! 🦆")
            else:
                messagebox.showerror("Test Failed",
                                   f"AppleScript test failed: {result.stderr}\n\n" +
                                   "Make sure Messages app is installed and accessible.")
        except Exception as e:
            messagebox.showerror("Test Error", f"Test failed: {str(e)}")
    
    def run(self):
        """Start the application"""
        # Bind phone number change to enable/disable quick send
        self.phone_var.trace_add('write', self.on_phone_change)
        
        self.root.mainloop()
    
    def paste_from_clipboard(self):
        """Paste phone number from clipboard"""
        try:
            # Get clipboard content
            clipboard_content = self.root.clipboard_get()
            
            # Basic phone number extraction - look for numbers
            import re
            # Find phone numbers in various formats
            phone_pattern = r'[\+]?[1]?[\s\-\(\)]?[\d]{3}[\s\-\(\)]?[\d]{3}[\s\-]?[\d]{4}'
            matches = re.findall(phone_pattern, clipboard_content)
            
            if matches:
                # Use the first phone number found
                phone_number = matches[0].strip()
                self.phone_var.set(phone_number)
                self.status_var.set(f"📋 Pasted phone number: {phone_number}")
                
                # Auto-focus on response selection
                if self.responses:
                    self.response_listbox.focus_set()
            else:
                # Just paste whatever is in clipboard
                self.phone_var.set(clipboard_content.strip())
                self.status_var.set("📋 Pasted from clipboard")
                
        except tk.TclError:
            # Clipboard is empty or can't be accessed
            messagebox.showwarning("Clipboard Empty", "No content found in clipboard to paste")
            self.status_var.set("Clipboard empty")
    
    def on_phone_change(self, *args):
        """Handle phone number field changes"""
        if self.phone_var.get().strip() and self.response_listbox.curselection():
            self.quick_send_btn.configure(state='normal')
        else:
            self.quick_send_btn.configure(state='disabled')


class ResponseDialog:
    def __init__(self, parent, title, initial_name="", initial_message=""):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name field
        ttk.Label(main_frame, text="Response Name:").pack(anchor=tk.W)
        self.name_var = tk.StringVar(value=initial_name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=50)
        name_entry.pack(fill=tk.X, pady=(5, 15))
        name_entry.focus()
        
        # Message field
        ttk.Label(main_frame, text="Message Text:").pack(anchor=tk.W)
        self.message_text = tk.Text(main_frame, height=8, wrap=tk.WORD)
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=(5, 15))
        self.message_text.insert(1.0, initial_message)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.RIGHT)
        
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def save(self):
        """Save the response"""
        name = self.name_var.get().strip()
        message = self.message_text.get(1.0, tk.END).strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter a name for the response")
            return
            
        if not message:
            messagebox.showwarning("Warning", "Please enter a message")
            return
        
        self.result = (name, message)
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


if __name__ == "__main__":
    app = SpamResponseApp()
    app.run()