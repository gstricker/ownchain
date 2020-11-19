#!/bin/bash --login

# exit on non-zero status
set -e

# activate conda environment and let the following process take over
conda activate ownchain
exec "$@"
