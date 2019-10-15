#!/usr/bin/env python
# -*- encoding: utf-8

import contextlib
import os
import subprocess
import sys
import tempfile


@contextlib.contextmanager
def working_directory(path):
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(prev_cwd)


try:
    youtube_url = sys.argv[1]
except IndexError:
    sys.exit('Usage: %s <YOUTUBE_URL>' % __file__)


with working_directory(tempfile.mkdtemp()):
    subprocess.check_call([
        'youtube-dl',
        '--write-auto-sub', '--skip-download',

        # This option is busted because I'm using --skip-download.
        # In an ideal world, I'd download direct to srt, because there are
        # really good libraries for parsing srt in Python, but not vrt.
        #
        # Bug report: https://github.com/rg3/youtube-dl/issues/9073
        # '--convert-subs' ,'srt',

        youtube_url
    ])

    # Check we have exactly one file saved, and it's the
    assert len(os.listdir('.')) == 1
    assert os.listdir('.')[0].endswith('.vtt')

    vtt_path = os.listdir('.')[0]
    srt_path = vtt_path.replace('.vtt', '.srt')

    subprocess.check_call(['ffmpeg', '-i', vtt_path, srt_path])
