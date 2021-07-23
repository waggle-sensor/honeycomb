while inotifywait -r -e modify,create,delete,move ./prod; do
    rsync -aP ./prod/* node-000048B02D0766CD:/honeycomb
    ssh node-000048B02D0766CD "systemctl restart honeycomb"
done