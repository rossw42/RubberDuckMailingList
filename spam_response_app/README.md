# 📱 Spam Response Assistant

A simple macOS application to quickly respond to text spam using predefined templates through the Messages app.

## ✨ Features

- **🦆 Rubber Duck Response Collection**: Over 20 hilarious rubber duck themed responses from dramatic cult recruitment to political duck conspiracies!
- **📱 Smart Phone Input**: Accepts any phone number format - (123) 456-7890, +1234567890, 123-456-7890, etc.
- **🎲 Random Duck Image Sender**: Send random rubber duck photos with funny messages like "QUACK ATTACK!" and "Duck invasion continues..."
- **Custom Response Management**: Add, edit, and delete your own response templates
- **Quick Send**: Select a template and send with one click
- **Messages App Integration**: Uses AppleScript to send messages through the native Messages app
- **Message Preview**: See exactly what you'll send before sending it
- **Persistent Storage**: Your custom responses are saved between sessions

## 🚀 Quick Start

### Requirements
- macOS (any recent version)
- Python 3.6 or later (usually pre-installed on macOS)
- Messages app (built into macOS)

### Installation

1. **Download the app files** to a folder on your Mac
2. **Open Terminal** and navigate to the app folder:
   ```bash
   cd /path/to/spam_response_app
   ```
3. **Install Messages integration** (RECOMMENDED):
   ```bash
   python3 install_messages_service.py
   ```
4. **Run the app**:
   ```bash
   python3 run_app.py
   ```

### First Run Setup

1. **Install Messages Integration** (HIGHLY RECOMMENDED):
   ```bash
   python3 install_messages_service.py
   ```
   - This allows right-clicking phone numbers in Messages!
   - System service will be installed automatically

2. **Test AppleScript Integration**:
   - Click "Test AppleScript" button
   - Grant permission if prompted
   - You should see "Messages app is accessible"

3. **Grant Permissions** (if needed):
   - Go to System Preferences → Security & Privacy → Privacy
   - Add Terminal (or Python) to "Automation" if prompted
   - Allow access to Messages app

### 🎯 Phone Number Input Help

**Having trouble finding where to put the phone number?**

Look for the **PROMINENT section** at the top of the app window:
**"📞 ENTER SPAM PHONE NUMBER HERE"** ← This is where you type!

**Three ways to get numbers in:**
1. **Right-click method**: Highlight number in Messages → Right-click → "Send to Spam Response App"
2. **Paste method**: Copy number → Click **"📋 Paste"** button in app
3. **Manual method**: Type directly in the big phone input field

## 📖 How to Use

### 🎯 EASIEST METHOD - Right-Click in Messages (Recommended!)

1. **Open Messages app**
2. **Find spam text** with phone number
3. **Select/highlight the phone number**
4. **Right-click** and choose **"Send to Spam Response App"**
5. **App opens automatically** with number pre-filled! 🎉
6. **Select duck response** and send instantly!

### 📋 Alternative Method - Copy & Paste

1. **Launch the App**: `python3 run_app.py`
2. **Copy phone number** from Messages app
3. **Click "📋 Paste" button** in the prominent phone input section
4. **Select Response** from 20+ rubber duck themed options
5. **Send Message or Duck Image** with one click!

### ✏️ Manual Entry Method

**Can't find where to enter the phone number?**
Look for the **BIG section** at the top that says: **"📞 ENTER SPAM PHONE NUMBER HERE"**

1. **Type phone number** directly in the big phone input field
   - Any format works: +1234567890, (123) 456-7890, 123-456-7890, etc.
2. **Select Response** from 20+ rubber duck themed responses
3. **Send Message or Duck Image**:
   - Click "Send Message" for text responses
   - Click "🦆 Send Random Duck Image" for duck photo attacks
   - Confirmation dialog will appear on success

### Managing Response Templates

#### Add New Response
1. Click "Add New Response"
2. Enter a name for your template
3. Type your message
4. Click "Save"

#### Edit Existing Response
1. Select a response from the list
2. Click "Edit Selected" or double-click the response
3. Modify the name or message
4. Click "Save"

#### Delete Response
1. Select a response from the list
2. Click "Delete Selected"
3. Confirm deletion

### 🦆 Rubber Duck Response Arsenal

The app comes loaded with 20+ creative rubber duck themed responses:

**Classic Spam Responses**:
- **Polite Decline**: Standard removal request
- **Stop Request**: Simple "STOP" command

**🦆 Rubber Duck Club Welcome Responses**:
- **Dramatic Welcome**: "Welcome, chosen one, to the hallowed order of the Yellow Rubber Duck Club..."
- **Deadpan Sarcastic**: "Congrats. You're in the Yellow Rubber Duck Club now..."
- **Wholesome Hype**: "Yessss, welcome to the squad! You did it..."
- **Corporate Memo**: "Your application to the Yellow Rubber Duck Club has been approved..."
- **Cult Recruitment**: "Welcome, initiate. You have been reborn..."
- **Apocalypse Radio**: "⚠️ ATTENTION SURVIVOR ⚠️ This is Command speaking..."
- **Gothic Horror**: "Ah, poor soul. You thought you were joining a club..."
- **Game Show Chaos**: "🎉 WELCOME, CONTESTANT! 🎉 You've just WON a lifetime membership..."

**🦆 Unhinged Duck Responses**:
- **Sugar Rush**: "HIIII FRIENDS!!! WOW WOW WOW, YOU DID IT!!!"
- **Host Losing It**: "HEY KIDDOS!!! WOWEEE!! GUESS WHO JUST JOINED..."
- **Puppet Terror**: "QUAAAACK QUAAAACK HELLOOOOO!!! 🦆 You're in the DUCKY CLUB NOW!"
- **Duck Oracle**: "Today's squeaky prophet has arrived. The council of quacks demanded..."
- **Clown Duck**: "Heeheehee! Another duck crawled out of the bathtub for you!"

**🦆 Political Duck Responses**:
- **Political PAC**: "Thank you for your message regarding [CANDIDATE NAME]. I have been automatically enrolled in the Yellow Rubber Duck Political Action Committee..."
- **Enthusiastic Policy**: "YES! I ABSOLUTELY agree that [POLITICAL ISSUE] is important! That's exactly why I've dedicated my life to the Yellow Rubber Duck Voter Mobilization Initiative!"
- **Conspiracy Duck**: "Finally, someone else who understands the TRUTH about what's really happening!"
- **Duck Department**: "🚨 NOTICE: This number has been flagged by the U.S. Department of Waterfowl Affairs..."
- **Duck Emergency**: "THIS IS NOT A DRILL! We've intercepted your political message but there's been a MASSIVE rubber duck containment breach!"

**🦆 Random Duck Image Feature**:
- Sends random rubber duck photos from curated collection
- Includes funny delivery messages like "DUCK ATTACK!" and "Emergency duck delivery!"
- Perfect for maximum confusion and spam deterrent

## 🔧 Troubleshooting

### Common Issues

#### "AppleScript test failed"
**Problem**: The app can't access Messages app

**Solutions**:
1. **Grant Permissions**:
   - System Preferences → Security & Privacy → Privacy → Automation
   - Enable Python/Terminal access to Messages

2. **Messages App Issues**:
   - Make sure Messages app is installed and working
   - Try opening Messages manually first
   - Sign in to iMessage if not already signed in

3. **Permission Prompts**:
   - Run the app from Terminal (not Finder)
   - You may see permission dialogs - click "Allow"

#### "Failed to send message"
**Problem**: Message sending fails

**Solutions**:
1. **Check Phone Number**: Ensure it's a valid number format
2. **iMessage Status**: Make sure you're signed into iMessage
3. **Network Connection**: Check internet connectivity
4. **Recipient Issues**: Number might not support iMessage (will try SMS)

#### App won't start
**Problem**: Python errors when launching

**Solutions**:
1. **Python Version**: Make sure you have Python 3.6+
   ```bash
   python3 --version
   ```
2. **Run from Terminal**: Don't double-click files, use Terminal
3. **File Permissions**: Make sure files aren't read-only

### Advanced Troubleshooting

#### Enable Debug Mode
Add this to see more detailed error messages:
```bash
python3 -v run_app.py
```

#### Manual AppleScript Test
Test AppleScript directly in Terminal:
```bash
osascript -e 'tell application "Messages" to return "test"'
```

#### Reset App Data
Delete the config file to reset to defaults:
```bash
rm spam_responses.json
```

## 🛠️ Technical Details

### How It Works
- **GUI**: Built with Python's tkinter (included with Python)
- **Messages Integration**: Uses AppleScript to control Messages app
- **Data Storage**: JSON file for response templates
- **Cross-Platform**: Core works on any OS, Messages integration macOS-only

### File Structure
```
spam_response_app/
├── main.py              # Main application code
├── run_app.py           # Startup script
├── README.md            # This documentation
└── spam_responses.json  # Your saved responses (created automatically)
```

### AppleScript Commands
The app uses these AppleScript commands:
```applescript
tell application "Messages"
    set targetService to 1st service whose service type = iMessage
    set targetBuddy to buddy "PHONE_NUMBER" of targetService
    send "MESSAGE_TEXT" to targetBuddy
end tell
```

## 🔒 Privacy & Security

- **No Data Collection**: All data stays on your Mac
- **No Network Requests**: Only communicates with local Messages app
- **Open Source**: You can review all code in the files
- **Permissions**: Only requests access to Messages app when needed

## 💡 Tips & Best Practices

### Effective Spam Response Strategy
1. **For Marketing Texts**: Use "STOP" - it's legally required to work
2. **For Scams**: Don't respond at all, or use "Report Spam"
3. **For Fun**: Use the "Fake Interest" template to waste scammers' time
4. **Custom Responses**: Create templates for specific types of spam you receive

### Using the App Efficiently
1. **Keep It Running**: Leave the app open for quick access to duck responses
2. **Phone Number Formats**: Any format works - the app handles formatting automatically
3. **Duck Image Strategy**: Use random duck images for maximum spammer confusion
4. **Response Categories**:
   - Use "Corporate Memo" for professional spammers
   - Use "Cult Recruitment" for MLM schemes
   - Use "Political Duck" responses for campaign texts
   - Use "Sugar Rush" for maximum chaos deployment
5. **Escalation Ladder**: Start with subtle duck references, escalate to full duck madness

### Safety Considerations
- **Don't Engage Scammers**: Some responses might encourage more contact
- **Block Numbers**: Use iOS's built-in blocking after responding
- **Report Spam**: Consider reporting to carriers (forward to 7726/SPAM)

## 🤝 Support

### Getting Help
1. **Check This README**: Most issues are covered here
2. **Test AppleScript**: Use the built-in test button first
3. **Check Permissions**: Most issues are permission-related
4. **Try Restarting**: Both the app and Messages app

### Making It Better
This is a simple tool that can be extended:
- Add more rubber duck image sources
- Create seasonal duck themes (Halloween ducks, Christmas ducks)
- Add duck sound effects with responses
- Integrate with contact blocking
- Add rubber duck statistics tracking ("Ducks Deployed: 47")
- Create duck response scheduling
- Add "Quack Translation" for converting normal text to duck speak

---

**Made for Mac users tired of spam texts! 🚫📱**