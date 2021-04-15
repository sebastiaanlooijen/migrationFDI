# geodist.R - this scripts loads and saves the CEPII geodist dataset
# Sebastiaan Looijen, april 2021

# load package ------------------------------------------------------------
library(cepiigeodist)

# load dataset ------------------------------------------------------------
geodist <- cepiigeodist::dist_cepii

# write file --------------------------------------------------------------
write.csv(
  geodist, 
  "~/Documents/migrationFDI/sources/geodist/geodist.csv",
  row.names = FALSE
  )
