def allocate_study_time(subjects, total_hours):
    total_weight = sum(sub["weight"] for sub in subjects)
    schedule = []
    for sub in subjects:
        time = round((sub["weight"] / total_weight) * total_hours, 2)
        schedule.append((sub["name"], time))
    return schedule
