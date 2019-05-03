import json, os
setting_file = (os.getcwd() + '/Settings.txt')

test_json = {"pAlignment": "left", "pAlignment": "center", "pAlignment": "right"}
file = open(setting_file, 'w')
json_insert = json.dumps(test_json, indent=4)
print(json_insert)
with open(setting_file, 'w') as f:
    json.dump(test_json, f, ensure_ascii=False)
