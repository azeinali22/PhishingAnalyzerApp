import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from pathlib import Path
import webbrowser
import os
from datetime import datetime
import threading
import html
import json


class PhishingAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Infosec IQ - Regional Phishing Report Analyzer")
        self.root.geometry("820x620")
        self.root.minsize(820, 620)
        self.root.configure(bg="#f0f0f0")

        self.folder_path = None
        self.processing = False
        self.dashboard_path = None
        self.analysis_data = None
        self.hospital_vars = {}

        title_label = tk.Label(
            root,
            text="Infosec IQ Phishing Report Analyzer",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
        )
        title_label.pack(pady=12)

        subtitle_label = tk.Label(
            root,
            text="Select the main folder. Each subfolder is treated as one hospital.",
            font=("Helvetica", 10),
            bg="#f0f0f0",
            fg="#7f8c8d",
        )
        subtitle_label.pack()

        folder_frame = tk.LabelFrame(root, text="1. Select Main Reports Folder", padx=15, pady=12, bg="#f0f0f0")
        folder_frame.pack(padx=20, pady=10, fill="x")

        btn_frame = tk.Frame(folder_frame, bg="#f0f0f0")
        btn_frame.pack(fill="x")

        browse_btn = tk.Button(
            btn_frame,
            text="Select Reports Folder",
            command=self.browse_folder,
            bg="#3498db",
            fg="white",
            padx=15,
            relief="flat",
            cursor="hand2",
        )
        browse_btn.pack(side="left", padx=(0, 10))

        help_btn = tk.Button(
            btn_frame,
            text="HELP",
            command=self.show_help,
            bg="#8e44ad",
            fg="white",
            padx=15,
            relief="flat",
            cursor="hand2",
        )
        help_btn.pack(side="left", padx=(0, 10))

        clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_folder,
            bg="#95a5a6",
            fg="white",
            padx=15,
            relief="flat",
            cursor="hand2",
        )
        clear_btn.pack(side="left")

        self.folder_label = tk.Label(
            folder_frame,
            text="No folder selected",
            font=("Helvetica", 9),
            bg="#f0f0f0",
            fg="#7f8c8d",
            justify="left",
            anchor="w",
        )
        self.folder_label.pack(fill="x", pady=(10, 0))

        hospital_frame = tk.LabelFrame(root, text="2. Hospitals to Include", padx=15, pady=10, bg="#f0f0f0")
        hospital_frame.pack(padx=20, pady=8, fill="both", expand=True)

        hospital_button_frame = tk.Frame(hospital_frame, bg="#f0f0f0")
        hospital_button_frame.pack(fill="x", pady=(0, 5))

        select_all_btn = tk.Button(
            hospital_button_frame,
            text="Select All",
            command=self.select_all_hospitals,
            bg="#27ae60",
            fg="white",
            padx=12,
            relief="flat",
            cursor="hand2",
        )
        select_all_btn.pack(side="left", padx=(0, 8))

        clear_all_btn = tk.Button(
            hospital_button_frame,
            text="Clear All",
            command=self.clear_all_hospitals,
            bg="#95a5a6",
            fg="white",
            padx=12,
            relief="flat",
            cursor="hand2",
        )
        clear_all_btn.pack(side="left")

        self.hospital_canvas = tk.Canvas(hospital_frame, height=170, bg="white", highlightthickness=1, highlightbackground="#dcdcdc")
        self.hospital_scrollbar = ttk.Scrollbar(hospital_frame, orient="vertical", command=self.hospital_canvas.yview)
        self.hospital_checkbox_frame = tk.Frame(self.hospital_canvas, bg="white")

        self.hospital_checkbox_frame.bind(
            "<Configure>",
            lambda e: self.hospital_canvas.configure(scrollregion=self.hospital_canvas.bbox("all")),
        )

        self.hospital_canvas.create_window((0, 0), window=self.hospital_checkbox_frame, anchor="nw")
        self.hospital_canvas.configure(yscrollcommand=self.hospital_scrollbar.set)
        self.hospital_canvas.pack(side="left", fill="both", expand=True)
        self.hospital_scrollbar.pack(side="right", fill="y")

        self.hospital_hint = tk.Label(
            hospital_frame,
            text="Select a folder to load hospital checkboxes.",
            font=("Helvetica", 9),
            bg="#f0f0f0",
            fg="#7f8c8d",
            anchor="w",
        )
        self.hospital_hint.pack(fill="x", pady=(5, 0))

        process_frame = tk.LabelFrame(root, text="3. Generate Report", padx=15, pady=10, bg="#f0f0f0")
        process_frame.pack(padx=20, pady=8, fill="x")

        self.process_btn = tk.Button(
            process_frame,
            text="Generate Dashboard",
            command=self.process_folder,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 11, "bold"),
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2",
        )
        self.process_btn.pack(pady=5)




        self.status_label = tk.Label(
            process_frame,
            text="Ready to process folder",
            font=("Helvetica", 9),
            bg="#f0f0f0",
            fg="#27ae60",
        )
        self.status_label.pack()

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select the main folder that contains hospital folders")
        if folder:
            self.folder_path = folder
            self.load_hospital_checkboxes()
            self.status_label.config(text="Folder selected. Choose hospitals, then generate dashboard.", fg="#27ae60")

    def clear_folder(self):
        self.folder_path = None
        self.dashboard_path = None
        self.analysis_data = None
        self.hospital_vars = {}
        self.folder_label.config(text="No folder selected")
        self.clear_hospital_checkbox_area()
        self.hospital_hint.config(text="Select a folder to load hospital checkboxes.")
        self.status_label.config(text="Ready to process folder", fg="#27ae60")



    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - How to Use")
        help_window.geometry("720x560")
        help_window.minsize(650, 500)
        help_window.configure(bg="#ffffff")
        help_window.transient(self.root)
        help_window.grab_set()

        header = tk.Frame(help_window, bg="#2c3e50", padx=18, pady=14)
        header.pack(fill="x")

        tk.Label(
            header,
            text="How to Organize and Open Reports",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Use one main folder. Each hospital must have its own subfolder.",
            font=("Helvetica", 10),
            bg="#2c3e50",
            fg="#ecf0f1",
        ).pack(anchor="w", pady=(4, 0))

        body_frame = tk.Frame(help_window, bg="#ffffff")
        body_frame.pack(fill="both", expand=True, padx=18, pady=14)

        help_text = """STEP 1 - Create one main folder

Example:
InfosecIQ Reports

STEP 2 - Create one folder for each hospital inside the main folder

Example:
InfosecIQ Reports
│
├── TBRHSC & SJCG
├── Riverside
├── Dryden
├── Kenora
└── Sioux Lookout

STEP 3 - Put each hospital's CSV files inside its own hospital folder

Example:
InfosecIQ Reports
│
├── TBRHSC & SJCG
│   ├── Monthly Phishing.csv
│   ├── Catch of the Week.csv
│   └── Executive Campaign.csv
│
├── Riverside
│   ├── Monthly Phishing.csv
│   └── June Campaign.csv
│
└── Dryden
    ├── May Campaign.csv
    └── June Campaign.csv

HOW TO USE THE PROGRAM

1. Click "Select Reports Folder".
2. Choose the MAIN folder, for example "InfosecIQ Reports".
3. Review the hospital checkboxes.
4. Uncheck any hospital you do not want included.
5. Click "Generate Dashboard".
6. If a hospital has no reported emails, the program will ask if you want to exclude it.
7. The dashboard opens automatically in your browser.

IMPORTANT

Do not select an individual hospital folder.
Select the main folder that contains all hospital folders.
"""

        text_box = tk.Text(
            body_frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#f8f9fa",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=14,
            pady=14,
        )
        text_box.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(body_frame, orient="vertical", command=text_box.yview)
        scrollbar.pack(side="right", fill="y")
        text_box.configure(yscrollcommand=scrollbar.set)

        text_box.insert("1.0", help_text)
        text_box.config(state="disabled")

        footer = tk.Frame(help_window, bg="#ffffff", padx=18, pady=12)
        footer.pack(fill="x")

        close_btn = tk.Button(
            footer,
            text="Close",
            command=help_window.destroy,
            bg="#3498db",
            fg="white",
            padx=20,
            pady=6,
            relief="flat",
            cursor="hand2",
        )
        close_btn.pack(side="right")

    def clear_hospital_checkbox_area(self):
        for widget in self.hospital_checkbox_frame.winfo_children():
            widget.destroy()
        self.hospital_canvas.configure(scrollregion=self.hospital_canvas.bbox("all"))

    def load_hospital_checkboxes(self):
        self.clear_hospital_checkbox_area()
        self.hospital_vars = {}

        root_folder = Path(self.folder_path)
        hospital_folders = sorted([p for p in root_folder.iterdir() if p.is_dir()], key=lambda p: p.name.lower())
        csv_count = len(list(root_folder.rglob("*.csv")))

        self.folder_label.config(
            text=f"Selected folder: {root_folder}\n"
                 f"Hospital folders found: {len(hospital_folders)}\n"
                 f"CSV files found: {csv_count}"
        )

        if not hospital_folders:
            self.hospital_hint.config(text="No hospital folders found.")
            return

        for hospital_folder in hospital_folders:
            csv_files = list(hospital_folder.glob("*.csv"))
            var = tk.BooleanVar(value=bool(csv_files))
            self.hospital_vars[hospital_folder.name] = var

            label_text = f"{hospital_folder.name} ({len(csv_files)} CSV file{'s' if len(csv_files) != 1 else ''})"
            checkbox = tk.Checkbutton(
                self.hospital_checkbox_frame,
                text=label_text,
                variable=var,
                bg="white",
                anchor="w",
                justify="left",
                font=("Helvetica", 9),
            )
            checkbox.pack(fill="x", anchor="w", padx=8, pady=2)

        self.hospital_hint.config(text="Uncheck any hospital you do not want included in the statistics.")
        self.hospital_canvas.configure(scrollregion=self.hospital_canvas.bbox("all"))

    def select_all_hospitals(self):
        for var in self.hospital_vars.values():
            var.set(True)

    def clear_all_hospitals(self):
        for var in self.hospital_vars.values():
            var.set(False)

    def selected_hospitals(self):
        return [hospital for hospital, var in self.hospital_vars.items() if var.get()]

    def process_folder(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select the main reports folder first.")
            return

        selected = self.selected_hospitals()
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one hospital to include.")
            return

        self.processing = True
        self.process_btn.config(
            text="Generating Dashboard...",
            state="disabled",
            bg="#95a5a6"
        )

        self.status_label.config(text="Processing...", fg="#f39c12")

        thread = threading.Thread(target=self._process_folder_thread, args=(selected,))
        thread.daemon = True
        thread.start()

    def _process_folder_thread(self, selected_hospitals):
        try:
            result = self._collect_data(selected_hospitals)
            self.root.after(0, lambda r=result: self._confirm_exclusions_and_generate(r))
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("Error", f"Processing failed:\n{msg}"))
        finally:
            self.processing = False
            self.root.after(0, self._cleanup_processing)

    def _collect_data(self, selected_hospitals):
        root_folder = Path(self.folder_path)
        selected_set = set(selected_hospitals)
        hospital_folders = sorted(
            [p for p in root_folder.iterdir() if p.is_dir() and p.name in selected_set],
            key=lambda p: p.name.lower(),
        )

        if not hospital_folders:
            raise ValueError("No selected hospital folders found.")

        hospital_summaries = []
        campaign_summaries = []
        combined_frames = []
        skipped_files = []

        for hospital_folder in hospital_folders:
            hospital_name = hospital_folder.name
            csv_files = sorted(hospital_folder.glob("*.csv"))

            if not csv_files:
                skipped_files.append(f"{hospital_name}: No CSV files found")
                continue

            hospital_frames = []
            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    campaign_name = self._clean_campaign_name(csv_file.stem)
                    campaign_data, delivered_df = self._analyze_dataframe(df, hospital_name, campaign_name)
                    campaign_summaries.append(campaign_data)
                    hospital_frames.append(delivered_df)
                    combined_frames.append(delivered_df)
                except Exception as e:
                    skipped_files.append(f"{hospital_name} / {csv_file.name}: {e}")

            if hospital_frames:
                hospital_df = pd.concat(hospital_frames, ignore_index=True)
                hospital_reported_df = hospital_df[hospital_df["Phish Status"] == "Reported Attack"]
                delivered = len(hospital_df)
                reported = len(hospital_reported_df)
                report_rate = (reported / delivered * 100) if delivered > 0 else 0
                warning = ""
                if delivered > 0 and reported == 0:
                    warning = "Make sure Phish Notify is installed as there is no reported email."

                hospital_summaries.append({
                    "hospital": hospital_name,
                    "campaigns": len(hospital_frames),
                    "delivered": delivered,
                    "reported": reported,
                    "report_rate": report_rate,
                    "warning": warning,
                })

        if not combined_frames:
            raise ValueError("No valid CSV files found inside the selected hospital folders.")

        combined_delivered_df = pd.concat(combined_frames, ignore_index=True)

        return {
            "root_folder": str(root_folder),
            "hospital_summaries": hospital_summaries,
            "campaign_summaries": campaign_summaries,
            "combined_delivered_df": combined_delivered_df,
            "skipped_files": skipped_files,
        }

    def _confirm_exclusions_and_generate(self, result):
        zero_reported_hospitals = [
            h["hospital"]
            for h in result["hospital_summaries"]
            if h["delivered"] > 0 and h["reported"] == 0
        ]

        excluded_zero_reported = []

        if zero_reported_hospitals:
            hospital_list = "\n".join(zero_reported_hospitals)
            exclude = messagebox.askyesno(
                "No Reported Emails",
                "These hospitals have no reported emails:\n\n"
                f"{hospital_list}\n\n"
                "This may mean the Phish Notify button is not installed or not working.\n\n"
                "Do you want to exclude these hospitals from the final statistics?"
            )

            if exclude:
                excluded_zero_reported = zero_reported_hospitals
                exclude_set = set(zero_reported_hospitals)
                result["hospital_summaries"] = [h for h in result["hospital_summaries"] if h["hospital"] not in exclude_set]
                result["campaign_summaries"] = [c for c in result["campaign_summaries"] if c["hospital"] not in exclude_set]
                result["combined_delivered_df"] = result["combined_delivered_df"][
                    ~result["combined_delivered_df"]["Hospital"].isin(exclude_set)
                ].copy()

                if result["combined_delivered_df"].empty:
                    messagebox.showerror(
                        "Error",
                        "All selected hospitals were excluded, so there is no data left for the dashboard."
                    )
                    return

                for hospital in excluded_zero_reported:
                    if hospital in self.hospital_vars:
                        self.hospital_vars[hospital].set(False)

        self.analysis_data = self._build_analysis_data(result, excluded_zero_reported)
        self.dashboard_path = self._generate_dashboard(self.analysis_data)
        self._update_ui_after_processing(excluded_zero_reported)
        self.open_dashboard()

    def _build_analysis_data(self, result, excluded_zero_reported=None):
        excluded_zero_reported = excluded_zero_reported or []
        combined_delivered_df = result["combined_delivered_df"]
        combined_reported_df = combined_delivered_df[combined_delivered_df["Phish Status"] == "Reported Attack"]

        total_delivered = len(combined_delivered_df)
        total_reported = len(combined_reported_df)
        report_rate = (total_reported / total_delivered * 100) if total_delivered > 0 else 0

        status_counts = combined_delivered_df["Phish Status"].value_counts().to_dict()
        status_counts.pop("Phished and Entered Data", None)
        status_counts.pop("Fast Click", None)

        return {
            "root_folder": result["root_folder"],
            "hospitals": sorted(result["hospital_summaries"], key=lambda x: x["hospital"].lower()),
            "campaigns": sorted(result["campaign_summaries"], key=lambda x: (x["hospital"].lower(), x["campaign"].lower())),
            "skipped_files": result["skipped_files"],
            "excluded_zero_reported": excluded_zero_reported,
            "total_delivered": total_delivered,
            "total_reported": total_reported,
            "report_rate": report_rate,
            "by_template": self._analyze_by_template(combined_delivered_df, combined_reported_df),
            "by_user": self._analyze_by_user(combined_delivered_df, combined_reported_df),
            "phish_status_breakdown": status_counts,
        }

    def _clean_campaign_name(self, campaign_name):
        remove_parts = [
            " - Attempts List 2026-06-29",
            " - Attempts List",
            " Attempts List",
        ]
        cleaned = campaign_name
        for part in remove_parts:
            cleaned = cleaned.replace(part, "")
        return cleaned.strip()

    def _analyze_dataframe(self, df, hospital_name, campaign_name):
        required_cols = ["Email", "Phish Status", "Email Status", "Template", "First Name", "Last Name"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"CSV is missing columns: {', '.join(missing)}")

        delivered_df = df[df["Email Status"] == "Delivered"].copy()
        delivered_df["Hospital"] = hospital_name
        delivered_df["Campaign"] = campaign_name
        reported_df = delivered_df[delivered_df["Phish Status"] == "Reported Attack"]

        total_delivered = len(delivered_df)
        total_reported = len(reported_df)
        report_rate = (total_reported / total_delivered * 100) if total_delivered > 0 else 0

        warning = ""
        if total_delivered > 0 and total_reported == 0:
            warning = "Make sure Phish Notify is installed as there is no reported email."

        return {
            "hospital": hospital_name,
            "campaign": campaign_name,
            "delivered": total_delivered,
            "reported": total_reported,
            "report_rate": report_rate,
            "warning": warning,
        }, delivered_df

    def _analyze_by_template(self, delivered_df, reported_df):
        templates = []
        for template in delivered_df["Template"].dropna().unique():
            temp_delivered_df = delivered_df[delivered_df["Template"] == template]
            temp_reported_df = reported_df[reported_df["Template"] == template]
            temp_delivered = len(temp_delivered_df)
            temp_reported = len(temp_reported_df)
            temp_rate = (temp_reported / temp_delivered * 100) if temp_delivered > 0 else 0
            templates.append({
                "name": template,
                "delivered": temp_delivered,
                "reported": temp_reported,
                "rate": temp_rate,
            })
        return sorted(templates, key=lambda x: x["rate"], reverse=True)

    def _analyze_by_user(self, delivered_df, reported_df):
        users = []
        for email in delivered_df["Email"].dropna().unique():
            user_delivered_df = delivered_df[delivered_df["Email"] == email]
            user_reported_df = reported_df[reported_df["Email"] == email]
            user_reported = len(user_reported_df)
            if user_reported > 0:
                user_delivered = len(user_delivered_df)
                user_rate = (user_reported / user_delivered * 100) if user_delivered > 0 else 0
                user_data = user_delivered_df.iloc[0]
                users.append({
                    "name": f"{user_data['First Name']} {user_data['Last Name']}",
                    "email": email,
                    "hospital": user_data.get("Hospital", ""),
                    "delivered": user_delivered,
                    "reported": user_reported,
                    "rate": user_rate,
                })
        return sorted(users, key=lambda x: x["reported"], reverse=True)

    def _rate_class(self, rate):
        if rate >= 10:
            return "high-rate"
        if rate >= 5:
            return "med-rate"
        return "low-rate"

    def _status_html(self, warning):
        if warning:
            return (
                '<span style="color:#d35400;font-weight:bold;">'
                '⚠️ Make sure Phish Notify is installed as there is no reported email.'
                '</span>'
            )
        return '<span style="color:#27ae60;font-weight:bold;">OK</span>'

    def _generate_dashboard(self, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hospital_labels = [h["hospital"] for h in data["hospitals"]]
        hospital_rates = [round(h["report_rate"], 1) for h in data["hospitals"]]
        status_labels = list(data["phish_status_breakdown"].keys())
        status_values = list(data["phish_status_breakdown"].values())

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infosec IQ - Regional Phishing Report Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1600px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 40px; }}
        header {{ text-align: center; margin-bottom: 40px; border-bottom: 3px solid #667eea; padding-bottom: 20px; }}
        h1 {{ color: #2c3e50; font-size: 2.3em; margin-bottom: 10px; }}
        .timestamp {{ color: #7f8c8d; font-size: 0.9em; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .metric-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 15px rgba(102,126,234,0.3); text-align: center; }}
        .metric-card h3 {{ font-size: 0.9em; opacity: 0.9; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
        .metric-value {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
        .metric-unit {{ font-size: 0.8em; opacity: 0.8; }}
        .chart-section {{ background: #f8f9fa; padding: 25px; border-radius: 8px; margin-bottom: 30px; }}
        .chart-section h2 {{ color: #2c3e50; margin-bottom: 10px; font-size: 1.5em; }}
        .chart-container {{ position: relative; height: 380px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #667eea; color: white; padding: 15px; text-align: left; font-weight: 600; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f5f7ff; }}
        .high-rate {{ color: #27ae60; font-weight: bold; }}
        .med-rate {{ color: #f39c12; font-weight: bold; }}
        .low-rate {{ color: #e74c3c; font-weight: bold; }}
        .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ecf0f1; color: #7f8c8d; font-size: 0.9em; }}
        .stat-box {{ background: white; border: 2px solid #667eea; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .note {{ color: #7f8c8d; font-size: 0.9em; margin-top: 8px; }}
        .warning-box {{ background:#fff3cd; border-left:6px solid #ffc107; color:#856404; padding:18px; margin:25px 0; border-radius:8px; font-weight:bold; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Regional Phishing Report Analysis</h1>
            <p class="timestamp">Generated: {timestamp}</p>
            <p class="timestamp">Source Folder: {html.escape(data['root_folder'])}</p>
        </header>

        <div class="metrics-grid">
            <div class="metric-card"><h3>Total Hospitals</h3><div class="metric-value">{len(data['hospitals'])}</div><div class="metric-unit">hospital folders analyzed</div></div>
            <div class="metric-card"><h3>Total Campaigns / Files</h3><div class="metric-value">{len(data['campaigns'])}</div><div class="metric-unit">CSV exports analyzed</div></div>
            <div class="metric-card"><h3>Total Delivered Emails</h3><div class="metric-value">{data['total_delivered']}</div><div class="metric-unit">phishing simulation emails</div></div>
            <div class="metric-card"><h3>Emails Reported</h3><div class="metric-value">{data['total_reported']}</div><div class="metric-unit">users flagged as attack</div></div>
            <div class="metric-card"><h3>Overall Report Rate</h3><div class="metric-value">{data['report_rate']:.1f}%</div><div class="metric-unit">of delivered emails</div></div>
        </div>
"""

        if data.get("excluded_zero_reported"):
            html_content += """
        <div class="warning-box">
            The following hospitals were excluded from the final statistics because they had no reported emails and may need Phish Notify verification:<br><br>
"""
            for hospital in data["excluded_zero_reported"]:
                html_content += f"            • {html.escape(str(hospital))}<br>\n"
            html_content += """
        </div>
"""

        html_content += """
        <div class="chart-section">
            <h2>Hospital Comparison by Report Rate</h2>
            <div class="chart-container"><canvas id="hospitalRateChart"></canvas></div>
        </div>

        <div class="chart-section">
            <h2>Hospital Summary</h2>
            <p class="note">All CSV files inside the same hospital folder are combined here.</p>
            <table>
                <thead><tr><th>Hospital</th><th>Campaigns / Files</th><th>Emails Delivered</th><th>Emails Reported</th><th>Report Rate</th><th>Status</th></tr></thead>
                <tbody>
"""

        for hospital in data["hospitals"]:
            rate_class = self._rate_class(hospital["report_rate"])
            status = self._status_html(hospital.get("warning"))
            html_content += f"""
                    <tr>
                        <td>{html.escape(str(hospital['hospital']))}</td>
                        <td>{hospital['campaigns']}</td>
                        <td>{hospital['delivered']}</td>
                        <td>{hospital['reported']}</td>
                        <td class="{rate_class}">{hospital['report_rate']:.1f}%</td>
                        <td>{status}</td>
                    </tr>
"""

        html_content += """
                </tbody>
            </table>
        </div>

        <div class="chart-section">
            <h2>Campaign / File Summary</h2>
            <p class="note">This section shows each individual CSV file under its hospital.</p>
            <table>
                <thead><tr><th>Hospital</th><th>Campaign / File</th><th>Emails Delivered</th><th>Emails Reported</th><th>Report Rate</th><th>Status</th></tr></thead>
                <tbody>
"""

        for campaign in data["campaigns"]:
            rate_class = self._rate_class(campaign["report_rate"])
            status = self._status_html(campaign.get("warning"))
            html_content += f"""
                    <tr>
                        <td>{html.escape(str(campaign['hospital']))}</td>
                        <td>{html.escape(str(campaign['campaign']))}</td>
                        <td>{campaign['delivered']}</td>
                        <td>{campaign['reported']}</td>
                        <td class="{rate_class}">{campaign['report_rate']:.1f}%</td>
                        <td>{status}</td>
                    </tr>
"""

        html_content += """
                </tbody>
            </table>
        </div>

        <div class="chart-section">
            <h2>Email Status Breakdown</h2>
            <p class="note">Click the legend below to show or hide categories.</p>
            <div class="chart-container"><canvas id="statusChart"></canvas></div>
        </div>

        <div class="chart-section">
            <h2>Campaign / Template Performance</h2>
            <table>
                <thead><tr><th>Campaign / Template</th><th>Emails Delivered</th><th>Emails Reported</th><th>Report Rate</th></tr></thead>
                <tbody>
"""

        for template in data["by_template"]:
            rate_class = self._rate_class(template["rate"])
            html_content += f"""
                    <tr>
                        <td>{html.escape(str(template['name']))}</td>
                        <td>{template['delivered']}</td>
                        <td>{template['reported']}</td>
                        <td class="{rate_class}">{template['rate']:.1f}%</td>
                    </tr>
"""

        html_content += """
                </tbody>
            </table>
        </div>

        <div class="chart-section">
            <h2>Top Reporters</h2>
            <table>
                <thead><tr><th>User Name</th><th>Email</th><th>Hospital</th><th>Emails Delivered</th><th>Emails Reported</th><th>Report Rate</th></tr></thead>
                <tbody>
"""

        for user in data["by_user"][:50]:
            html_content += f"""
                    <tr>
                        <td>{html.escape(str(user['name']))}</td>
                        <td>{html.escape(str(user['email']))}</td>
                        <td>{html.escape(str(user['hospital']))}</td>
                        <td>{user['delivered']}</td>
                        <td>{user['reported']}</td>
                        <td class="high-rate">{user['rate']:.1f}%</td>
                    </tr>
"""

        html_content += """
                </tbody>
            </table>
        </div>

        <div class="chart-section">
            <h2>Phish Status Distribution</h2>
            <div class="stat-box">
"""

        for status, count in data["phish_status_breakdown"].items():
            percentage = (count / data["total_delivered"] * 100) if data["total_delivered"] > 0 else 0
            html_content += f"<div><strong>{html.escape(str(status))}:</strong> {count} ({percentage:.1f}%)</div>"

        if data["skipped_files"]:
            html_content += """
            </div>
        </div>
        <div class="chart-section">
            <h2>Skipped Files</h2>
            <div class="stat-box">
"""
            for skipped in data["skipped_files"]:
                html_content += f"<div>{html.escape(skipped)}</div>"

        html_content += f"""
            </div>
        </div>

        <footer>
            <p>This report contains sensitive security information. Handle with appropriate confidentiality.</p>
            <p>For questions or analysis requests, contact the SOC team.</p>
        </footer>
    </div>

    <script>
        const hospitalLabels = {json.dumps(hospital_labels)};
        const hospitalRates = {json.dumps(hospital_rates)};
        const statusLabels = {json.dumps(status_labels)};
        const statusValues = {json.dumps(status_values)};

        new Chart(document.getElementById('hospitalRateChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: hospitalLabels,
                datasets: [{{
                    label: 'Report Rate %',
                    data: hospitalRates,
                    backgroundColor: '#667eea',
                    borderColor: '#4c63c7',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'Report Rate %' }} }} }}
            }}
        }});

        new Chart(document.getElementById('statusChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: statusLabels,
                datasets: [{{
                    data: statusValues,
                    backgroundColor: ['#27ae60', '#f39c12', '#e74c3c', '#3498db', '#9b59b6', '#34495e'],
                    borderColor: '#fff',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'bottom' }} }}
            }}
        }});
    </script>
</body>
</html>
"""

        output_dir = Path.home() / "Documents" / "Phishing_Reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"Regional_Phishing_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(filepath)

    def _update_ui_after_processing(self, excluded_zero_reported=None):
        self.status_label.config(text="Processing complete!", fg="#27ae60")

        excluded_zero_reported = excluded_zero_reported or []
        if excluded_zero_reported:
            messagebox.showinfo(
                "Dashboard Generated",
                "Dashboard generated successfully.\n\nExcluded from final statistics:\n\n"
                + "\n".join(excluded_zero_reported)
            )
        else:
            messagebox.showinfo("Success", "Dashboard generated successfully!")

        if self.dashboard_path and os.path.exists(self.dashboard_path):
            webbrowser.open(f"file://{self.dashboard_path}")
        else:
            messagebox.showerror("Error", "Dashboard not found.")

    def open_dashboard(self):
        if self.dashboard_path and os.path.exists(self.dashboard_path):
            webbrowser.open(f"file://{self.dashboard_path}")
        else:
            messagebox.showerror("Error", "Dashboard not found.")
    def _cleanup_processing(self):
        self.process_btn.config(
            text="Generate Dashboard",
            state="normal",
            bg="#27ae60"
        )



if __name__ == "__main__":
    root = tk.Tk()
    app = PhishingAnalyzerApp(root)
    root.mainloop()
