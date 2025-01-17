import csv
from datetime import datetime

### MOODLE FILE PATH
ics_file_path = 'Questions/Question 2/ADE_RT1_Septembre2023_Decembre2023.ics'
### CSV FILE PATH
csv_file_path = 'Questions/Question 2/Sorting File.csv'
csv_file_path_in_question3_section = 'Questions/Question 3/Sorting File.csv'


### READ THE PREVIOUS FILE
def read_ics_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def extract_events_from_ics(ics_content):

    events = []
    event = {}

    for line in ics_content:
        line = line.strip()
        if line.startswith('BEGIN:VEVENT'):
            event = {}

        elif line.startswith('UID:'):
            event['uid'] = line.split(':', 1)[1].strip()

        elif line.startswith('DTSTART:'):
            event['start_date'] = line.split(':', 1)[1].strip()

        elif line.startswith('DTEND:'):
            event['end_date'] = line.split(':', 1)[1].strip()

        elif line.startswith('SUMMARY:'):
            event['title'] = line.split(':', 1)[1].strip()

        elif line.startswith('LOCATION:'):
            event['room'] = line.split(':', 1)[1].strip()

        elif line.startswith('DESCRIPTION:'):
            event['description'] = line.split(':', 1)[1].strip()

        elif line.startswith('END:VEVENT'):
            events.append(event)

    return events


def convert_to_pseudo_csv(event):

    date = datetime.strptime(event['start_date'][:8], '%Y%m%d').strftime('%d-%m-%Y')
    start_time = datetime.strptime(event['start_date'][9:15], '%H%M%S').strftime('%H:%M')
    end_time = datetime.strptime(event['end_date'][9:15], '%H%M%S')
    start_time_dt = datetime.strptime(event['start_date'][9:15], '%H%M%S')
    duration = end_time - start_time_dt
    formatted_duration = f"{duration.seconds // 3600:02}:{(duration.seconds // 60) % 60:02}"

    groups = "|".join(event['description'].split('\\n')) if 'description' in event else "empty"
    room = event.get('room', 'empty').replace('\\,', '|')

    return [
        event['uid'], 
        date, 
        start_time, 
        formatted_duration, 
        "CM",  
        event['title'], 
        room, 
        "empty",  
        groups
    ]


### EXECUTE FUNCTIONS AND STORE THE RETURN IN THE VARIABLE
ics_content = read_ics_file(ics_file_path)
events = extract_events_from_ics(ics_content)
pseudo_csv_table = [convert_to_pseudo_csv(e) for e in events]


### SORT EVENTS BY DATE AND TIME
pseudo_csv_table.sort(key=lambda x: (x[1], x[2]))


### OPEN OR CREATE THE CSV FILE WITH "mode = 'w'" AND CREATE THE DIFFERENT COLUMNS
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:

    writer = csv.writer(csv_file, delimiter=';') # when a semicolon is found in the code, we change line, move to the next
    writer.writerow(["UID", "Date", "Start Time", "Duration", "Mode", "Title", "Room", "Professors", "Groups"])
    writer.writerows(pseudo_csv_table)

with open(csv_file_path_in_question3_section, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(["UID", "Date", "Start Time", "Duration", "Mode", "Title", "Room", "Professors", "Groups"])
    writer.writerows(pseudo_csv_table)


print(pseudo_csv_table)
