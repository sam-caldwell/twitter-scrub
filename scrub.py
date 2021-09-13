#!/usr/bin/env python3
"""
    twitter-scrub
    (c) 2019 Sam Caldwell.  See LICENSE.txt file.

    This tool will scrub your twitter timeline.

"""
from argparse import ArgumentParser
import tweepy
import time
import sys


def get_arguments():
    """
        Parse and return the cli arguments
        :return:
    """
    parser = ArgumentParser(
        description="scrub a given twitter account's posts")
    parser.add_argument(
        "--noop",
        required=False,
        action="store_true",
        default=False,
        help="No operation flag (for dry runs).")
    parser.add_argument(
        "--timeline",
        required=False,
        action="store_true",
        help="Purge timeline"
    )
    parser.add_argument(
        "--likes",
        required=False,
        action="store_true",
        help="Purge likes"
    )
    parser.add_argument(
        "--dms",
        required=False, \
        action="store_true",
        help="Purge direct messages"
    )
    parser.add_argument(
        "--key",
        required=True,
        type=str,
        help="Consumer Key")
    parser.add_argument(
        "--secret",
        required=True,
        type=str,
        help="Consumer secret")
    return parser.parse_args()


def twitter_auth(key, secret):
    """
        Login to Twitter.
        :param key:
        :param secret:
        :return:
    """
    try:
        auth = tweepy.OAuthHandler(key, secret)
        auth_url = auth.get_authorization_url()

        print(f"Navigate to {auth_url} to authenticate.")
        verification_code = ""
        while verification_code == "" and verification_code.lower() != "q":
            verification_code = input(f"Enter Verification Code: ")
        auth.get_access_token(verification_code)
        api = tweepy.API(auth)
        print("User Auth successful.  User:{api.me().screen_name}")
        return api
    except tweepy.error.TweepError:
        print(f"Authentication failed.")
        sys.exit(2)


def scrub_timeline(api, dry_run: bool = False):
    """
        scrub all items in the user's timeline
        :param api:
        :param dry_run:
        :return:
    """
    confirm = None
    while confirm is None:
        print("Please verify that you wish to delete all "
              "tweets for this account.")
        print("Warning: This is an unrecoverable action.")
        confirm = input("Enter yes/no: ")
        if confirm.lower() == "yes":
            confirm = True
        elif confirm.lower() == "no":
            print("Aborting.")
            sys.exit(1)
        else:
            confirm = None

        count = 0
        errors = 0
        while True:
            for status in tweepy.Cursor(api.user_timeline).items():
                try:
                    if dry_run:
                        print(f"Deleted (noop):{status.id} : {status.text}")
                    else:
                        print(f"Deleted:{status.id} : {status.text}")
                        api.destroy_status(status.id)
                        count += 1
                        time.sleep(1)
                except Exception as e:
                    print(f"Failed to delete {status.id} : {status}")
                    print(f"Error: {e}")
                    errors += 0
                if (100 * errors / count) > 25:
                    print("errors exceeds bounds")
                    sys.exit(99)
            print(f"Timeline purge completed.\n"
                  f"Messages deleted:{count}\n"
                  f"Message errors: {errors}")
            if count == 0:
                break


def scrub_likes(api, dry_run: bool = False):
    """
        Scrub likes

        :param api:
        :param dry_run:
        :return:
    """
    count = 0
    errors = 0
    while True:
        for like in tweepy.Cursor(api.favorites).items():
            try:
                if dry_run:
                    print(f"Deleted (noop):{like.id}")
                else:
                    print(f"Deleted:{like.id}")
                    api.destroy_favorite(like.id)
                    count += 1
                    time.sleep(1)
            except Exception as e:
                print(f"Failed to delete {like.id}")
                print(f"Error: {e}")
                errors += 0
            if (100 * errors / count) > 25:
                print("errors exceeds bounds")
                sys.exit(99)
        print(f"Timeline purge completed.\n"
              f"Messages deleted:{count}\n"
              f"Message errors: {errors}")
        if count == 0:
            break


def scrub_direct_messages(api, dry_run: bool = False):
    """
        Scrub direct messages.

        :param api:
        :param dry_run:
        :return:
    """
    confirm = None
    while confirm is None:
        print("Please verify that you wish to delete all "
              "direct messages for this account.")
        print("Warning: This is an unrecoverable action.")
        confirm = input("Enter yes/no: ")
        if confirm.lower() == "yes":
            confirm = True
            break
        elif confirm.lower() == "no":
            print("Aborting.")
            sys.exit(1)
        else:
            confirm = None

    count = 0
    errors = 0
    while True:
        try:
            chunk = api.list_direct_messages()
            if len(chunk) >= 1:
                for message in chunk:

                    if dry_run:
                        print(f"Deleted (noop):{message} : {message}")
                    else:
                        print(f"Deleted:{message} : {message}")
                        message.destroy()
                        count += 1

            else:
                break
        except Exception as e:
            print(f"Failed to delete {message}")
            print(f"Error: {e}")
            errors += 1
    print(f"DM purge completed.\n"
          f"Messages deleted:{count}\n"
          f"Message errors: {errors}")


def scrub_twitter(api, timeline: bool, dms: bool, likes: bool, dry_run: bool):
    if not timeline and not dms:
        print("You must use --timeline or --dms to do any actions.")
        sys.exit(1)

    print(f"timeline:{timeline}")
    print(f"dms:{dms}")

    if timeline:
        print("Purge timelines")
        scrub_timeline(api, dry_run)

    if dms:
        print("Purge Direct Messages")
        scrub_direct_messages(api, dry_run)

    if likes:
        print("Purge likes")
        scrub_likes(api, dry_run)


if __name__ == "__main__":
    args = get_arguments()
    scrub_twitter(
        twitter_auth(args.key, args.secret),
        args.timeline,
        args.dms,
        args.likes,
        args.noop)
