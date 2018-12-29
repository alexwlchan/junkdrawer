#!/usr/bin/env python
# -*- encoding: utf-8

from twitter_oauth import TwitterSession, save_user_info


if __name__ == "__main__":
    sess = TwitterSession()

    friends = sess.list_friends()
    save_user_info(friends, dirname="friends")
