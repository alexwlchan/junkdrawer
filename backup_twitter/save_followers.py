#!/usr/bin/env python
# -*- encoding: utf-8

from twitter_oauth import TwitterSession, save_user_info


if __name__ == "__main__":
    sess = TwitterSession()

    followers = sess.list_followers()
    save_user_info(followers, dirname="followers")
