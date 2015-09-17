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

The column after the bass, column I or row[9] contains the line breaks and rightshifts. If a coinciding note (with another voice) is shifted to the right, it is indicated with an s, a, t, or b, depending on which note is shifted. An "x" in the column means a line break in the original books. A "y" indicates the lyric is a verse number/marker.

The next column after "B" is for the voice lines. Place an "s", "a", "t", or "b" where the voice line starts and ends.

This project also borrows heavily from the Nova Organi Harmonia project.
	https://github.com/CMAA/nova-organi-harmonia
The file noh_test is based on noh.ily and is a work in progress, as the name implies.
