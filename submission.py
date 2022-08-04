""""
Data structure to represent student code submissions
"""

class Submission:
    def __init__(
        self, 
        student_id, 
        crid, 
        lab_id, 
        submission_id, 
        type, 
        code, 
        sub_time,
        score,
        anomaly_dict=None,
    ):
        self.student_id = student_id
        self.crid = crid
        self.lab_id = lab_id
        self.submission_id = submission_id
        self.type = type
        self.code = code
        self.sub_time = sub_time
        self.score = score
        self.anomaly_dict = anomaly_dict
