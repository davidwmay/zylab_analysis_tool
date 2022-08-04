import pandas as pd
import requests
import zipfile
import os.path
import incdev
import csv
import io

from submission import Submission
from datetime import datetime

def get_valid_datetime(timestamp):
    """ Get valid datetime based on given timestamp.
    
        Parameters
        ----------
        timestamp : `str`
            Timestamp of the given activity row
    
        Returns
        -------
        valid_datetime : `datetime.datetime`
            Valid datetime for the given timestamp
    
        Raises
        ------
        ValueError
            Raised if the timestamp given cannot be converted into a valid datetime.
    
        Notes
        -----
        Expected csv format: 2017-04-05 17:01:12
        Excel format: yyyy-mm-dd h:mm:ss
        New log file has extra time information after the h:mm:ss timestamp
    """
    t = timestamp
    t_split = timestamp.split()
    if t_split[1].find("-"):
        t_split[1] = t_split[1][0:t_split[1].find("-")]
        t = ' '.join(t_split)
    
    for fmt in ('%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(t, fmt)
        except ValueError:
            pass
    raise ValueError('Cannot recognize datetime format: ' + t)


def get_code(url):
    """ Download a student's code submission.

    Parameters
    ----------
    url : `str`
        URL of the zip file to be downloaded

    Returns
    -------
    url : `datetime.datetime`
        URL of the zip file that was downloaded

    result : `str`
        Code submission

    Raises
    ------
    ConnectionError
        Raised if the submission could not be downloaded
    
    """

    try:
        response = requests.get(url)
        zfile = zipfile.ZipFile(io.BytesIO(response.content))
        filenames = zfile.namelist()
        content = zfile.open(filenames[0], 'r').read()
        result = content.decode('utf-8')
        return (url, result)
    except ConnectionError:
        return (url, "Max retries met, cannot retrieve student code submission")

if __name__ == "__main__":
    # Stores IncDev analysis results
    data = {}
    # Stores user metadata (name, email)
    metadata = {}

    filename = input('Enter logfile name: ')
    filepath = os.path.join('input', filename)
    output_file = 'output_' + filename

    # Read log file into pandas df, filter to only include students
    logfile = pd.read_csv(filepath)
    logfile = logfile[logfile.role == 'Student']

    for row in logfile.itertuples():
        if row.user_id not in data:
            data[row.user_id] = {}
            metadata[row.user_id] = {}
            metadata[row.user_id]['name'] = row.first_name + ' ' + row.last_name
            metadata[row.user_id]['email'] = row.email
        if row.content_section not in data[row.user_id]:
            data[row.user_id][row.content_section] = {}
            data[row.user_id][row.content_section] = []
        # Download code submission
        url, result = get_code(row.zip_location)
        # Create new Submission object, add to dict
        sub = Submission(
            student_id = row.user_id,
            crid = row.content_resource_id,
            lab_id = row.content_section,
            submission_id = row.zip_location.split('/')[-1],
            type = row.submission,
            code = result,
            sub_time = get_valid_datetime(row.date_submitted),
            anomaly_dict=None,
            score = row.score
        )
        data[row.user_id][row.content_section].append(sub)

    # Generate nested dict of IncDev results
    output = incdev.run(data)

    # Create output directory if it doesn't already exist
    try:
        os.mkdir('output')
    except Exception:
        pass

    # Write IncDev results to csv
    with open(os.path.join('output', 'output_' + filename), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User ID', 'Name', 'Email', 'Lab ID', 'IncDev Score', 'IncDev Trail', 'LOC Trail', 'Time Trail', 'Coding Trail', 'Drastic Change Trail'])
        for user_id in output:
            uid = user_id
            name = metadata[user_id]['name']
            email = metadata[user_id]['email']
            lab_specific_cols = []
            for lab_id in output[user_id]:
                lid = lab_id
                score = output[user_id][lab_id]['incdev_score']
                score_trail = output[user_id][lab_id]['incdev_score_trail']
                loc_trail = output[user_id][lab_id]['loc_trail']
                time_trail = output[user_id][lab_id]['time_trail']
                coding_trail = output[user_id][lab_id]['coding_trail']
                dc_trail = output[user_id][lab_id]['drastic_change_trail']
                lab_specific_cols += ([lid, score, score_trail, loc_trail, time_trail, coding_trail, dc_trail])
            row = [uid, name, email] + lab_specific_cols
            # writer.writerow([uid, name, email, lid, score, score_trail, loc_trail, time_trail])
            writer.writerow(row)

    print('Success! ' + output_file + ' has been generated.')