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







### ANALYZE TCP DUMP FILE ###
def analyze_file(file_content):
    
    issues = []
    packet_counts = {
        "DNS NXDomain": 0,
        "Suspicious SYN": 0,
        "Repeated Payload": 0,
        "Total Packets": 0
    }




    ### COUNT TOTAL PACKETS ###
    all_packets_pattern = re.compile(r"^\d+", re.MULTILINE)
    all_packets = all_packets_pattern.findall(file_content)
    packet_counts["Total Packets"] = len(all_packets)




    ### SEARCH SUSPICIOUS PACKETS ###
    dns_frames = list(set(re.findall(r".*NXDomain.*", file_content, re.MULTILINE)))
    syn_frames = list(set(re.findall(r"IP \S+ > \S+\.http: Flags \[S\].*?", file_content)))
    repeated_frames = list(set(re.findall(r".*5858 5858.*", file_content)))




    ### UPDATE PACKET COUNTS ###
    packet_counts["DNS NXDomain"] = len(dns_frames)
    packet_counts["Suspicious SYN"] = len(syn_frames)
    packet_counts["Repeated Payload"] = len(repeated_frames)





    ### STORE FRAME DETAILS ###
    for frame in dns_frames:
        issues.append(["DNS Error", "DNS Resolution Failed", frame])

    for frame in syn_frames:
        issues.append(["SYN Flag", "Suspicious SYN Connection", frame])
        
    for frame in repeated_frames:
        issues.append(["Repetition", "Repeated Payload Data", frame])

    return issues, packet_counts




### GENERATE EXCEL REPORT ###
def generate_excel(issues):


    path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                        filetypes=[("CSV files", "*.csv")])
    

    if path:

        try:

            df = pd.DataFrame(issues, columns=["Type", "Description", "Frame"])
            df.to_csv(path, index=False, sep=';', encoding='utf-8-sig')
            messagebox.showinfo("Success", "Results saved into a CSV file.")


        except Exception as e:
            messagebox.showerror("Error", f"Unable to save the file: {e}")




### GENERATE HTML REPORT ###
def save_as_HTML(issues):



    markdown_content = "# TCP Analysis Results\n\n"
    markdown_content += "| Type | Description | Frame |\n"
    markdown_content += "| ---  | ---         | ---   |\n"



    for issue in issues:

        markdown_content += f"| {issue[0]} | {issue[1]} | {issue[2]} |\n"

    html_converted_content = markdown.markdown(markdown_content, extensions=['tables'])



    counts = {"DNS NXDomain": 0, "Suspicious SYN": 0, "Repeated Payload": 0}


    for i in issues:

        if i[0] == "DNS Error":
            counts["DNS NXDomain"] += 1

        elif i[0] == "SYN Flag":

            counts["Suspicious SYN"] += 1


        elif i[0] == "Repetition":

            counts["Repeated Payload"] += 1

    counts["Total Packets"] = sum(counts.values())





    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts.keys(), counts.values(), color='skyblue')
    ax.set_title("Packet Distribution")
    ax.set_xlabel("Issue Types")
    ax.set_ylabel("Number of Packets")
    plt.xticks(rotation=0)




    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    bar_chart_filename = "bar_chart.png"
    bar_chart_full_path = os.path.join(desktop_path, bar_chart_filename)
    fig.savefig(bar_chart_full_path)
    plt.close(fig)



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
        <h2>Bar Chart (Packet Distribution)</h2>
        <img src="{bar_chart_filename}" alt="Bar Chart" width="400" />

    </body>
    </html>
    """


    path = os.path.join(os.path.expanduser("~"), "Desktop", "tcp_analysis.html")

    with open(path, 'w', encoding='utf-8') as f:

        f.write(final_html_content)


    webbrowser.open('file://' + path)





### LOAD AND ANALYZE FILE ###
def load_file():

    path = filedialog.askopenfilename()

    if path:

        try:
            with open(path, 'r') as f:
                content = f.read()

                results, _ = analyze_file(content)
                display_results(results, content)


        except Exception as e:

            print("Error:", e)





### DISPLAY ANALYSIS RESULTS ###
def display_results(issues, file_content):

    results_window = tk.Toplevel()
    results_window.title("Analysis Results")



    def filter_issues(event):

        selected_type = filter_var.get()

        for row in tree.get_children():
            tree.delete(row)



        for issue in issues:

            if selected_type == "All" or issue[0] == selected_type:
                tree.insert("", tk.END, values=issue)



    filter_frame = ttk.Frame(results_window)
    filter_frame.pack(fill=tk.X, padx=10, pady=5)


    ttk.Label(filter_frame, text="Filter by issue type:").pack(side=tk.LEFT, padx=5)
    filter_var = tk.StringVar(value="All")


    filter_menu = ttk.Combobox(filter_frame, textvariable=filter_var, state="readonly")
    filter_menu['values'] = ["All"] + list(set(issue[0] for issue in issues))


    filter_menu.pack(side=tk.LEFT, padx=5)
    filter_menu.bind("<<ComboboxSelected>>", filter_issues)




    tree = ttk.Treeview(results_window)
    tree["columns"] = ("Type", "Description", "Frame")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Type", anchor=tk.W, width=120)
    tree.column("Description", anchor=tk.W, width=200)
    tree.column("Frame", anchor=tk.W, width=400)


    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Type", text="Type", anchor=tk.W)
    tree.heading("Description", text="Description", anchor=tk.W)
    tree.heading("Frame", text="Suspicious Frame", anchor=tk.W)
    tree.pack(fill=tk.BOTH, expand=True)





    for issue in issues:

        tree.insert("", tk.END, values=issue)



    button_frame = ttk.Frame(results_window)
    button_frame.pack(pady=10)


    save_csv_button = tk.Button(button_frame, text="Save as CSV", 
                                command=lambda: generate_excel(issues))
    
    save_csv_button.pack(side=tk.LEFT, padx=5)


    save_html_button = tk.Button(button_frame, text="Open in Browser", 
                                 command=lambda: save_as_HTML(issues))
    
    save_html_button.pack(side=tk.LEFT, padx=5)



    _, counts = analyze_file(file_content)  



    fig = plt.Figure(figsize=(14, 4), dpi=100)
    ax = fig.add_subplot(111)


    ax.bar(counts.keys(), counts.values(), color=['purple', 'red', 'blue', 'green'])
    ax.set_title("Packet Distribution")
    ax.set_xlabel("Issue Types")
    ax.set_ylabel("Number of Packets")
    ax.tick_params(axis='x', rotation=0)



    ### Added value labels on bars ###
    for i, value in enumerate(counts.values()):

        ax.text(i, value + 0.5, str(value), ha='center', va='bottom')



    canvas = FigureCanvasTkAgg(fig, master=results_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)







### MAIN APPLICATION ###
root = tk.Tk()
root.title("TCP Packet Analyzer")



btn = tk.Button(root, text="Load a File", command=load_file)
btn.pack(pady=20)




root.mainloop()