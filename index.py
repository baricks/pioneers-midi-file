from miditime.miditime import MIDITime
from datetime import datetime
import calendar
import time
import json

with open('data.json') as json_data:
    my_data = json.load(json_data)

mymidi = MIDITime(120, 'pioneers.mid', 5, 5, 1)

# Convert the time string to a datetime object
my_data_epoched = [{'days_since_epoch': calendar.timegm(time.strptime(d['date'],'%d %m %Y'))/100000, 'pioneers': d['pioneers']} for d in my_data]

my_data_timed = [{'beat': mymidi.beat(d['days_since_epoch']), 'pioneers': d['pioneers']} for d in my_data_epoched]

start_time = my_data_timed[0]['beat']

def mag_to_pitch_tuned(pioneers):
    scale_pct = mymidi.linear_scale_pct(1, 1057, pioneers) #from 0.0 to 1.0

    # Range of notes.
    # c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    # d_minor = ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']
    c_pent = [ 'C', 'D', 'E', 'G', 'A']

    # Find the note that matches data point
    note = mymidi.scale_to_note(scale_pct, c_pent) #D5 E5 F5 etc

    # Translate that note to a MIDI pitch
    midi_pitch = mymidi.note_to_midi_pitch(note) #from 62 to 64

    return midi_pitch

notes_list = []

for d in my_data_timed:
    notes_list.append([
        d['beat'] - start_time, # Rhythm
        mag_to_pitch_tuned(d['pioneers']), # Pitch
        100,  # Velocity
        3  # Duration, in beats
    ])

# Add a track with those notes
mymidi.add_track(notes_list)

# Output the .mid file
mymidi.save_midi()
