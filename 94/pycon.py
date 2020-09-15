from collections import namedtuple
import os
import pickle
import urllib.request

# prework
# download pickle file and store it in a tmp file
pkl_file = 'pycon_videos.pkl'
data = f'https://bites-data.s3.us-east-2.amazonaws.com/{pkl_file}'
tmp = os.getenv("TMP", "/tmp")
pycon_videos = os.path.join(tmp, pkl_file)
urllib.request.urlretrieve(data, pycon_videos)

# the pkl contains a list of Video namedtuples
Video = namedtuple('Video', 'id title duration metrics')


def load_pycon_data(pycon_videos=pycon_videos):
    """Load the pickle file (pycon_videos) and return the data structure
       it holds"""
    with open(pycon_videos, 'rb') as fd:
        return pickle.load(fd)


def get_most_popular_talks_by_views(videos):
    """Return the pycon video list sorted by viewCount"""
    return sorted(videos, key=lambda x: int(x.metrics['viewCount']), reverse=True)


def get_most_popular_talks_by_like_ratio(videos):
    """Return the pycon video list sorted by most likes relative to
       number of views, so 10 likes on 175 views ranks higher than
       12 likes on 300 views. Discount the dislikeCount from the likeCount.
       Return the filtered list"""
    def _like_ratio(video):
        views = int(video.metrics['viewCount'])
        likes = int(video.metrics['likeCount'])
        dislikes = int(video.metrics['dislikeCount'])
        return (likes-dislikes) / views

    return sorted(videos, key=_like_ratio, reverse=True)


# taken from https://stackoverflow.com/a/35159973/238845
def iso8601DurationToSeconds(duration): #eg P1W2DT6H21M32S
    week = 0
    day  = 0
    hour = 0
    min  = 0
    sec  = 0

    duration = duration.lower()

    value = ''
    for c in duration:
        if c.isdigit():
            value += c
            continue

        elif c == 'p':
            pass
        elif c == 't':
            pass
        elif c == 'w':
            week = int(value) * 604800
        elif c == 'd':
            day = int(value)  * 86400
        elif c == 'h':
            hour = int(value) * 3600
        elif c == 'm':
            min = int(value)  * 60
        elif c == 's':
            sec = int(value)

        value = ''

    return week + day + hour + min + sec


def get_talks_gt_one_hour(videos):
    """Filter the videos list down to videos of > 1 hour"""
    return [video for video in videos if iso8601DurationToSeconds(video.duration) > 60 * 60]


def get_talks_lt_twentyfour_min(videos):
    """Filter videos list down to videos that have a duration of less than
       24 minutes"""
    return [video for video in videos if iso8601DurationToSeconds(video.duration) < 60 * 24]