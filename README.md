# GPT-Code
Code developed with OpenAI's GPT

bitflipper.c copies a file and flips a random bit within the file. Used to confirm error checking and correction code for things like reed-solomon.

twitchpartnercheck.py takes a twitch streamers account name as a command line argument and returns whether they are a partner or affiliate.

yt_trans.py takes the videoid of a youtube video as an argument, downloads the transcript using yt_dlp, then passes the transcript to chatgpt for summarization.

trng.py pulls random data from the adafruit tinkey qt2040 TRNG

xorfiles.c takes two files and XORs them. it assumes they're the same length. IDK what happens if they aren't

randbytes.c outputs argv or random bytes using arc4random_buf on macos. It may work on other platforms.
