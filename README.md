# GPT-Code
Code developed with OpenAI's GPT

bitflipper.c copies a file and flips a random bit within the file. Used to confirm error checking and correction code for things like reed-solomon.

twitchpartnercheck.py takes a twitch streamers account name as a command line argument and returns whether they are a partner or affiliate.

yt_trans.py takes the videoid of a youtube video as an argument, downloads the transcript using yt_dlp, then passes the transcript to chatgpt for summarization. Requires a transcript.prompt file containing the prompt for chatgpt, and a cookies.txt for yt_dlp. My normal transcript.prompt is: "Provide a detailed summary fo the following transcript. call out any novel concepts, philosophies, and action items.
Call out any cognitive errors or poor reasoning use by the speakers that might be present in arguments for a conclusion, especially confirmation bias. This is any cognitive errors that the speaker might be using, rather than any cognitive errors the speaker is discussing."
