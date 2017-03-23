# Use a simple shell loop, to process each of the images.
  mkdir rotated

  for f in *.png
  do 
	convert "$f" -background none -rotate 5 rotated/"$f"_5R.png
	convert "$f" -background none -rotate 10 rotated/"$f"_10R.png
	convert "$f" -background none -rotate 15 rotated/"$f"_15R.png

	convert "$f" -background none -rotate -5 rotated/"$f"_5L.png
	convert "$f" -background none -rotate -10 rotated/"$f"_10L.png
	convert "$f" -background none -rotate -15 rotated/"$f"_15L.png

  done
