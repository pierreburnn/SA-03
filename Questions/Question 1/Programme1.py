from datetime import datetime

file_path = "Questions\Question 1\evenementSAE_15.ics"


# Open the ics file here
def read_ics_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def extract_event_from_ics(ics_content):

    event = {}
    for line in ics_content:
        if line.startswith('UID:'):
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
    return event


def convert_to_pseudo_csv(event):

    date = datetime.strptime(event['start_date'][:8], '%Y%m%d').strftime('%d-%m-%Y')
    start_time = datetime.strptime(event['start_date'][9:15], '%H%M%S').strftime('%H:%M')
    end_time = datetime.strptime(event['end_date'][9:15], '%H%M%S')
    start_time_dt = datetime.strptime(event['start_date'][9:15], '%H%M%S')
    duration = end_time - start_time_dt
    formatted_duration = f"{duration.seconds // 3600:02}:{(duration.seconds // 60) % 60:02}"

    groups = "|".join(event['description'].split('\\n')) if 'description' in event else "empty"
    return f"{event['uid']};{date};{start_time};{formatted_duration};CM;{event['title']};{event['room']};LACAN DAVID;S1"

def main():
    ics_content = read_ics_file(file_path)
    event = extract_event_from_ics(ics_content)
    pseudo_csv = convert_to_pseudo_csv(event)
    print(pseudo_csv)

if __name__ == "__main__":
    main()
