#!/bin/bash

# Input parameters:
#   - $1 - true - starting service WITHOUT cached data (allows to start the service faster);
#          false - starting the service WITH cache (cache is cleared)
#          default = false

INI_CONFIG_FILE="${1:-pytest.ini}"
clear_cache=${2:-false}

ORIGINAL_PROJECT_PATH="$(pwd)"
source ./setup.sh || { echo "setup.sh failed"; exit 1; }
if [[ $? -ne 0 ]]; then
  return 1
fi

set -Eeuo pipefail
trap cleanup EXIT ERR SIGINT SIGTERM

cleanup() {
  echo "Deactivating venv, if active..."
  deactivate
  echo "Returning to the original project path to be able to run the test again with new changes, if there are any"
  cd "$ORIGINAL_PROJECT_PATH"
}

echo "Building images..."
case "$clear_cache" in
  true)
    echo "Cache will be cleared when starting the service"
    # docker compose build tests --no-cache
    ;;
  *)
    echo "Cache will be preserved when starting the service"
    # docker compose build tests
esac

# echo "Starting the tests..."
# docker compose run --rm tests

if [[ ! -f "$INI_CONFIG_FILE" ]]; then
  echo "ERROR: Provided path '$INI_CONFIG_FILE' for the repo does not exist"
  return 1
else
  echo "Using $INI_CONFIG_FILE ini config file"
fi

# python3 -m pytest -v --tb=short -s --reruns 2 --reruns-delay 2 --ini-config "$INI_CONFIG_FILE" --html=$HOST_ARTIFACTS/test_report_$(date +%Y-%m-%d_%H-%M-%S).html
python3 -m pytest -v --tb=short -k test_login_success_admin -s -c "$INI_CONFIG_FILE" --html=$HOST_ARTIFACTS/test_report_$(date +%Y-%m-%d_%H-%M-%S).html

#
#
#
