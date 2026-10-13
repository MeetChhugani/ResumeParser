# Resume Matcher

A Streamlit application for comparing a candidate's resume with a job description. It provides a match score, a 70% hiring-screen recommendation, a candidate summary, and a library of editable job descriptions for common roles.

## Features

- Upload a candidate resume in PDF or TXT format.
- Select a job role from the built-in role library.
- Search roles and add or remove custom roles.
- Start with a prepared job description and edit it for a specific opening.
- Compare the resume and job description using term similarity.
- Exclude generic words from the skill comparison.
- Show a match score and recommendation:
  - **70% or higher:** Candidate can be considered for review.
  - **Below 70%:** Candidate needs stronger alignment with the role.
- Show role-specific missing terms and interview focus points.

## Project structure

```text
Resume_Matcher/
├── app.py                 # Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Light theme configuration
├── README.md              # Project documentation
└── .gitignore             # Files excluded from Git
```

## Requirements

- Python 3.10 or later
- pip
- A modern web browser

## Run locally

### 1. Clone the repository

```powershell
git clone <YOUR_PRIVATE_REPOSITORY_URL>
cd Resume_Matcher
```

If you received the project as a ZIP file, extract it and open PowerShell in the `Resume_Matcher` folder instead.

### 2. Create a virtual environment

```powershell
py -m venv .venv
```

If `py` is unavailable, use:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this once for the current terminal and then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Start the app

```powershell
streamlit run app.py
```

Streamlit will print a local address similar to the following. Open it in a browser:

```text
http://localhost:8501
```

## How to use the app

1. Choose a role from **Smart Role Library**.
2. Use **Manage role library** to add a custom role or remove an unneeded one.
3. Review and edit the job description for the selected role.
4. Upload the candidate's resume as a PDF or TXT file.
5. Click **Analyze candidate**.
6. Review the match score, hiring prediction, candidate summary, and missing role-specific terms.

## Troubleshooting

### `streamlit` is not recognized

Confirm the virtual environment is active, then install dependencies again:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### The existing virtual environment does not work

Delete the local `.venv` directory, then repeat the virtual-environment creation and installation steps above. The `.venv` directory is not included in Git.

### The app does not refresh after code changes

Stop the app using `Ctrl+C`, then start it again:

```powershell
streamlit run app.py
```

## Notes on screening

The match score is a first-pass comparison aid. It should support recruiter or hiring-manager review, not replace professional evaluation of candidates.

## Dependencies

- [Streamlit](https://streamlit.io/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [scikit-learn](https://scikit-learn.org/)
