gabc-to-ly
==========

Produce LilyPond from GABC and extend the GABC format to include chords for organ accompaniments.

Usage:
Convert the GABC to CSV
	./gabc2ly <number-of-sharps> <transpose> <file>
Open the CSV manually and add the chords
Convert the CSV to Lilypond
	./csv2ly <file>

Known issues:
The clef adjust adjusts semitones instead of notes.
