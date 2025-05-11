#!/usr/bin/bash
# Description: Update F1-LED-Leaderboard software (github.com/feram18/f1-led-leaderboard)

function clean() {
  rm -f "*.log*"
  sudo rm -rf "*/__pycache__"
  sudo rm -rf "__pycache__"
}

function updateRepository() {
  printf "Updating repository...\n"
  git reset --hard
  git fetch --tags --force
  tag="$(git tag --sort=-v:refname | head -n 1)"
  git checkout tags/"$tag"
}

function installDependencies() {
  printf "\nInstalling dependencies...\n"
  sudo pip3 install -r requirements.txt
}

function main() {
  clean
  updateRepository
  installDependencies

  chmod +x install.sh update.sh

  echo "$(tput setaf 2)Update completed$(tput setaf 7)"
}

main