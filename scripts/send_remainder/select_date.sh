#!/bin/zsh

meeting_info=$(zenity --forms \
    --title 'Meeting' --text 'Remainder Information' \
    --add-calendar 'Date' --add-entry 'Title' \
    --add-entry 'Emails' \
    2>/dev/null)

if [[ -n "$meeting_info" ]]; then
    python3 send_remainders.py "$meeting_info"
fi