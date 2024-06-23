import json
import os
def organize_by_mood():
    print(os.getcwd())
    with open('../flask_server/userdata/user_data.json', 'r+') as f:
            user_data = json.load(f)

    temp_dict = {}
    for track in user_data:
        mood = user_data[track]['mood']
        id = user_data[track]['id']
        if mood not in temp_dict:
            temp_dict[mood] = {'trackname': track, 'id': id}

        temp_dict[mood].append(track)
    new_data = f.write(json.dumps(temp_dict))
    return new_data
        

organize_by_mood()