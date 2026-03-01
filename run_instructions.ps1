# run_instructions.ps1
# PowerShell helper to locate R and optionally run the check_r_versions.R script
param(
  [switch]$Run
)

Write-Host "Checking for R executable in PATH..."
try {
  $rCmd = Get-Command R -ErrorAction Stop
  Write-Host "R found at:" $rCmd.Source
} catch {
  Write-Host "R executable not found in PATH."
  Write-Host "If you have R installed, ensure its bin folder (containing R.exe and Rscript.exe) is added to your PATH, or configure VS Code's R extension to point to the correct R binary."
}

if ($Run) {
  if (Get-Command Rscript -ErrorAction SilentlyContinue) {
    Write-Host "Running: Rscript check_r_versions.R`n"
    & Rscript check_r_versions.R
  } else {
    Write-Host "Rscript not found in PATH — cannot run the script."
  }
}
