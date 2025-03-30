./run_dict.sh &

gunicorn -w 4 'main:app'