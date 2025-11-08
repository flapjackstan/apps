# Apps

Collection of apps that I use for different purposes and have saved as an `alias` on my local machine.

For some reason I cant run regular `uv run python apps/apps.py`

`holiday` - Print the closest federal holiday from today.
`dates` - Date calculator with two uses. 1) Provided a spcific date calculate the date ahead or back n days. 2) Calculate the days between 2 dates. Used this as like a reminder of how many days until my next vacation and little stuff like that.
`names` - Generates a random name from an sqlite db dependent on the theme you pass it (simpsons|rappers). I use this to demo some random examples of processes.

# UVX runs

These scripts should be runnable within `uvx` for example

`uvx --from git+https://github.com/flapjackstan/apps apps --help`
`uvx --from git+https://github.com/flapjackstan/apps apps holiday next`
`uvx --from git+https://github.com/flapjackstan/apps apps dates shift 2025-08-21 365 forward`
`uvx --from git+https://github.com/flapjackstan/apps apps dates between 2025-11-08 2026-08-21`

# Archived apps
These apps used to exist, but I havent migrated them to the standalone and build uvx way of running them

`timer` - I mostly use this as a pomodoro app or as a timer for making an aeropress.
`lotto` - Provided a list of space seperated names, randomly select members. Useful for group project brainstorm sessions.
`tracts` - A tool to download census tract data and save it as a GeoJSON file. It uses the Census and Tiger APIs to fetch data for a specified state, county, and year. The data includes geographic information and census variables such as median age, total population, and median income (adjust in script for now). The script requires a Census API key to function.
`interview` - Questions to ask an interview prep buddy.

