#!/bin/bash

# Exit script if any command fails
set -e

# Update package list and install necessary packages
apt-get update
apt-get install -y --no-install-recommends apt-utils curl wget vim coreutils zsh

# Download and run Oh My Zsh install script
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Change Oh My Zsh theme
sed -i -e 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/g' ~/.zshrc
