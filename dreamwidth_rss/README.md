# dreamwidth_rss

This directory contains a script for making an RSS feed from my Dreamwidth Reading Page.

It's a bit of a hack -- it pretends to be a browser, logs in to Dreamwidth, then creates an RSS feed from all the entries from my friends.

The feed it creates only includes *links* to posts, their titles and the tags -- you need to log in to Dreamwidth proper to see what a post actually says.
I'm trying to keep a balance between having a useful feed, and not having a feed that isn't at risk of leaking private post content.

Here are some examples of the entries the feed contains:

> **Fantastic Beats speculating**
> Sep 28th 2018, 00:00, by theweirdsisters
>
> This post is tagged with harry-potter,music
>
> **Can we do some more testing please?**
> Sep 27th 2018, 00:00, by frustrateddev
>
> (This post is untagged)

## Usage

I'm running this script with Python 2.7.12; other Python versions should work but they're untested.

1.  Clone the repo:

    ```console
    $ git clone git@github.com:alexwlchan/junkdrawer.git
    $ cd junkdrawer/dreamwidth_rss
    ```

2.  Create a virtualenv, install dependencies:

    ```console
    $ virtualenv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    ```

3.  Run the script, passing your username and password as parameters:

    ```console
    $ python build_dreamwidth_rss.py --username=USERNAME --password=PASSWORD
    ```
