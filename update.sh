#!/bin/bash
export HOME="/home/app.e0016372"
export http_proxy="http://172.19.92.23:13128"
export https_proxy="http://172.19.92.23:13128"

cd "/nas_data/userdata/randy/projects/loss_plotter"
CONVERTER="/home/app.e0016372/miniconda3/envs/main/bin/jupyter-nbconvert"

while true; do
    echo "$(seq -s '*' 101 | tr -d '[:digit:]')"
    echo "[$(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M:%S %Z')]"
    $CONVERTER --execute --inplace plotter.ipynb

    git checkout --orphan temp
    git add -A
    git commit -m "Auto sync commit"

    git push -f origin temp:main
    git checkout main
    git branch -D temp

    sleep 300
done
