import json

uni_dict = {}

with open("covid_policies.txt", "r") as f:
    uni = None
    for line in f.readlines():
        line = line.strip('\n')

        if ":" in line and "Source" not in line:
            uni = line.strip(':')
            uni_dict[uni] = []

        elif uni and line != '' and "Source" not in line:
            uni_dict[uni].append(line)


with open('covid_policies.json', 'w') as f:
    f.write(json.dumps(uni_dict, sort_keys=False, indent=4))
