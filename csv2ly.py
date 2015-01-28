#!/usr/bin/python

import csv, sys, io, re

#TODO
# Add key signature?
# add tie if note equals previous note. Global variables prev_sop, etc?
#

#Usage: ./csv2ly <file>

### Files and metadata
csv_file = sys.argv[1]
table_file = open(csv_file)
csv_table = csv.reader(table_file, delimiter='\t')
header = next(csv_table)
ly_filename = re.sub('csv$','csv.ly',csv_file)
ly_file = open(ly_filename,'w')
ly_template = io.open('template.ly', 'r')
try: 
  ly_key = header[9]
except:
  ly_key = ''
try: 
  ly_title = header[10]
except:
  ly_title = ''
try: 
  ly_genre = header[11]
except:
  ly_genre = ''
try: 
  noh_page = header[13]
except:
  ly_mode = ''

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
##     
lyrics = ''
soprano_score = ''
soprano_prev_note = ''
alto_score = ''
alto_prev_note = ''
alto_duration = 0
tenor_score = ''
tenor_prev_note = ''
tenor_duration = 0
bass_score = ''
bass_prev_note = ''
bass_duration = 0
slur = -1
i = 0
division = 0
divison_marker = ''

for row in csv_table:
  syllable = row[0]
  beats = row[2]
  duration = lilynotelength(beats)

  ##Lyrics
  if syllable != '':
    lyrics += syllable + ' '
  if syllable == '':
#    if row[3] != '':
    if slur <= 0:
      lyrics += '_ '

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
  if "divisio" in soprano_note:
    soprano_score += '\n'
  if "finalis" in soprano_note:
    soprano_score += '\n'
  soprano_prev_note = soprano_note

  ##Alto
  alto_note = row[5]
  if alto_note != '':
    alto_total_duration = lilynotelength(str(alto_duration))
    alto_score += alto_prev_note + alto_total_duration + ' '
    if alto_note == alto_prev_note:
      alto_score += '~ '
    if division == 1:
      alto_score += divison_marker + '\n'
    alto_duration = float(beats)
    alto_prev_note = alto_note
  else:
    alto_duration += float(beats)

  ##Tenor
  tenor_note = row[6]
  if tenor_note != '':
    tenor_total_duration = lilynotelength(str(tenor_duration))
    tenor_score += tenor_prev_note + tenor_total_duration + ' '
    if tenor_note == tenor_prev_note:
      tenor_score += '~ '
    if division == 1:
      tenor_score += divison_marker + '\n'
    tenor_duration = float(beats)
    tenor_prev_note = tenor_note
  else:
    tenor_duration += float(beats)

  ##Bass
  bass_note = row[7]
  if bass_note != '':
    bass_total_duration = lilynotelength(str(bass_duration))
    bass_score += bass_prev_note + bass_total_duration + ' '
    if bass_note == bass_prev_note:
      bass_score += '~ '
    if division == 1:
      bass_score += divison_marker + '\n'
    bass_duration = float(beats)
    bass_prev_note = bass_note
  else:
    bass_duration += float(beats)

  i = i + 1
  division = 0
  if "divisio" in soprano_note:
    division = 1
    divison_marker = soprano_note
  if "finalis" in soprano_note:
    division = 1
    divison_marker = soprano_note

#TODO Add to gabctk: "0" for mult if soprano contains bar

#Hacks...
#lyrics = lyrics.replace('*', '&zwj;*')
#soprano_score = soprano_score.replace('\\bar \"\"', '')
#soprano_score = soprano_score.replace('\\bar \"\'\"', '\\quarterBar')
#soprano_score = soprano_score.replace('\\bar \"\"', '\\halfBar')
#soprano_score = soprano_score.replace('\\bar \"|\"', '\\singleBar')
#soprano_score = soprano_score.replace('\\bar \"||\"', '\\doubleBar')
soprano_score = soprano_score.replace(') (', ' ')
soprano_score = soprano_score.replace(' \\normalsize)',') \\normalsize')
soprano_score = soprano_score.replace(' (\\tiny','\\tiny (')
lyrics = lyrics.replace('--', ' --')
#Remove all 2/2
alto_score = alto_score.replace('2*2/2','2')
tenor_score = tenor_score.replace('2*2/2','2')
bass_score = bass_score.replace('2*2/2','2')
#Replace 2*1/2 with 4
alto_score = alto_score.replace('2*1/2','4')
tenor_score = tenor_score.replace('2*1/2','4')
bass_score = bass_score.replace('2*1/2','4')

##Write file
#Fields: Name, mode, 
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
    elif 'KEY_SIGNATURE' in line:
      line = line.replace('KEY_SIGNATURE', str(ly_key))
      ly_file.write(line)
    elif 'GABC_TITLE' in line:
      line = line.replace('GABC_TITLE', str(ly_title))
      ly_file.write(line)
    elif 'GABC_GENRE' in line:
      line = line.replace('GABC_GENRE', str(ly_genre))
      ly_file.write(line)
    elif 'GABC_MODE' in line:
      line = line.replace('GABC_MODE', str(ly_mode))
      ly_file.write(line)
    elif 'NOH_PAGE' in line:
      line = line.replace('NOH_PAGE', str(noh_page))
      ly_file.write(line)
    else:
      ly_file.write(line)
