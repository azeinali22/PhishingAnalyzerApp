\# 🛡️ Regional Phishing Report Analyzer



A Python desktop application that automates the analysis of \*\*InfoSec IQ phishing campaign reports\*\* across multiple hospitals and generates an interactive HTML dashboard.



Built with \*\*Python\*\*, \*\*Tkinter\*\*, and \*\*Pandas\*\*.



\---



\## Features



\- 📂 Analyze multiple hospital folders at once

\- ✅ Automatically detects hospital folders

\- 📊 Generates a professional interactive HTML dashboard

\- 📈 Hospital comparison charts

\- 📧 Campaign performance analysis

\- 👤 Top phishing reporters

\- 📉 Phish status breakdown

\- ⚠️ Detects hospitals with no reported emails

\- 🗂️ Option to exclude hospitals with missing Phish Notify reporting

\- 🌐 Automatically opens the generated dashboard in your browser



\---



\## Dashboard Includes



\- Overall reporting statistics

\- Hospital comparison

\- Campaign summary

\- Template performance

\- Top reporters

\- Email status distribution

\- Skipped file reporting

\- Interactive charts powered by Chart.js



\---



\## Technologies



\- Python 3

\- Tkinter

\- Pandas

\- HTML/CSS

\- Chart.js



\---



\## Requirements



```bash

pip install pandas

```



Tkinter is included with the standard Python installation on Windows.



\---



\## Project Structure



```

PhishingAnalyzerApp/

│

├── InfosecIQ.py

├── README.md

├── .gitignore

└── assets/

```



\---



\## Folder Structure for Reports



The application expects the following folder layout:



```

Reports/

│

├── TBRHSC \& SJCG/

│   ├── Campaign1.csv

│   ├── Campaign2.csv

│

├── Riverside/

│   ├── Campaign1.csv

│

├── Dryden/

│   ├── Campaign1.csv

│

└── Kenora/

&#x20;   ├── Campaign1.csv

```



Each subfolder represents one hospital.



\---



\## How to Use



1\. Launch the application.

2\. Click \*\*Select Reports Folder\*\*.

3\. Choose the main folder containing all hospital folders.

4\. Select which hospitals to include.

5\. Click \*\*Generate Dashboard\*\*.

6\. Review the generated interactive HTML report.



The dashboard is automatically saved to:



```

Documents/Phishing\_Reports/

```



and opened in your default web browser. :contentReference\[oaicite:0]{index=0}



\---



\## Output



The application generates an interactive dashboard containing:



\- Total hospitals analyzed

\- Total campaigns

\- Delivered emails

\- Reported emails

\- Overall report rate

\- Hospital comparison charts

\- Campaign statistics

\- User reporting statistics

\- Template analysis

\- Phish status breakdown



\---



\## Key Features



✔ Multi-hospital analysis



✔ Automatic campaign aggregation



✔ Interactive HTML reports



✔ Automatic hospital discovery



✔ CSV validation



✔ Error reporting for invalid files



✔ Professional dashboard interface



✔ Automatic browser launch



\---



\## Future Improvements



\- Export to PDF

\- Excel summary export

\- Trend analysis

\- Monthly comparison reports

\- Dark mode

\- Additional dashboard visualizations



\---



\## License



This project is intended for educational and organizational cybersecurity reporting purposes.



\---



\## Author



\*\*Amirhossein Zeinali Dehaghani\*\*



Cybersecurity • IT • Python Development

