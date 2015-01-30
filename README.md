gabc-to-ly
==========

Produce LilyPond from GABC and extend the GABC format to include chords for organ accompaniments.

Usage:
Convert the GABC to CSV:  
	./gabc2ly <number-of-sharps> <transpose> <file>
Open the CSV manually and add the chords
Convert the CSV to Lilypond:  
	./csv2ly <file>

This project borrows heavily from the GABC Toolkit
	https://github.com/jperon/gabctk

The multiplier column specifies the length of the row in beats.

The "slur" column is for the soprano line, eg "3" means the current line and the next two are slurred.

Known issues:
Can't handle clef changes yet.

