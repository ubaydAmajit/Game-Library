import random


def copyright_rand():
    team_members = ["Ubayd Abdul Majit", "Bilal Sarwar", "Madeline Whitmore"]
    random.shuffle(team_members)
    return f"&copy {team_members[0]}, {team_members[1]} and {team_members[2]} 2023"
