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
ly_template = io.open('/iomega/CP/NOH/csv/template.ly', 'r')
#ly_template = io.open('/home/ahinkley/Documents/gabctoly/template.ly', 'r')
print(header)
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
  ly_mode = header[12]
except:
  ly_mode = ''
try: 
  noh_page = header[14]
except:
  noh_page = ''

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
soprano_score = '\\tieDown '
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
voiceline = 0
voiceline_score = ''
voiceline_staffA = ''
voiceline_start = ''
voiceline_started = 0
voiceline_staffB = ''
voiceline_end = ''
voiceline_ended = 0
voiceline_duration = 0
voiceline_column = 0
slur = -1
i = 0
division = 0
divison_marker = ''

for row in csv_table:
  syllable = row[0]
  beats = row[2]
  duration = lilynotelength(beats)

  ##Tags
  tags = row[8]

  ##Lyrics
  #Split lyrics into smaller lines
  #Divisions:: 1:Minima 2:Maior 3:Maxima 4:Finalis
  if division > 1:
    lyrics += '\n'
  #Verses, asterisks, etc.
  if "y" in tags:
    syllable = '\n\set stanza = " ' + syllable + ' "'
  #Add syllable
  if syllable != '':
    lyrics += syllable + ' '
  #Continue syllable
  if syllable == '':
    if row[3] != '' and row[4] != soprano_prev_note:
      lyrics += '_ '

  ##Soprano
  soprano_note = row[4]
  x = row[3]
  if slur == 0:
    soprano_score += ')'
  slur -= 1
  if soprano_note == soprano_prev_note:
    if row[0] == '' and row[3] != '':
      soprano_score += ' ~'
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
  if "x" in tags:
    soprano_score += ' \\forceBreak\n'
  if "divisio" in soprano_note:
    soprano_score += '\n'
  if "finalis" in soprano_note:
    soprano_score += '\n'
  soprano_prev_note = soprano_note 
  #Forced line breaks

  ##Alto
  ##TODO These should be separated out into a function
  alto_note = row[5]
  if alto_note != '':
    alto_total_duration = lilynotelength(str(alto_duration))
    alto_score += alto_prev_note + alto_total_duration + ' '
    if alto_note == alto_prev_note and 'r' not in alto_note:
      alto_score += '~ '
    if "a" in tags:
      alto_note = '\\shiftRight ' + alto_note
    if "A" in tags:
      alto_note = '\\shiftRightB ' + alto_note
    if division != 0:
      alto_score += divison_marker + '\n'
    alto_duration = float(beats)
    alto_prev_note = alto_note
  else:
    alto_duration += float(beats)
  if voiceline_started == 'a' and alto_note != '':
    voiceline_start += alto_total_duration
    voiceline_started = 0
  if voiceline_ended == 'a' and alto_note != '':
    voiceline_end += alto_total_duration
    voiceline_ended = 0
    voiceline_score += '\n\\voiceLine ' + voiceline_staffA + ' ' + voiceline_staffB + ' ' + voiceline_start + ' ' + voiceline_end

  ##Tenor
  tenor_note = row[6]
  if tenor_note != '':
    tenor_total_duration = lilynotelength(str(tenor_duration))
    tenor_score += tenor_prev_note + tenor_total_duration + ' '
    if tenor_note == tenor_prev_note and 'r' not in tenor_note:
      tenor_score += '~ '
    if "t" in tags:
      tenor_note = '\\shiftRight ' + tenor_note
    if "T" in tags:
      tenor_note = '\\shiftRightB ' + tenor_note
    if division != 0:
      tenor_score += divison_marker + '\n'
    tenor_duration = float(beats)
    tenor_prev_note = tenor_note
  else:
    tenor_duration += float(beats)
  if voiceline_started == 't' and tenor_note != '':
    voiceline_start += tenor_total_duration
    voiceline_started = 0
  if voiceline_ended == 't' and tenor_note != '':
    voiceline_end += tenor_total_duration
    voiceline_ended = 0
    voiceline_score += '\n\\voiceLine ' + voiceline_staffA + ' ' + voiceline_staffB + ' ' + voiceline_start + ' ' + voiceline_end

  ##Bass
  bass_note = row[7]
  if bass_note != '':
    bass_total_duration = lilynotelength(str(bass_duration))
    bass_score += bass_prev_note + bass_total_duration + ' '
    if bass_note == bass_prev_note and 'r' not in bass_note:
      bass_score += '~ '
    if "b" in tags:
      bass_note = '\\shiftRight ' + bass_note
    if "B" in tags:
      bass_note = '\\shiftRightB ' + bass_note
    if division != 0:
      bass_score += divison_marker + '\n'
    bass_duration = float(beats)
    bass_prev_note = bass_note
  else:
    bass_duration += float(beats)
  if voiceline_started == 'b' and bass_note != '':
    voiceline_start += bass_total_duration
    voiceline_started = 0
  if voiceline_ended == 'b' and bass_note != '':
    voiceline_end += bass_total_duration
    voiceline_ended = 0
    voiceline_score += '\n\\voiceLine ' + voiceline_staffA + ' ' + voiceline_staffB + ' ' + voiceline_start + ' ' + voiceline_end

  ##Voicelines
  #Start of voiceline
  if row[9] != '' and voiceline == 0:    
    if "s" in row[9]:
      voiceline_staffA = '"up"'
      voiceline_start = row[4]
      voiceline_started = 's'
    if "t" in row[9]:
      voiceline_staffA = '"up"'
      voiceline_start = row[5]
      voiceline_started = 't'
    if "t" in row[9]:
      voiceline_staffA = '"down"'
      voiceline_start = row[6]
      voiceline_started = 't'
    if "b" in row[9]:
      voiceline_staffA = '"down"'
      voiceline_start = row[7]
      voiceline_started = 'b'
    voiceline = 1
    voiceline_score += '\ns' + lilynotelength(str(voiceline_duration))
    voiceline_duration = float(beats)
  elif row[9] != '' and voiceline == 1:
    if "s" in row[9]:
      voiceline_staffB = '"up"'
      voiceline_end = row[4]
      voiceline_ended = 's'
    if "a" in row[9]:
      voiceline_staffB = '"up"'
      voiceline_end = row[5]
      voiceline_ended = 'a'
    if "t" in row[9]:
      voiceline_staffB = '"down"'
      voiceline_end = row[6]
      voiceline_ended = 't'
    if "b" in row[9]:
      voiceline_staffB = '"down"'
      voiceline_end = row[7]
      voiceline_ended = 'b'
    voiceline = 0
    voiceline_duration = float(beats)
  else:
    voiceline_duration += float(beats)


     
  #
  #
  # voiceline = 1 voiceline_start = col(SATB)

  i = i + 1
  division = 0
  if "divisioMinima" in soprano_note:
    division = 1
    divison_marker = soprano_note
  if "divisioMaior" in soprano_note:
    division = 2
    divison_marker = soprano_note
  if "divisioMaxima" in soprano_note:
    division = 3
    divison_marker = soprano_note
  if "finalis" in soprano_note:
    division = 4
    divison_marker = soprano_note
#Write last notes of chords
alto_score += alto_prev_note + lilynotelength(str(alto_duration)) + ' ' + divison_marker
tenor_score += tenor_prev_note + lilynotelength(str(tenor_duration)) + ' ' + divison_marker
bass_score += bass_prev_note + lilynotelength(str(bass_duration)) + ' ' + divison_marker


#TODO Add to gabctk: "0" for mult if soprano contains bar

#Hacks...
#lyrics = lyrics.replace('*', '&zwj;*')
lyrics = lyrics.replace('&zwj;* ', '\n\set stanza = " * " ')
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
#Remove all 0/2
alto_score = re.sub('^2\*0\/2','',alto_score)
tenor_score = re.sub('^2\*0\/2','',tenor_score)
bass_score = re.sub('^2\*0\/2','',bass_score)
#Remove spaces at start
alto_score = re.sub('^\s','',alto_score)
tenor_score = re.sub('^\s','',tenor_score)
bass_score = re.sub('^\s','',bass_score)
#NOH uses minims for all "plural" lengths outside soprano line. (Instead of dotted quavers.)
alto_score = alto_score.replace('4.','2*3/4')
tenor_score = tenor_score.replace('4.','2*3/4')
bass_score = bass_score.replace('4.','2*3/4')


##Write file
#Fields: Name, mode, 
with open("/iomega/CP/NOH/csv/template.ly", "rt") as ly_template:
#with open("/home/ahinkley/Documents/gabctoly/template.ly", "rt") as ly_template:
  for line in ly_template:
    if 'SOPRANO_PART' in line:
      ly_file.write(soprano_score + '\n')
    elif 'ALTO_PART' in line:
      ly_file.write(alto_score + '\n')
    elif 'TENOR_PART' in line:
      ly_file.write(tenor_score + '\n')
    elif 'BASS_PART' in line:
      ly_file.write(bass_score + '\n')
    elif 'VOICELINES' in line:
      ly_file.write(voiceline_score + '\n')
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
