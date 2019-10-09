#!/usr/bin/env python3
"""
    twitter-scrub
    (c) 2019 Sam Caldwell.  See LICENSE.txt file.

    This tool will scrub your twitter timeline.

"""
from argparse import ArgumentParser
import tweepy
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
        help="No operation flag (for dry runs).")
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


def scrub_tweets(api, dry_run: bool = False):
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

        for status in tweepy.Cursor(api.user_timeline).items():
            try:
                # ToDo: Remove the comment below to make it real.
                if dry_run:
                    print(f"Deleted (noop):{status.id} : {status.text}")
                else:
                    print(f"Deleted:{status.id} : {status.text}")
                    # api.destroy_status(status.id)
            except Exception as e:
                print(f"Failed to delete {status.id} : {status}")
                print(f"Error: {e}")


if __name__ == "__main__":
    args = get_arguments()
    scrub_tweets(twitter_auth(args.key, args.secret), args.noop)
