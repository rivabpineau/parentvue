# Scheduler: macOS LaunchAgent for Python App

## Overview
This guide provides step-by-step instructions for setting up a **LaunchAgent** on macOS to automatically run a Python application (`main.py`).

## 📌 Configuration

### **1️⃣ Create the plist File**
Save the following `.plist` file as:
```sh
~/Library/LaunchAgents/com.parentvue.plist
```

#### **plist File Example**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.parentvue.plist</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>  <!-- Python interpreter -->
        <string>/Users/bp_home/PycharmProjects/parentvue/app/src/main.py</string>  <!-- Path to your script -->
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/bp_home/PycharmProjects/parentvue/app/src/</string>  <!-- Directory where your script runs -->

    <key>StandardOutPath</key>
    <string>/Users/bp_home/PycharmProjects/parentvue/plist_logs/parentvue.log</string>  <!-- Log output -->

    <key>StandardErrorPath</key>
    <string>/Users/bp_home/PycharmProjects/parentvue/plist_logs/parentvue_error.log</string>  <!-- Log errors -->

    <key>RunAtLoad</key>
    <true/>  <!-- Runs on user login -->

    <key>KeepAlive</key>
    <true/>  <!-- Relaunches if it crashes -->
</dict>
</plist>
```

---

### **2️⃣ Set Up the LaunchAgent**
#### **Move the plist to the Correct Location**
```sh
mv com.parentvue.plist ~/Library/LaunchAgents/
```

#### **Adjust File Permissions**
```sh

chmod 644 ~/Library/LaunchAgents/com.parentvue.plist
sudo chown bp_home:staff ~/Library/LaunchAgents/com.parentvue.plist
chmod +x /Users/bp_home/PycharmProjects/parentvue/app/src/main.py
  
```

#### **Load the LaunchAgent**
```sh
launchctl load ~/Library/LaunchAgents/com.parentvue.plist
```

#### **Check if it's Running**
```sh
launchctl list | grep com.parentvue
```

#### **Unload if Needed**
```sh
launchctl unload ~/Library/LaunchAgents/com.parentvue.plist
```

---

## 📌 Additional LaunchAgent Parameters
| Key | Type | Description |
|------|------|-------------|
| **`Label`** | `string` | Unique identifier (must match the filename). |
| **`ProgramArguments`** | `array` | Command and arguments to execute. |
| **`WorkingDirectory`** | `string` | Directory where the script runs. |
| **`RunAtLoad`** | `boolean` | Runs the script immediately on load. |
| **`KeepAlive`** | `boolean/dict` | Restarts if it crashes (set to `true` for always running). |
| **`StandardOutPath`** | `string` | Path to the log file for stdout. |
| **`StandardErrorPath`** | `string` | Path to the log file for stderr. |

---

## ⏳ **Scheduling & Process Control**
| Key | Type | Description |
|------|------|-------------|
| **`StartInterval`** | `integer` | Runs the job every `X` seconds. |
| **`StartCalendarInterval`** | `dict` | Runs at specific times/days. |
| **`ThrottleInterval`** | `integer` | Minimum seconds between restarts. |
| **`WatchPaths`** | `array` | Restarts when a file changes. |
| **`EnvironmentVariables`** | `dict` | Set environment variables. |

### **Example: Run at 3:15 AM Daily**
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key> <integer>3</integer>
    <key>Minute</key> <integer>15</integer>
</dict>
```

---

## **🚀 Advanced KeepAlive Options**
```xml
<key>KeepAlive</key>
<dict>
    <key>SuccessfulExit</key> <false/>  <!-- Restart if the job exits successfully -->
    <key>NetworkState</key> <true/>  <!-- Restart when network is available -->
</dict>
```

---

## **✅ Troubleshooting**
- **Check logs:**
  ```sh
  cat /Users/bp_home/PycharmProjects/parentvue/plist_logs/parentvue.log
  cat /Users/bp_home/PycharmProjects/parentvue/plist_logs/parentvue_error.log
  ```
- **Ensure `python3` is correctly referenced:**
  ```sh
  which python3
  ```
- **Verify script permissions:**
  ```sh
  chmod +x /Users/bp_home/PycharmProjects/parentvue/app/src/main.py
  
  sudo chown bp_home:staff ~/Library/LaunchAgents/com.parentvue.plist
  ```
- **Manually start the script to test:**
  ```sh
  /usr/bin/python3 /Users/bp_home/PycharmProjects/parentvue/app/src/main.py
  ```

---

## 🎯 **Final Notes**
- The **LaunchAgent runs as the logged-in user**.
- If you need system-wide execution, use a **LaunchDaemon** instead.
- Modify **StartCalendarInterval** or **StartInterval** for scheduled execution.

🚀 **Now your Python app will run automatically at login!** 🎉
