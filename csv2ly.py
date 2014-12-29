#!/usr/bin/python

import csv, sys, io, re

#TODO
#
#
#

#Usage: ./csv2ly <file>

### Files
csv_file = sys.argv[1]
table_file = open(csv_file)
csv_table = csv.reader(table_file, delimiter='\t')
header = next(csv_table)
ly_filename = csv_file.replace('csv', 'csv.ly')
ly_file = open(ly_filename,'w')
ly_template = io.open('template.ly', 'r')

### Multiplier to notelength
# Assume note is a minim. If integer, then note*beats/2. If non integer, then beats/4??
def lilynotelength(mult):
  if mult == "0":
    return ''
  if mult == "1":
    length = "4"
  elif mult == "2":
    length = "2"
  elif mult == "1.5":
    length = "4."
  elif mult == "3":
    length = "2."
  elif ".5" in mult:
    multiplier = float(mult)
    multiplier *= 2
    mult = str(multiplier)
    length = ("2*" + mult + "/4")
  else:
    length = ("2*" + mult + "/2")
  if ".0" in length:
    length = length.replace('.0','')
  return length

##Soprano line
##TODO How to account for variable multiplier, esp. in row 2
##     How to add ~ if note is same as prev. note (could do this in post-processing)
##     
lyrics = ''
soprano_score = ''
alto_score = ''
alto_duration = 1
tenor_score = ''
tenor_duration = 1
bass_score = ''
bass_duration = 1
slur = -1
i = 0
for row in csv_table:
  syllable = row[0]
  beats = row[2]
  duration = lilynotelength(beats)

  ##Lyrics
  lyrics += syllable + ' '

  ##Soprano
  soprano_note = row[4]
  x = row[3]
  if slur == 0:
    soprano_score += ')'
  slur -= 1
  if "\\" in soprano_note:
    soprano_score += ' ' + soprano_note
  elif "--" in soprano_note:
    soprano_score += ' ' + soprano_note
  else:
    soprano_score += ' ' + soprano_note + duration
  if row[3] != '':
    slur = int(row[3])
    soprano_score += ' ('
    slur -= 1
  
#  if syllable == '' and 'Bar' not in soprano_note:
#    soprano_note = '(' + soprano_note

  ##Alto
  alto_note = row[5]
  if alto_note != '':
    alto_total_duration = lilynotelength(str(alto_duration))
    alto_score += alto_note + alto_total_duration + ' '
    alto_duration = float(beats)
  else:
    alto_duration += float(beats)

  ##Tenor
  tenor_note = row[6]
  if tenor_note != '':
    tenor_total_duration = lilynotelength(str(tenor_duration))
    tenor_score += tenor_note + tenor_total_duration + ' '
    tenor_duration = float(beats)
  else:
    tenor_duration += float(beats)

  ##Bass
  bass_note = row[7]
  if bass_note != '':
    bass_total_duration = lilynotelength(str(bass_duration))
    bass_score += bass_note + bass_total_duration + ' '
    bass_duration = float(beats)
  else:
    bass_duration += float(beats)
  i = i + 1


#TODO Add to gabctk: "0" for mult if soprano contains bar

#Hacks...
lyrics = lyrics.replace('*', '&zwj;*')
soprano_score = soprano_score.replace('\\bar \"\"', '')
soprano_score = soprano_score.replace('\\bar \"\'\"', '\\quarterBar')
soprano_score = soprano_score.replace('\\bar \"\"', '\\halfBar')
soprano_score = soprano_score.replace('\\bar \"|\"', '\\singleBar')
soprano_score = soprano_score.replace('\\bar \"||\"', '\\doubleBar')
soprano_score = soprano_score.replace(') (', ' ')
soprano_score = soprano_score.replace(' \\normalsize)',') \\normalsize')
soprano_score = soprano_score.replace(' (\\tiny','\\tiny (')


##Write file
with open("template.ly", "rt") as ly_template:
  for line in ly_template:
    if 'SOPRANO_PART' in line:
      ly_file.write(soprano_score + '\n')
    elif 'ALTO_PART' in line:
      ly_file.write(alto_score + '\n')
    elif 'TENOR_PART' in line:
      ly_file.write(tenor_score + '\n')
    elif 'BASS_PART' in line:
      ly_file.write(bass_score + '\n')
    elif 'LYRICS' in line:
      ly_file.write(lyrics)
    else:
      ly_file.write(line)


#for line in io.open('template.ly', 'r'):

#with open("template.ly", "rt") as ly_template
#  for line in ly_template
#    ly_template.write(line.replace(


""" 
From abc2ly

def duration_to_lilypond_duration  (multiply_tup, defaultlen, dots):
    base = 1
    # (num /  den)  / defaultlen < 1/base
    while base * multiply_tup[0] < multiply_tup[1]:
        base = base * 2
    if base == 1:
        if (multiply_tup[0] / multiply_tup[1])  == 2:
            base = '\\breve'
        if (multiply_tup[0] / multiply_tup[1]) == 3:
            base = '\\breve'
            dots = 1
        if (multiply_tup[0] / multiply_tup[1]) == 4:
            base = '\\longa'
    return '%s%s' % ( base, '.'* dots)

"""
