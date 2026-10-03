# Extension Risk Scanner

A small Python tool that reads the manifest.json of your installed Chrome extensions, checks them for risky permissions, and ranks them from highest to lowest risk, with a plain-English list of reasons for each score.

Important: a high score means an extension asks for powerful permissions, not that it is malware. Many legitimate extensions (password managers, ad blockers) need broad access. Use the score as a prompt to take a closer look, not as a verdict.


Example output:


Scanning: C:\Users\you\AppData\Local\Google\Chrome\User Data\Default\Extensions

Cool Dark Mode: 65/100
  - cookies (+15)
  - history (+15)
  - <all_urls> (+25)
  - Manifest V2 (legacy) (+10)
Notes Helper: 0/100


Features
Scans every extension in a Chrome extensions folder
Scores each one from 0 to 100 based on the permissions it requests
Shows exactly why each extension got its score
Works on Windows, macOS, and Linux
Skips unreadable manifests instead of crashing
Requirements
Python 3.8 or newer
No extra packages needed (uses only the standard library)
Install
bash
git clone https://github.com/sridharshinicloud/Extension-Risk-Scanner.git
cd extension-risk-scanner

Usage

Scan the default Chrome extensions folder for your operating system:

bash
python extension_scanner.py

Scan a specific folder:

bash
python extension_scanner.py "D:\my\extensions"

Default locations used:

OS	Path
Windows	%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions
macOS	~/Library/Application Support/Google/Chrome/Default/Extensions
Linux	~/.config/google-chrome/Default/Extensions

Using Edge, Brave, or another Chrome profile? Pass its extensions folder as the argument.

How the scoring works

Each extension starts at 0. Points are added for every risky permission it requests, and the total is capped at 100.

Finding	Points	Why it matters
debugger	+30	Can inspect and control pages and network traffic
<all_urls>	+25	Can access every website you visit
webRequestBlocking	+25	Can intercept and modify web requests
nativeMessaging	+20	Can talk to programs on your computer
cookies	+15	Can read and change cookies (including login sessions)
history	+15	Can read your browsing history
management	+15	Can inspect, disable, or control other extensions
Manifest V2	+10	Older, less restrictive security model

Suggested risk levels:

Score	Level
0 to 24	Low
25 to 49	Medium
50 to 74	High
75 to 100	Critical

The weights live in the RISKY dictionary at the top of extension_scanner.py, so you can adjust them to fit your own risk tolerance.

Limitations
Manifest only. It does not analyze the extension's JavaScript code yet, so it cannot detect eval, obfuscation, or suspicious network calls.
No purpose check. It does not compare permissions against what the extension claims to do (e.g. a "dark mode" extension asking for history).
Limited permission list. Only a handful of permissions are scored. Others, such as tabs, proxy, clipboardRead, and downloads, are not included yet.
Translated names. Some extensions show names like __MSG_appName__ because their real name is stored in a translation file.
Default profile only. It scans the Default Chrome profile unless you pass another folder.
Scores are heuristic. The weights are judgment calls, not an official standard.
Roadmap
 Scan JavaScript files for risky patterns (eval, hardcoded URLs, obfuscation)
 Resolve __MSG_...__ names from _locales
 Add more permissions to the scoring table
 HTML report output
 Diff mode: flag when an update adds new permissions
 Unit tests with sample extensions
Responsible use

This is a defensive auditing tool. Use it only on extensions installed on your own machine or that you are otherwise allowed to inspect.

Contributing

Issues and pull requests are welcome. If you think a permission is weighted too high or too low, open an issue and explain your reasoning.

License

MIT License. See the LICENSE file for details.
