#!/bin/sh
set +e

cd $(dirname $0)

cp mycelium.service /etc/systemd/system
systemctl daemon-reload
systemctl restart mycelium
systemctl enable mycelium
