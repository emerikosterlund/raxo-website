# check_r_versions.R
cat("R version:", R.version$version.string, "\n")
cat("R home:   ", R.home(), "\n")
cat("R in PATH:", Sys.which("R"), "\n")
