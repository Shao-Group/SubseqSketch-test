from matplotlib import pyplot as plt
import numpy as np
import sys

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Usage: plotRFDist.py <input-file> <-r>\nfile should have the format that each method name follows by the same number of lines, each line has three fields: #gen RF/Max_RF norm_RF")
    exit(1)

up_side_down = True if len(sys.argv) == 3 and sys.argv[2] == '-r' else False

group = []
group_idx = 0
data = {}
cur = None
with open(sys.argv[1], 'r') as f:
    for l in f:
        x = l.split()
        if len(x) == 1: #new method
            cur = x[0]
            data[cur] = []
            if group_idx != len(group):
                print("Error: not all methods have the same number of results")
                exit(1)
            group_idx = 0
        else:
            if up_side_down:
                data[cur].append(round(float(x[1]),1))
            else:
                data[cur].append(round(float(x[2]),2))
            if len(group) == group_idx:
                group.append(int(x[0]))
            elif group[group_idx] != int(x[0]):
                print("Error: the #gen for each method do not align")
                exit(1)
            group_idx += 1

plt.figure(figsize=(16,4.5))
plt.rcParams['font.size'] = 12

#bar plot
x = np.arange(len(group))
width = 1/(len(data.keys())+1)
multiplier = 0

for method, values in data.items():
    offset = width * multiplier
    # if up_side_down:
    #     rects = plt.bar(x + offset, [-v for v in values], width, label=method.upper())
    #     plt.bar_label(rects, labels=values, padding=3, fontsize=7)
    # else:
    #     rects = plt.bar(x + offset, values, width, label=method.upper())
    #     plt.bar_label(rects, padding=3, fontsize=7)
    rects = plt.bar(x + offset, values, width, label=method)#.upper())
    plt.bar_label(rects, padding=3, fontsize=7)
    multiplier += 1

plt.xticks(x+.5-width, group)

#line plot
'''
for method, values in data.items():
    plt.plot(group, values, label=method)

plt.xticks(group, group)
'''
if up_side_down:
    plt.ylabel('Time in seconds')
    plt.legend(ncols=len(data.keys()), bbox_to_anchor=(0.525,1.07), framealpha=1)
    plt.xlabel('generation')
    plt.yscale('log')
    # locs, labels = plt.yticks()
    # new_labels = [tick.get_text() for tick in labels]
    # for i in range(len(new_labels)):
    #     if not new_labels[i][0].isdigit():
    #         new_labels[i] = new_labels[i][1:]
    # plt.yticks(locs, new_labels)
    # #plt.gca().xaxis.tick_top()
    # plt.xticks([])
else:
    plt.ylabel('nRF distance from the ground truth tree')
    plt.legend(ncols=len(data.keys()), bbox_to_anchor=(0.525,1.07), framealpha=1)
    plt.xlabel('generation')

# plt.ylim(0,1)
plt.savefig(f'{sys.argv[1]}.pdf', bbox_inches='tight')
plt.close()

