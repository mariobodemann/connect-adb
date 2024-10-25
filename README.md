# WHAT?
Script to run a developer machine server that can be connected to by an android phone using the script delivered by a GET request to this server.

# HOW?

Use termux to run android local things. Could be an app, but isn't. :shrug:

# Process

1. checkout this file on the developer machine
2. replace SERVER_ADDRESS down below with the servers ip address in the network the phone connects to too.
3. run server on local developer machine
4. install termux on Android developer phone
4. install termux-api on Android phone
4. install termux-widget on Android phone
5. install curl on Android phone
5. create folder `~/.shortcuts/` in termux home
6. curl the SERVER, saving response to .shortcuts: `curl $SERVER_ADDRESS > ~/.shortcuts/connect-adb
7. add termux widget to launcher: longpress on launcer background, scroll to termux, longpress on termux, move widget to where it needs to be, select 'connect-adb'.
8. enable wireless developer settings
9. open wireless developer settings
10. copy ip:port by longpressing on it and selecting copy
11. tap on 'connect-adb' in newly created widget
12. on developer machine confirm connection with `adb devices`.
13. trouble? Use adb connect tcp:12344 once on every phone while connected with usb
14. more trouble? file a ticket.
15. ....
16. profit


