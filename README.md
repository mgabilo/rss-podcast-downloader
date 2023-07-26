# How to use

```
python rss.py
```

This will read the rss feeds in `rss_list.txt` and download all the episodes in
each one. It will write to a folder for each separate RSS feed.

One of the main features is that it writes a filename corresponding to the
title of the episode. It does not use the original filename, which tends to be
not informative. This is the main reason this project exists instead of just
using gPodder.

