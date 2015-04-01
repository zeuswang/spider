date=`date +%Y-%m-%d`
python get_new_movie.py ../conf/template ../data/movie.$date ../data/link.$date ../data/pic/ |tee ../log/log.$date
cp ../data/movie.$date /home/wangwei/moviesite/moviesite/main/movie
cp ../data/link.$date /home/wangwei/moviesite/moviesite/main/link
