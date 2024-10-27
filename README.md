# WHAT?
Server to run on a developer machine that can be connected to by an android phone using the GET request to this server. Use http://{SERVER_IP}:65535 from the phone.

# HOW?

DevMachine: run server; Phone enable wireless dev, copy host:port, open browser/shortcut.

# Process

1. checkout this file on the developer machine
3. run server on local developer machine
8. on phone: enable wireless developer settings
9. open wireless developer settings
10. copy host:port by longpressing on it and selecting copy
11. open server page http://{SERVER_IP}:65535 from browser on phone
12. optional: save page as shortcut / launcher
12. paste ip from before in text field
12. hit submit.
12. on developer machine confirm connection with `adb devices`.
13. trouble? Use adb connect tcp:12344 once on every phone while connected with usb
14. more trouble? file a ticket.
15. ....
16. profit


