# Apps

Collection of apps that I use for different purposes and have saved as an `alias` on my local machine.

For some reason I cant run regular `uv run python apps/apps.py`

`holiday` - Print the closest federal holiday from today.

`dates` - Date calculator with two uses. 1) Provided a spcific date calculate the date ahead or back n days. 2) Calculate the days between 2 dates. Used this as like a reminder of how many days until my next vacation and little stuff like that.

`interview` - Prints a behavioral prompt, a technical prompt at a given difficulty, and a random Leetcode question title to run through with an interview prep buddy.

`lotto` - Provided a list of space separated names, randomly select members one at a time until all are picked. Useful for group project brainstorm sessions.

`names` - Generates a random name from an sqlite db dependent on the theme you pass it (simpsons|rappers). I use this to demo some random examples of processes.

`savings` - Given a monthly expense amount, prints a 20-year table of annual cost and cumulative savings needed to cover that expense.

`timer` - Runs a timer for a total duration, with optional sub-timer notifications along the way. Plays a sound at each notification. I mostly use this as a pomodoro app or as a timer for making an aeropress.

`tracts` - Downloads census tract data and saves it as a GeoJSON file. It uses the Census and Tiger APIs to fetch data for a specified state, county, and year. The data includes geographic information and census variables such as median age, total population, and median income (adjust in script for now). Requires a `CENSUS_API_KEY` in a `.env` file to function.

# UVX runs

These scripts should be runnable within `uvx` for example

`uvx --from git+https://github.com/flapjackstan/apps apps --help`

`uvx --from git+https://github.com/flapjackstan/apps apps holiday next`

`uvx --from git+https://github.com/flapjackstan/apps apps dates shift 2025-08-21 365 forward`

`uvx --from git+https://github.com/flapjackstan/apps apps dates between 2025-11-08 2026-08-21`

`uvx --from git+https://github.com/flapjackstan/apps apps lotto pick red rza gza ol'dirty ghostface`

`uvx --from git+https://github.com/flapjackstan/apps apps interview prep --difficulty M`

`uvx --from git+https://github.com/flapjackstan/apps apps savings calculate 3000`

`uvx --from git+https://github.com/flapjackstan/apps apps timer start --total 1:00 --sub 0:30`

`uvx --from git+https://github.com/flapjackstan/apps apps tracts download --state CA --county 'Los Angeles' --year 2021`

