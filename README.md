# KIDS2UBIART
Converts just dance kids '.bin' files into ubiart tmls.

## SUPPORTED GAMES
* Just Dance Kids 1 (Wii)
* Just Dance Kids 2 (Wii, XBOX 360)
* Just Dance Kids 2014 (Wii, XBOX 360)
* Just Dance Disney Party 1 (Wii, XBOX 360)
* Just Dance Disney Party 2 (Wii, XBOX 360)
* The Smurfs Dance Party (Wii)
* The Hip Hop Dance Experience (Wii)

## SETTINGS
* BPM: Reads BPM of a song.
* beatAmount: Total beats (in other words, endbeat).
* beatType: Chooses between beatAmount or milliseconds to generate beats.
* mapInput: Reading bin names from the input folder.
* shakeRange: Splits shake moves from the duration you put in. (0 = OFF)
* offset (move, picto, lyric): Changes the starttime offset.
* lyricLanguage: Input values chooses different language from the text file (0 = English, 1 = French, 2 = Spanish, etc.).
* gestureType: Platform for gesture files (x360, orbis, durango).
* hideuiClips: Enables hide user interface clips (used for jddisney 1-2, kids 2014 and hip hop dance experience during dance breaks)
* goldEffectType: Adds goldmove effects coming from pictos or moves.
* dumpTraces: Writing json data for right hand traces made only for smurfs maps. "_trace.bin"
* dumpJSON: Writes json data of every tml (in milliseconds).

## CREDITS
* planedec50: Converting miliseconds to 24 seconds per beat (for ubiart)
* Elliot/MZommer: Some class info and data from the bin files

## NOTES
Please note that there may be some bugs that I haven't discovered yet. If you run into any bugs, let me know.
### JDKIDS 1
* The last move (always a goldmove) isn't used due to clip count or reading useless classes (removed the last goldmove effect as well).
