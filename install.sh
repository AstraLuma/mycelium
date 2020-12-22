#!/bin/sh
set -ex

cd $(dirname $0)

cp mycelium.service /etc/systemd/system
pip3 install -r requirements.txt
systemctl daemon-reload
systemctl restart mycelium
systemctl enable mycelium
