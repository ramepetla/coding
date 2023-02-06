# Reading a Lists from a Text File

inputf = open("08.input_values.txt", "r")

data = inputf.read()

lists = data.split("\n")


missing_ramesh_groups = []
missinng_varshini_groups = []

for list in lists:
    if 'ramesh' in list:
        ramesh_groups = list.split(",")
    elif 'varshini' in list:
        varshini_groups = list.split(",")
    elif 'bhawna' in list:
        bhawna_groups = list.split(",")

def compare_lists(master, slave):
    missing_groups = []
    for item in master:
        if item not in slave:
            missing_groups.append(item)
    print("\nMissing Groups for ", slave[0], '\n')
    for item in missing_groups:
        print(item)


compare_lists(bhawna_groups, ramesh_groups)
compare_lists(bhawna_groups, varshini_groups)
