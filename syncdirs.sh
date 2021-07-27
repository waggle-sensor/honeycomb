while inotifywait -r -e modify,create,delete,move ./client; do
    rsync -aP ./client/* node-000048B02D0766CD:/honeycomb
    ssh node-000048B02D0766CD "systemctl restart honeycomb"
done