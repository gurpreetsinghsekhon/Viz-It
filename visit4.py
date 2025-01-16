import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns

df = pd.read_csv("adult1.csv")
#dropping missing values
df.replace('?', pd.NA, inplace=True)
df = df.dropna()
# Declare global variables for selected attributes
selected_attribute1 = ''
selected_attribute2 = ''
selected_attribute3 = ''

# Declare global variable for second dropdown options
second_options = []

# Function to embed the plot in Tkinter window
def embed_plot_in_window(fig, root):
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Add the toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # Make sure to keep a reference to the canvas and toolbar
    root.canvas = canvas
    root.toolbar = toolbar

# Define plot functions
def plot_histogram(attribute):
    plt.figure(figsize=(8, 6))
    sns.histplot(df[attribute], kde=True)
    plt.title(f'Histogram for {attribute}')
    plt.xlabel(attribute)
    plt.ylabel('Frequency')
    embed_plot_in_window(plt.gcf(), root)

def plot_bar_chart(attribute1, attribute2):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=attribute1, hue=attribute2, data=df)
    plt.title(f'Bar Chart for: {attribute1} vs {attribute2}')
    plt.xlabel(attribute1)
    plt.ylabel('Count')
    embed_plot_in_window(plt.gcf(), root)

def plot_count_plot(attribute1, attribute2):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=attribute1, hue=attribute2, data=df)
    plt.title(f'Count Plot for: {attribute1} vs {attribute2}')
    plt.xlabel(attribute1)
    plt.ylabel('Count')
    embed_plot_in_window(plt.gcf(), root)

def plot_violin_plot(attribute1, attribute2):
    plt.figure(figsize=(12, 6))
    sns.violinplot(x=attribute1, y=attribute2, data=df)
    plt.title(f'Violin Plot for: {attribute1} vs {attribute2}')
    plt.xlabel(attribute1)
    plt.ylabel(attribute2)
    embed_plot_in_window(plt.gcf(), root)

def plot_stacked_bar_chart(attribute1, attribute2):
    plt.figure(figsize=(12, 6))
    stacked_data = df.groupby([attribute1, 'income']).size().unstack()
    stacked_data.plot(kind='bar', stacked=True)
    plt.title(f'Stacked Bar Chart for: {attribute1} vs {attribute2}')
    plt.xlabel(attribute1)
    plt.ylabel('Count')
    embed_plot_in_window(plt.gcf(), root)

def plot_pie_chart(attribute):
    plt.figure(figsize=(8, 8))
    df[attribute].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title(f'Pie Chart for: {attribute}')
    plt.ylabel('')
    embed_plot_in_window(plt.gcf(), root)

def plot_line_plot(attribute1, attribute2):
    plt.figure(figsize=(12, 6))
    plt.plot(df[attribute1], df[attribute2], marker='o', color='b')
    plt.title(f'Line Plot for {attribute1} vs {attribute2}')
    plt.xlabel(attribute1)
    plt.ylabel(attribute2)
    embed_plot_in_window(plt.gcf(), root)

def plot_correlation_heat_map():
    # Select only numeric columns
    numeric_columns = df.select_dtypes(include='number').columns.tolist()

    # Create a DataFrame with only numeric columns
    numeric_df = df[numeric_columns]

    # Create a new figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot the correlation heatmap on the specified axes
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)

    # Set the title
    ax.set_title('Correlation Heat Map')

    # Embed the plot in the Tkinter window
    embed_plot_in_window(fig, root)


def plot_facet_plot(attribute1, attribute2):
    plt.figure(figsize=(12, 8))
    sns.FacetGrid(df, col=attribute1, row=attribute2, height=4).map(plt.scatter, 'age', 'education.num')
    embed_plot_in_window(plt.gcf(), root)

# Function to update the second dropdown
def update_second_dropdown(*args):
    global selected_attribute1
    global second_options

    selected_attribute1 = attribute1_var.get()

    # Clear existing options
    attribute2_dropdown['values'] = []

    # First attribute determines the options for the second attribute
    if selected_attribute1 == 'Pie Chart':
        second_options = ['income', 'race', 'education', 'occupation']
    elif selected_attribute1 == 'Bar Chart- categorical vs categorical data':
        second_options = ['marital.status', 'occupation', 'relationship']
    elif selected_attribute1 == 'Bar Chart- categorical vs numerical data':
        second_options = ['race', 'education']
    elif selected_attribute1 == 'Bar Chart- numerical vs categorical data':
        second_options = ['age']
    elif selected_attribute1 == 'Count Plot':
        second_options = ['workclass', 'education', 'marital.status', 'occupation', 'relationship', 'race', 'sex', 'native.country']
    elif selected_attribute1 == 'Histogram':
        second_options = ['age', 'fnlwgt', 'education.num', 'capital.gain', 'capital.loss', 'hours.per.week']
    elif selected_attribute1 == 'Line Plot':
        second_options = ['age', 'education.num']
    elif selected_attribute1 == 'Correlation Heat Map':
        second_options = ['No attribute needed']
    elif selected_attribute1 == 'Violin Plot':
        second_options = ['age','hours.per.week']
    elif selected_attribute1 == 'Stacked Bar Chart':
        second_options = ['education', 'occupation', 'marital.status', 'race', 'relationship', 'sex']
    elif selected_attribute1 == 'Facet Plot':
        second_options = ['age', 'occupation', 'education.num', 'marital.status']
    else:
        second_options = ['default']  # Add more cases as needed

    attribute2_dropdown['values'] = second_options

# Function to update the third dropdown
def update_third_dropdown(*args):
    global selected_attribute1
    global selected_attribute2

    selected_attribute1 = attribute1_var.get()
    selected_attribute2 = attribute2_var.get()

    # Second attribute determines the options for the third attribute
    if selected_attribute1 == 'Pie Chart':
        third_options = ['No attribute needed']
    elif selected_attribute1 == 'Bar Chart- categorical vs categorical data':
        third_options = ['income']
    elif selected_attribute1 == 'Bar Chart- categorical vs numerical data':
        third_options = ['hours.per.week']
    elif selected_attribute1 == 'Bar Chart- numerical vs categorical data':
        third_options = ['marital.status']
    elif selected_attribute1 == 'Count Plot':
        third_options = ['income']
    elif selected_attribute1 == 'Histogram':
        third_options = ['No attribute needed']
    elif selected_attribute1 == 'Line Plot':
        third_options = ['hours.per.week']
    elif selected_attribute1 == 'Correlation Heat Map':
        third_options = ['No attribute needed']
    elif selected_attribute1 == 'Violin Plot':
        third_options = ['workclass', 'education', 'marital.status', 'occupation', 'relationship', 'race', 'sex', 'native.country']
    elif selected_attribute1 == 'Stacked Bar Chart':
        third_options = ['income']
    elif selected_attribute1 == 'Facet Plot':
        if selected_attribute2 in ['age', 'occupation']:
            third_options = ['hours.per.week']
        elif selected_attribute2 in ['education.num']:
            third_options = ['income']
        elif selected_attribute2 in ['marital.status']:
            third_options = ['relationship']
    else:
        third_options = ['default']  # Add more cases as needed

    third_dropdown['values'] = third_options

# Function to handle the plot button click
def plot():
    global selected_attribute1
    global selected_attribute2
    global selected_attribute3

    selected_attribute1 = attribute1_var.get()
    selected_attribute2 = attribute2_var.get()
    selected_attribute3 = attribute3_var.get()

    # Access selected attributes here
    print("Selected Attribute 1:", selected_attribute1)
    print("Selected Attribute 2:", selected_attribute2)
    print("Selected Attribute 3:", selected_attribute3)

    # Call the appropriate function based on the selected type of visual
    if selected_attribute1 == 'Histogram':
        plot_histogram(selected_attribute2)
    elif selected_attribute1 in ["Bar Chart- categorical vs categorical data", "Bar Chart- categorical vs numerical data", "Bar Chart- numerical vs categorical data"]:
        plot_bar_chart(selected_attribute2, selected_attribute3)
    elif selected_attribute1 == 'Count Plot':
        plot_count_plot(selected_attribute2, selected_attribute3)
    elif selected_attribute1 == 'Violin Plot':
        plot_violin_plot(selected_attribute2, selected_attribute3)
    elif selected_attribute1 == 'Stacked Bar Chart':
        plot_stacked_bar_chart(selected_attribute2, selected_attribute3)
    elif selected_attribute1 == 'Pie Chart':
        plot_pie_chart(selected_attribute2)
    elif selected_attribute1 == 'Line Plot':
        plot_line_plot(selected_attribute2, selected_attribute3)
    elif selected_attribute1 == 'Correlation Heat Map':
        plot_correlation_heat_map()
    elif selected_attribute1 == 'Facet Plot':
        plot_facet_plot(selected_attribute2, selected_attribute3)
    else:
        print("No valid selection")

# Create the main window
root = tk.Tk()
root.title("VizIt")

# First Dropdown Menu
attribute1_label = ttk.Label(root, text="Type of Visual")
attribute1_label.grid(row=0, column=0, padx=10, pady=10)

attribute1_var = tk.StringVar()
attribute1_dropdown = ttk.Combobox(root, textvariable=attribute1_var, values=["Select", "Histogram", "Bar Chart- categorical vs categorical data", "Bar Chart- categorical vs numerical data", "Bar Chart- numerical vs categorical data", "Count Plot", "Violin Plot", "Stacked Bar Chart", "Pie Chart", "Line Plot", "Correlation Heat Map", "Facet Plot"], width=40)
attribute1_dropdown.grid(row=0, column=1, padx=10, pady=10)
attribute1_dropdown.bind('<<ComboboxSelected>>', update_second_dropdown)

# Second Dropdown Menu
attribute2_label = ttk.Label(root, text="Attribute 1:")
attribute2_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

attribute2_var = tk.StringVar()
attribute2_dropdown = ttk.Combobox(root, textvariable=attribute2_var, values=[])
attribute2_dropdown.grid(row=1, column=1, padx=10, pady=10)
attribute2_dropdown.bind('<<ComboboxSelected>>', update_third_dropdown)

# Third Dropdown Menu
attribute3_label = ttk.Label(root, text="Attribute 2:")
attribute3_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

attribute3_var = tk.StringVar()
third_dropdown = ttk.Combobox(root, textvariable=attribute3_var, values=[])
third_dropdown.grid(row=2, column=1, padx=10, pady=10)

plot_button = tk.Button(root, text="Plot", command=plot)
plot_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
