#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#Usage: gabc2ly <number-of-sharps> <file>

#TODO
#Note groups - extra column to start or end slurs

import os, sys, re, getopt, io, csv

#Parameters
#for opt, arg in opts:
#  opts, args = getopt.getopt(argv, "i:k")
#    gabc_filename = arg
#  elif opt in ("-k"):
#    key_signature = int(arg)
#  elif opt in ("-d"):
#    adjust = int(arg)
key_signature = sys.argv[1]
semitone_adjust = sys.argv[2]
gabc_filename = sys.argv[3]

gabc_file = open(gabc_filename)
ly_filename = gabc_filename.replace('gabc', 'gabc.ly')
csv_filename = gabc_filename.replace('gabc', 'gabc.csv')

gabcvalues = {"a":45, "b":47, "c":48, "d":50, "e":52, "f":53, "g":55, "h":57, "i":59, "j":60, "k":62, "l":64, "m":65, "A":45, "B":47, "C":48, "D":50, "E":52, "F":53, "G":55, "H":57, "I":59, "J":60, "K":62, "L":64, "M":65}
'''
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

gabc_code = ''
clef = ''
flat = False

def clef_adjust(clef):
  x = 0
  if clef[0] == 'f':
    x += 3
  if clef[1] == '3':
    x += 3
  if clef[1] == '2':
    x += 7
  if clef[1] == '1':
    x += 11
  return x

def g2midi(note):
  #TODO
  #Add other modifiers
  #Restrict flat to particular note, change true/false to "note"
  #Try if x, flat = gabcnote; if y, or eow, flat = ''
  global flat
  gabcnote = note[0]
  value = gabcvalues[gabcnote]
  if len(note) >= 2:
    modifier = note[1]
    if modifier == "x":
      flat = True
    if modifier == "y":
      flat = False
  return value

def transpose(value):
  global clef
  key = int(key_signature)
  if key >= 0:
    return int(value) + clef_adjust('clef') + (7*key%12)
  else:
    return int(value) + clef_adjust('clef') + (7*key%12) - 12

def lily(value):
  value = int(value)
  if flat == True:
    value -= 1
  o = int(value / 12) - 1
  n = int(value % 12)
  if int(key_signature) >= 0:
    note = ('c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b')[n]
  else:
    note = ('c', 'des', 'd', 'ees', 'e', 'f', 'ges', 'g', 'aes', 'a', 'bes', 'b')[n]
  note += (", , ", ", ", "", "'", "''", "'''", "''''")[o-1]
  return note

#def adjust(value):

def bar(sym):
  if "::" in sym:
    return "\\doubleBar"
  if ":" in sym:
    return "\\singleBar"
  if ";" in sym:
    return "\\halfBar"
  if "," in sym:
    return "\\quarterBar"
  if "`" in sym:
    return ""

print(lily("58"))
###########################################

#Read in file, ignore headers
offset = 0
header_line = 1
for line in gabc_file:
  if header_line == 0:
    gabc_code = gabc_code + line
  if "%%" in line:
    header_line = 0
  
#Convert to list
gabc_syllables = re.sub('(\([^\)]*\))([^ ])', '--\g<1>\g<2>', gabc_code)
gabc_syllables = gabc_syllables.replace('\) \(','')
gabc_syllables = gabc_syllables.replace(' ', '|')
gabc_syllables = gabc_syllables.split(")")

#Create list of syllables and notes
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
      notes = re.sub('([a-mA-M])([^a-mA-M]*)','\g<1>\g<2>\n\t',k[1])
      notes = re.sub('\n\t$','',notes)
      out_file.write(lyric + "\t" + notes + '\n')
    except:
      pass
out_file.close()

#Open csv, write full csv
with open('output.csv','r') as gabc_table:
  with open('output2.csv','w') as output_csv:
    output_csv.write("Syllable\tGABC\tMultiplier\tSlur\tS\tA\tT\tB\n")
    csv_table = csv.reader(gabc_table, delimiter='\t')
    for row in csv_table:
      lyric = row[0]
      if '|' in lyric:
        flat = False
        lyric = re.sub('\|','',lyric)
      note = row[1]
      if re.match('[cf][1-4]', note) is not None:
        clef = note
      elif re.match('[a-mA-M]', note) is not None:
        if 'w' in note:
          midi = transpose(g2midi(note)) + clef_adjust(clef) + int(semitone_adjust)
          output_csv.write(lyric + "\t" + note + "\t1\t\t" + lily(midi) + "\\prall\n")
        elif '~' in note:
          midi = transpose(g2midi(note)) + clef_adjust(clef) + int(semitone_adjust)
          output_csv.write(lyric + "\t" + note + "\t1\t\t" + "\\tiny " + lily(midi) + " \\normalsize\n")
        if '//' in note:
          midi = transpose(g2midi(note)) + clef_adjust(clef) + int(semitone_adjust)
          output_csv.write(lyric + "\t" + note + "\t1.5\t\t" + lily(midi) + "\n")
        elif 'x' in note:
          output_csv.write(lyric + "\t" + note + "\t0\t\t" + "\n")
        elif 'y' in note:
          output_csv.write(lyric + "\t" + note + "\t0\t\t" + "\n")
        else:
          midi = transpose(g2midi(note)) + clef_adjust(clef) + int(semitone_adjust)
          output_csv.write(lyric + "\t" + note + "\t1\t\t" + lily(midi) + "\n")
#        output_csv.write(lyric + "\t" + note + "\t1\t\t" + adjust(midi) + "\n")
      elif re.match('[`,;:]', note) is not None:
        output_csv.write(lyric + "\t" + note + "\t0\t\t" + bar(note) + "\n")


    


