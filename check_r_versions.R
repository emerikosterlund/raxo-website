# check_r_versions.R
# Prints information to compare R used in different environments (RStudio vs VS Code)

cat("--- R basic info ---\n")
cat("R.version.string:", R.version$version.string, "\n")
cat("Platform:", R.version$platform, "\n")
cat("R.home():", R.home(), "\n")
cat("Sys.which('R'):", Sys.which("R"), "\n")
cat("RSTUDIO environment variable:", Sys.getenv("RSTUDIO"), "\n")

cat("\n--- sessionInfo() ---\n")
print(sessionInfo())

cat("\n--- external 'R --version' (if available in PATH) ---\n")
if (!is.null(ext_ver <- tryCatch(system("R --version", intern = TRUE), error = function(e) NULL))) {
  cat(paste(ext_ver, collapse = "\n"), "\n")
} else {
  cat("(external 'R' not found in PATH or failed to run)\n")
}

cat("\nRun this script in RStudio and in VS Code (or use `Rscript`) and compare the outputs.\n")