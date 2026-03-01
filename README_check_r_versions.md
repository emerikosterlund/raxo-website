# check_r_versions — Compare R versions between RStudio and VS Code

This repository contains a small R script to help verify that VS Code and RStudio are using the same R installation.

Files
- `check_r_versions.R`: prints R version, R home, path to `R` in PATH, environment variable `RSTUDIO`, and `sessionInfo()`.

How to use

1. In RStudio
- Open `check_r_versions.R` in RStudio and run the script (Source or run all). The output will appear in the R console.

2. In VS Code
- Option A — using the integrated R extension: open `check_r_versions.R` and run the script in the VS Code R console.
- Option B — using a terminal: run:

```bash
Rscript check_r_versions.R
```

3. Compare
- Check the printed `R.version.string` and `Sys.which('R')` values from both runs.
- If the `R.version.string` and `Sys.which('R')` outputs match, both editors are using the same R installation.

Notes
- `Sys.which('R')` shows the `R` executable found on the PATH for the process running the script. VS Code's R extension can be configured to point to a specific R binary; confirm that setting if you see different paths.
- On Windows, VS Code may use the `r.rterm.windows` setting or R extension configuration to select R. In RStudio, R is chosen in Tools → Global Options → General.
