#!/bin/sh
# Start both journalist and admin bots in background
python journalist_bot.py &
python admin_bot.py &
# Wait for all (both) processes (they run indefinitely)
wait
