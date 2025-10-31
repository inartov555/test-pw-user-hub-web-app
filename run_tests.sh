#!/bin/bash

# Input parameters:
#   - $1 - true - starting service WITHOUT cached data (allows to start the service faster);
#          false - starting the service WITH cache (cache is cleared)
#          default = false

clear_cache=${1:-false}

ORIGINAL_PROJECT_PATH="$(pwd)"
source ./setup.sh || { echo "setup.sh failed"; exit 1; }
if [[ $? -ne 0 ]]; then
  return 1
fi

set -Eeuo pipefail
trap cleanup EXIT ERR SIGINT SIGTERM

cleanup() {
  echo "Returning to the original project path to be able to run the test again with new changes, if there are any"
  cd "$ORIGINAL_PROJECT_PATH"
}

echo "Building images..."
case "$clear_cache" in
  true)
    echo "Cache will be cleared when starting the service"
    docker compose build --no-cache
    ;;
  *)
    echo "Cache will be preserved when starting the service"
    docker compose build
esac

echo "Starting the service"
docker compose up
