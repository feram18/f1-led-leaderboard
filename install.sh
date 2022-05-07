#!/usr/bin/bash
# Description: Install F1-LED-Leaderboard software (github.com/feram18/f1-led-leaderboard)

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

function installMatrixLibrary() {
  printf "\nInstalling rpi-rgb-led-matrix library...\n"
  cd "${ROOT_DIR}/rpi-rgb-led-matrix/" || exit
  make build-python PYTHON="$(command -v python3)"
  sudo make install-python PYTHON="$(command -v python3)"
  cd "${ROOT_DIR}" || exit
}

main() {
  echo "$(tput setaf 5)__________________________________________________________________________________________"
  echo "$(tput setaf 5)   ___  _     __    __  ___     __                _           _                         _ "
  echo "$(tput setaf 5)  / __\/ |   / /   /__\/   \   / /  ___  __ _  __| | ___ _ __| |__   ___   __ _ _ __ __| |"
  echo "$(tput setaf 5) / _\  | |  / /   /_\ / /\ /  / /  / _ \/ _\` |/ _\` |/ _ \ '__| '_ \ / _ \ / _\` | '__/ _\` |"
  echo "$(tput setaf 5)/ /    | | / /___//__/ /_//  / /__|  __/ (_| | (_| |  __/ |  | |_) | (_) | (_| | | | (_| |"
  echo "$(tput setaf 5)\/     |_| \____/\__/___,'   \____/\___|\__,_|\__,_|\___|_|  |_.__/ \___/ \__,_|_|  \__,_|"
  echo "$(tput setaf 5)__________________________________________________________________________________________"

  echo -e "$(tput setaf 7)\nUpdating system & installing Python 3"
  sudo apt-get update && sudo apt install python3-dev

  installMatrixLibrary

  chmod +x update.sh
  ./update.sh

  echo -e "\n$(tput setaf 2)If there are no errors shown above, installation was successful."
  echo "$(tput setaf 7)To make sure your matrix is working properly, execute the samples located in ./rpi-rgb-led-matrix/bindings/python/samples"

  exit
}

main