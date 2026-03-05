def calculate_scores(answers):

    emotional = sum(answers[0:4]) / 20 * 100
    communication = sum(answers[4:8]) / 20 * 100
    trust = sum(answers[8:12]) / 20 * 100
    conflict = sum(answers[12:16]) / 20 * 100
    satisfaction = sum(answers[16:20]) / 20 * 100

    overall = (
        emotional +
        communication +
        trust +
        conflict +
        satisfaction
    ) / 5

    return {
        "emotional": round(emotional,2),
        "communication": round(communication,2),
        "trust": round(trust,2),
        "conflict": round(conflict,2),
        "satisfaction": round(satisfaction,2),
        "overall": round(overall,2)
    }
