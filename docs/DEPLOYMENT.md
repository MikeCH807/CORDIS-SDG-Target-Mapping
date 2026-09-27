# Deployment

Publish only the contents of this release directory as the public repository root. Do not push the private research master. Python 3.12 is the tested interpreter family.

```bash
python -m venv .venv
# Activate .venv using the command appropriate for your shell.
python -m pip install -r requirements.txt
python tests/release_integrity_test.py
python -m streamlit run app/app.py
```

The app resolves paths from its own file and reads only bundled data. No OpenAI credentials, model weights or GPU are needed. It displays frozen results and does not map future project text. No funding/country/organisation analysis is provided by this release. Do not interpret multi-label row counts as project-level funding totals.

For Streamlit Community Cloud, select `app/app.py` as entry point, Python 3.12, and this root's standard `requirements.txt`. Do not add secrets. This configuration is prepared but public deployment is NOT TESTED. Runtime resource use depends on Streamlit/pandas; no laptop RAM minimum is certified.

Run the notebook from this root or its `notebooks` directory:

```bash
python -m jupyter nbconvert --execute --to notebook --inplace notebooks/final_analysis.ipynb
```

It uses only release paths and creates the five figures. Regenerated outputs may change presentation hashes; regenerate the release manifest only after reviewing intentional changes. Tests also support `python -O tests/release_integrity_test.py` and do not rely on removable Python assertions.

Before publishing: resolve LICENSE_STATUS.md, inspect app desktop/narrow layouts, review included project text and third-party attribution, create/push a repository containing only this release, deploy, then test all pages and downloads in an incognito browser. Insert the verified public URL in README and submission, create the final release ZIP, and perform a post-deployment audit. Deployment and ZIP creation were not authorized in this build task.

PUBLIC APP URL: TO BE ADDED AFTER DEPLOYMENT
