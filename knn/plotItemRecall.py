import pandas as pd
import matplotlib.pyplot as plt
import sys

if len(sys.argv) != 3:
    print('Usage: plotItemRecall.py result-file T\nIn the input file, the first column is the number of items, followed by recall of each method. The first row is the headers.')
    sys.exit(1)

df = pd.read_csv(sys.argv[1], sep='\t')

x = df.iloc[:, 0]

# Create the plot
# plt.figure(figsize=(10, 6))

markers = ['o', 'x', '^', 's', '*']
for i in range(1, len(df.columns)):
    plt.plot(x, df.iloc[:, i], label=df.columns[i], marker=markers[(i-1)%len(markers)])
    
# Plot the data
#plt.plot(x, y1, label='y1', marker='o', linestyle='-', color='b')

# Set x-axis to logarithmic scale
plt.xscale('log')

# Add labels and title
plt.xlabel(f'{df.columns[0]} (log scale)')
plt.ylabel('recall')

# Add a legend
plt.legend(title=f'Top-{sys.argv[2]}', loc='lower right')

# Show the plot
plt.tight_layout()
plt.savefig(f'{sys.argv[1]}.pdf')
