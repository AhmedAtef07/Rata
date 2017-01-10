# Rata
A remote access Trojan (RAT), for educative security purpose.

# Functionality
Log every single key pressed to a google form, the data is sent over SSL using "cert.pem" as trusted certificates.

# How to build and run
1. Make sure that you have all the imported packages.
2. Go to "lib\site-packages\pyHook\HookManager.py".
3. Replace line 349 with "func = self.keyboard_funcs.get( int(str(msg)) )".
4. Open new terminal.
5. Pip install pyinstaller
6. Add pyinstaller to environment PATH.
7. Run pyinstaller --onefile main.py.

