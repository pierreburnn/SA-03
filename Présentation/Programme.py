import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import webbrowser
import os
import markdown







def analyze_file(file_content):

    issues = []
    
    
    ### SEARCH FRAMES ONE BY ONE ###
    dns_frame = re.finditer(r".*NXDomain.*", file_content, re.MULTILINE)
    syn_frames = re.finditer(r".*SYN.*", file_content, re.MULTILINE)
    repeated_frames = re.finditer(r".*5858.*", file_content, re.MULTILINE)

    # Store each frame
    for frame in dns_frame:
        issues.append(["DNS error", "DNS problem", frame.group(0)])

    for frame in syn_frames:
        issues.append(["SYN Flag", "Suspicious SYN flag", frame.group(0)])

    for frame in repeated_frames:
        issues.append(["Repetition", "Repeated data", frame.group(0)])

    return issues






### GENERATE AN EXCEL TABLE ###
def generate_excel(issues):

    """
    Save issues into a CSV file, allowing 
    the user to select the location via a dialog box.
    """
    path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                        filetypes=[("CSV files", "*.csv")])
    
    if path:

        try:

            df = pd.DataFrame(issues, columns=["Type", "Description", "Frame"])

            df.to_csv(path, index=False, sep=';', encoding='utf-8-sig')

            messagebox.showinfo("Success", "Results saved into a CSV file.")

        except Exception as e:
            messagebox.showerror("Error", f"Unable to save the file: {e}")







### SAVE RESULTS INTO AN HTML FILE ###
def save_as_HTML(issues):

    """
    Save results into an HTML file, 
    but using the Markdown library for table generation.
    """
    


    markdown_content = "# TCP Analysis Results\n\n"
    markdown_content += "| Type | Description | Frame |\n"
    markdown_content += "| ---  | ---         | ---   |\n"



    # Add each issue to the Markdown table
    for issue in issues:
        markdown_content += f"| {issue[0]} | {issue[1]} | {issue[2]} |\n"




    # Convert the Markdown text into HTML
    # Enable the 'tables' extension for better table handling
    html_converted_content = markdown.markdown(markdown_content, extensions=['tables'])




    # Encapsulate this HTML content in a skeleton 
    final_html_content = f"""
    <html>
    <head>
        <title>TCP Analysis</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            h1 {{ color: #4CAF50; }}
        </style>
    </head>
    <body>
        {html_converted_content}
    </body>
    </html>
    """




    ### SAVE THE HTML FILE ON THE DESKTOP ###
    path = os.path.join(os.path.expanduser("~"), "Desktop", "tcp_analysis.html")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(final_html_content)


    # Open the HTML file in the web browser
    webbrowser.open('file://' + path)





def load_file():

    path = filedialog.askopenfilename()
    if path:

        try:

            with open(path, 'r') as f:
                content = f.read()
                results = analyze_file(content)
                display_results(results)

        except Exception as e:
            print("Error:", e)




def display_results(issues):

    results_window = tk.Toplevel()
    results_window.title("Results")

    def filter_issues(event):

        selected_type = filter_var.get()
        for row in tree.get_children():
            tree.delete(row)



        for issue in issues:

            if selected_type == "All" or issue[0] == selected_type:
                tree.insert("", tk.END, values=issue)





    # Add filters
    filter_frame = ttk.Frame(results_window)

    filter_frame.pack(fill=tk.X, padx=10, pady=5)



    ttk.Label(filter_frame, text="Filter by issue type:").pack(side=tk.LEFT, padx=5)
    filter_var = tk.StringVar(value="All")

    filter_menu = ttk.Combobox(filter_frame, textvariable=filter_var, state="readonly")
    filter_menu['values'] = ["All"] + list(set(issue[0] for issue in issues))
    filter_menu.pack(side=tk.LEFT, padx=5)
    filter_menu.bind("<<ComboboxSelected>>", filter_issues)




    # List of results with modified column
    tree = ttk.Treeview(results_window)
    tree["columns"] = ("Type", "Description", "Frame")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Type", anchor=tk.W, width=120)
    tree.column("Description", anchor=tk.W, width=200)
    tree.column("Frame", anchor=tk.W, width=400)  # The column is wider for frames


    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Type", text="Type", anchor=tk.W)
    tree.heading("Description", text="Description", anchor=tk.W)
    tree.heading("Frame", text="Suspicious Frame", anchor=tk.W)
    tree.pack(fill=tk.BOTH, expand=True)



    for issue in issues:
        tree.insert("", tk.END, values=issue)




    # Save buttons
    button_frame = ttk.Frame(results_window)
    button_frame.pack(pady=10)
    
    save_csv_button = tk.Button(button_frame, text="Save as CSV", 
                                command=lambda: generate_excel(issues))
    
    save_csv_button.pack(side=tk.LEFT, padx=5)
    
    save_html_button = tk.Button(button_frame, text="Open in Browser", 
                                 command=lambda: save_as_HTML(issues))
    
    save_html_button.pack(side=tk.LEFT, padx=5)





# Create the main window
root = tk.Tk()
root.title("TCP Analyzer")



btn = tk.Button(root, text="Load a File", command=load_file)
btn.pack(pady=20)



root.mainloop()
