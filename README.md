# fireControl

Manual Mode Improvements Branch

Fire control board

This is the project for the remote Fire Control board


RPI <~~~xbee~~~> Arduino

GUI->comms~~~~~comms->Arduino->main relays & sensors

So far there are three operationg modes:
Safety - No messages to the remote panel are sent
Test - messages to the remote panel are sent, but remote will not fire the mains
Armed - messages to the remote panel are sent and the remote will fire the mains

Diagnostics provides logging for messages transmitted and messages received.  Additionally, There is a "Test All" option that will test all of the fire mechanisms.

Manual is a virtual-manual panel

Sequencer is a way to script via time-delay (Finale, etc)
The Sequencer will provide a basic editing platform

