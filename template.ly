\version "2.18"
%\include "/home/ahinkley/noh.ily"
%\include "/iomega/CP/NOH/noh.ily"
%\include "gregorian.ly"
\include "/iomega/CP/NOH/test/noh_test.ly"
%\include "L:\CP\NOH\test\noh_test.ly"

%Page reference: page NOH_PAGE
%(volume.page)

global = {
 \key KEY_SIGNATURE
 \cadenzaOn 
}

\header {
  title = "GABC_TITLE"
  tagline = ""
  composer = ""
}

\paper {
 #(include-special-characters)
  oddHeaderMarkup = \markup \fill-line {
    \line {}
    \center-column {
      \on-the-fly #first-page     " "
      \on-the-fly #not-first-page "GABC_TITLE"
    }
    \line { \on-the-fly #print-page-number-check-first \fromproperty #'page:page-number-string }
  }
  evenHeaderMarkup = \markup \fill-line {
    \line { \on-the-fly #print-page-number-check-first \fromproperty #'page:page-number-string }
    \center-column { "GABC_TITLE" }
    \line {}
  }
}

chantText = \lyricmode {
  LYRICS
}

chantMusic = {
  SOPRANO_PART
}

altoMusic = {
  ALTO_PART
}

tenorMusic = {
  TENOR_PART
}

bassMusic = {
  BASS_PART
}

voiceLines = {
  VOICELINES
}

\score{
  <<
    \new GrandStaff <<
      \set GrandStaff.autoBeaming = ##f
      \set GrandStaff.instrumentName = \markup \center-column {
        "GABC_GENRE"
        "GABC_MODE"
      }
      \new Staff = up <<
        \new Voice = "chant" {
          \voiceOne \global \chantMusic
        }
        \new Voice {
          \voiceTwo \global \altoMusic
        }
      >>

      \new Staff = down <<
        \clef bass
        \new Voice {
          \voiceOne \global \tenorMusic
        }
        \new Voice {
          \voiceTwo \global \bassMusic
        }
	\new Voice {
        \voiceThree \global \voiceLines
        }
      >>
    >>
    \new Lyrics \lyricsto chant {
      \chantText
    }
  >>
  \layout{
  }
  \midi{
    \tempo 4 = 125
  }
}
