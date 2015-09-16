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

The first column after "B" is for the voice lines. Place an s, a, t, or b where the voice line starts and ends.
The next column contains an "x" wherever a line break occurs in the original books.

This project also borrows heavily from the Nova Organi Harmonia project.
	https://github.com/CMAA/nova-organi-harmonia
The file noh_test is based on noh.ily and is a work in progress, as the name implies.
