#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#Usage: gabc2ly <number-of-sharps> <file>

#TODO:
#vv shortcut -> x ~ x
#
#Repeat loop if ij or iij 
# - ij: repeat = 2, ij = ''
# - iij repeat = 3, iij = ij
#
#Handle clef changes
#
#add parameters...
#for opt, arg in opts:
#  opts, args = getopt.getopt(argv, "i:k")
#    gabc_filename = arg
#  elif opt in ("-k"):
#    key_signature = int(arg)
#  elif opt in ("-d"):
#    adjust = int(arg)

''' Extra variables to incorporate...
gabcnotes = "abcdefghijklm"
episeme = '_'
point = '.'
ictus = "'"
quilisma = 'w'
liquescence = '~'
special = 'osvOSV'
bars = '`, ;:'
flat = "x"
natural = "y"
cut = '/ '
'''

import os, sys, re, getopt, io, csv

if len(sys.argv) != 4:
  sys.exit("Usage: gabc2ly <number-of-sharps> <transpose (semitones)> <file>")

#Parameters:
sharps = int(sys.argv[1])
semitone_adjust = sys.argv[2]
gabc_filename = sys.argv[3]

#Files:
gabc_file = open(gabc_filename)
ly_filename = gabc_filename.replace('gabc', 'gabc.ly')
csv_filename = gabc_filename.replace('gabc', 'gabc.csv')

#Variables:
key_transpose = 7*sharps % 12
#if sharps < 0:
#  key_transpose -= 12
gabcnotes = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m","n", "o", "p", "q", "r", "s", "t")
gabcnotes_caps = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M")
clef_adjust = {"c4":0, "c3":2, "c2":4, "c1":6, "f4":3, "f3":5, "f2":0, "f1":2}
gabcvalues = {"a":45, "b":47, "c":48, "d":50, "e":52, "f":53, "g":55, "h":57, "i":59, "j":60, "k":62, "l":64, "m":65, "n":67, "o":69, "p":71, "q":72, "r":74, "s":76, "t":77}
gabc_code = ''
clef = "c3" #Default for Gregorio
flat = ''
ly_title = ''
ly_mode = ''
ly_genre = ''

#Key signature variables
lastnote = ''
lastmidi = 60
mode = {0:"major", 2:"dorian", 4:"phrygian", 5:"lydian", 7:"mixolydian", 9:"minor", 11:"locrian"}

def flatnote(note):
  global flat
  gabcnote = note
  value = gabcnotes.index(gabcnote)
  clef_value = clef_adjust[clef]
  value += clef_value
  flat = (gabcvalues[gabcnotes[value]] + key_transpose ) % 12

#Get MIDI value of note
def g2midi(note):
  global flat
  global clef
  gabcnote = note[0]
  if re.match('[A-M]', note) is not None:
    value = gabcnotes_caps.index(gabcnote)
  else:
    value = gabcnotes.index(gabcnote)
  clef_value = clef_adjust[clef]
  value += clef_value
  if len(note) >= 2:
    modifier = note[1]
    if modifier == "x":
      flatnote(gabcnote)
    if modifier == "y":
      flat = ''
  return gabcvalues[gabcnotes[value]] + key_transpose

#Convert MIDI value to LilyPond value
def lily(value):
  value = int(value)
  if value % 12 == flat:
    value -= 1
  o = int(value / 12) - 1
  n = int(value % 12)
  if sharps > 0:
    note = ('c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b')[n]
  else:
    note = ('c', 'des', 'd', 'ees', 'e', 'f', 'ges', 'g', 'aes', 'a', 'bes', 'b')[n]
  note += (", , ", ", ", "", "'", "''", "'''", "''''")[o-1]
  return note

#Bars and divisions
def bar(sym):
  if "::" in sym:
    return "\\finalis"
#    return "\\doubleBar"
  if ":" in sym:
    return "\\divisioMaxima"
#    return "\\singleBar"
  if ";" in sym:
    return "\\divisioMaior"
#    return "\\halfBar"
  if "," in sym:
    return "\\divisioMinima"
#    return "\\quarterBar"
  if "`" in sym:
    return ""

###########################################

#Read in GABC file, skip the headers
offset = 0
header_line = 1
for line in gabc_file:
  if re.match('^name:', line) is not None:
    ly_title = line
    ly_title = re.sub('^[^:]*:','', ly_title)
    ly_title = re.sub(';$','', ly_title)
    ly_title = re.sub('\n','', ly_title)
  if re.match('^mode:', line) is not None:
    ly_mode = line
    ly_mode = re.sub('^[^:]*:','', ly_mode)
    ly_mode = re.sub(';$','', ly_mode)
    ly_mode = re.sub('\n','', ly_mode)
  if re.match('^office-part:', line) is not None:
    ly_genre = line
    ly_genre = re.sub('^[^:]*:','', ly_genre)
    ly_genre = re.sub(';$','', ly_genre)
    ly_genre = re.sub('\n','', ly_genre)
  
  if header_line == 0:
    gabc_code = gabc_code + line
  if "%%" in line:
    header_line = 0
  
#Convert to list of syllables (with notes)
gabc_syllables = re.sub('(\([^\)]*\))([^ ])', '--\g<1>\g<2>', gabc_code)
gabc_syllables = gabc_syllables.replace('\) \(','')
gabc_syllables = gabc_syllables.replace(' ', '|')
gabc_syllables = gabc_syllables.split(")")

#Separate out syllables and notes, write to CSV
with open('output.csv', 'w') as out_file:
  for i,j in enumerate(gabc_syllables):
    k = j.split("(")
    if i == 0:
      clef = k[1]
    try:
#     lyric = k[0] with substitutions:
      lyric = k[0]\
            .replace('*', '&zwj;*')\
            .replace('<i>', '').replace('</i>', '')\
            .replace('<b>', '').replace('</b>', '')\
            .replace('ae', 'æ')\
            .replace('áe', 'ǽ')\
            .replace('aé', 'ǽ')\
            .replace('oe', 'œ')\
            .replace('óe', 'œ́')\
            .replace('oé', 'œ́')\
            .replace('<sp>R/</sp>', '℟')\
            .replace('<sp>V/</sp>', '℣')\
            .replace('<sp>ae</sp>', 'æ')\
            .replace("<sp>'ae</sp>", 'ǽ')\
            .replace("<sp>'æ</sp>", 'ǽ')\
            .replace('<sp>AE</sp>', 'Æ')\
            .replace("<sp>'AE</sp>", 'Ǽ')\
            .replace("<sp>'Æ</sp>", 'Ǽ')\
            .replace('<sp>oe</sp>', 'œ')\
            .replace("<sp>'oe</sp>", 'œ́')\
            .replace("<sp>'œ</sp>", 'œ́')\
            .replace('<sp>OE</sp>', 'Œ')\
            .replace("<sp>'OE</sp>", 'Œ́')\
            .replace("<sp>'Œ</sp>", 'Œ́')
      notes = re.sub('([a-mA-M\.,;:])([^a-mA-M]*)','\g<1>\g<2>\n\t',k[1])
      notes = re.sub('\n\t$','',notes)
      out_file.write(lyric + "\t" + notes + '\n')
    except:
      #out_file.write("\t\n")
      pass
out_file.close()


#Determine key
with open('output.csv','r') as gabc_table:
  csv_table = csv.reader(gabc_table, delimiter='\t')
  for row in csv_table:
    note = row[1]
    if re.match('[a-mA-M]', note) is not None:
      midi = g2midi(note) + int(semitone_adjust)
      lastnote = lily(midi)
      lastnote = re.sub('\'','',lastnote)
      lastmidi = midi
gabc_table.close()
key_mode_value = (lastmidi - 7*sharps) % 12
key_mode = mode[key_mode_value]

#Open csv, write full csv
with open('output.csv','r') as gabc_table:
  with open('output2.csv','w') as output_csv:
    csv_table = csv.reader(gabc_table, delimiter='\t')
    output_csv.write("Syllable\tGABC\tMultiplier\tSlur\tS\tA\tT\tB\t" + str(sharps) + " Sharps, Key = \t" + str(lastnote) + " \\" + str(key_mode) + "\t" + str(ly_title) + "\t" + str(ly_genre) + "\t" +  str(ly_mode) + "\t" + "Gregorio clef: " + str(clef) + ", transposed " + str(semitone_adjust) + " semitones.\n")
    print(str(sharps) + " Sharps, Key = \n" + str(lastnote) + " \\" + str(key_mode) + "\n" + str(ly_title) + "\n" + str(ly_genre) + "\n" +  str(ly_mode) + "\n" + "Gregorio clef: " + str(clef) + ", transposed " + str(semitone_adjust) + " semitones. Pageref pp:\t\n")
    #Write the output file
    for row in csv_table:
      lyric = row[0]
      if '|' in lyric:
        flat = ''
        lyric = lyric.replace('|--','')
        lyric = lyric.replace('|','')
      note = row[1]
      if re.match('[cf][1-4]', note) is not None:
        clef = note
      elif re.match('[a-mA-M]', note) is not None:
        if 'w' in note:
          midi = g2midi(note) + int(semitone_adjust)
          output_csv.write(lyric + "\t" + note + "\t1\t\t" + lily(midi) + "\\prall\t\t\t\n")
        elif '~' in note:
          midi = g2midi(note) + int(semitone_adjust)
          output_csv.write(lyric + "\t" + note + "\t1\t\t" + "\\tiny " + lily(midi) + " \\normalsize\t\t\t\n")
        elif '//' in note:
          midi = g2midi(note) + int(semitone_adjust)
          output_csv.write(lyric + "\t" + note + "\t1.5\t\t" + lily(midi) + "\t\t\t\n")
        elif 'x' in note:
          flatnote(note[0])
          output_csv.write(lyric + "\t" + note + "\t0\t\t" + "\t\t\t\n")
        elif 'y' in note:
          flat = ''
          output_csv.write(lyric + "\t" + note + "\t0\t\t" + "\t\t\t\n")
        elif 'vv' in note:
          output_csv.write(lyric + "\t" + note + "\t1\t\t" + lily(midi) + "\t\t\t\n")
          output_csv.write("\t" + note + "\t1\t\t" + lily(midi) + "\t\t\t\n")
        else:
          midi = g2midi(note) + int(semitone_adjust)
          output_csv.write(lyric + "\t" + note + "\t1\t\t" + lily(midi) + "\t\t\t\n")
      elif re.match('[`,;:]', note) is not None:
        output_csv.write(lyric + "\t" + note + "\t0\t\t" + bar(note) + "\t\t\t\n")
      else:
        output_csv.write(lyric + "\t\t0\t\t\t\t\t\n")



    


