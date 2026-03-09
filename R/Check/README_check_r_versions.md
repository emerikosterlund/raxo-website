# check_r_versions — Compare R versions between RStudio and VS Code

This repository contains a small R script to help verify that VS Code and RStudio are using the same R installation.

Files
- `check_r_versions.R`: prints R version, R home, path to `R` in PATH, environment variable `RSTUDIO`, and `sessionInfo()`.

How to use

1. In RStudio
- Open `check_r_versions.R` in RStudio and run the script (Source or run all). The output will appear in the R console.

2. In VS Code / Windows PowerShell
- Option A — using the integrated R extension: open `check_r_versions.R` and run the script in the VS Code R console.
- Option B — using a terminal.

PowerShell (recommended on Windows):

```powershell
# Check for R in PATH only
Get-Command R -ErrorAction SilentlyContinue

# Run the helper PowerShell script which will locate R and optionally run the R script
.\run_instructions.ps1 -Run
```

Direct `Rscript` invocation (works in PowerShell/CMD/Git Bash if `Rscript` is on PATH):

```powershell
Rscript check_r_versions.R
```

3. Compare
- Check the printed `R.version.string` and `Sys.which('R')` values from both runs.
- If the `R.version.string` and `Sys.which('R')` outputs match, both editors are using the same R installation.

Notes
- `Sys.which('R')` shows the `R` executable found on the PATH for the process running the script. VS Code's R extension can be configured to point to a specific R binary; confirm that setting if you see different paths.
- On Windows, VS Code may use the `r.rterm.windows` setting or R extension configuration to select R. In RStudio, R is chosen in Tools → Global Options → General.
- If you can't trigger the script: ensure `R`/`Rscript` are on your system `PATH`, or use the `run_instructions.ps1` helper to diagnose.
- To add R to PATH on Windows, add the folder that contains `R.exe` and `Rscript.exe` (for example `C:\Program Files\R\R-4.3.2\bin`) to your user or system PATH environment variable, then restart VS Code.
