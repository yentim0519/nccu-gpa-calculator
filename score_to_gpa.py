def score_to_gpa_4point3(score):
    score_interval = [90, 85, 80, 77, 73, 70, 67, 63, 60, 50, 0]

    if score >= score_interval[0]:
        return 4.3
    
    elif score >= score_interval[1] and score < score_interval[0]:
        return 4.0

    elif score >= score_interval[2] and score < score_interval[1]:
        return 3.7

    elif score >= score_interval[3] and score < score_interval[2]:
        return 3.3

    elif score >= score_interval[4] and score < score_interval[3]:
        return 3.0 

    elif score >= score_interval[5] and score < score_interval[4]:
        return 2.7

    elif score >= score_interval[6] and score < score_interval[5]:
        return 2.3

    elif score >= score_interval[7] and score < score_interval[6]:
        return 2.0

    elif score >= score_interval[8] and score < score_interval[7]:
        return 1.7

    elif score >= score_interval[9] and score < score_interval[8]:
        return 1.0

    elif score >= score_interval[10] and score < score_interval[9]:
        return 0.0 


def score_to_gpa_4(score):
    score_interval = [80, 70, 60, 50, 0]

    if score >= score_interval[0]:
        return 4.0
    
    elif score >= score_interval[1] and score < score_interval[0]:
        return 3.0

    elif score >= score_interval[2] and score < score_interval[1]:
        return 2.0

    elif score >= score_interval[3] and score < score_interval[2]:
        return 1.0

    elif score >= score_interval[4] and score < score_interval[3]:
        return 0.0 
