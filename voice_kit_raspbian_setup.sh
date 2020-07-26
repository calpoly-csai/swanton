#Add AIY package repo:

echo "deb https://packages.cloud.google.com/apt aiyprojects-stable main" | sudo tee /etc/apt/sources.list.d/aiyprojects.list

#Add Google package keys:

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
