#!/usr/bin/bash
# Description: Update F1-LED-Leaderboard software (github.com/feram18/f1-led-leaderboard)

# Cleans up repository directory
function clean() {
  rm -f "*.log*"  # Log files
  sudo rm -rf "*/__pycache__"  # pycache
  sudo rm -rf "__pycache__"
}

# Updates repository
function updateRepository() {
  printf "Updating repository...\n"
  git reset --hard
  git checkout master
  git fetch --tags
  tag="$(git describe --tags "git rev-list --tags --max-count=1")"
  git checkout tags/"$tag"
}

# Installs dependencies
function installDependencies(){
  printf "\nInstalling dependencies...\n"
  sudo pip3 install -r requirements.txt
}

function main() {
  clean
  updateRepository
  installDependencies

  # Allow scripts to be easily executed next time
  chmod +x install.sh update.sh

  echo "$(tput setaf 2)Update completed$(tput setaf 7)"
}

# Execute script
main