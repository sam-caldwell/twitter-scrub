twitter-scrub
=============
(c) 2019 Sam Caldwell.  MIT License.

### Purpose
This utility will scrub your Twitter timeline of anything and everything.

### Warning
* Download your twitter history first from their site.
* THIS IS IRREVOCABLE AND IRREVERSIBLE.

### Getting Started
To setup the tool, you'll need to...
1. Create a twitter development account (https://developer.twitter.com/).
2. Then register your app (https://developer.twitter.com/en/apps/).
3. Clone the github repo: `git@github.com:sam-caldwell/twitter-scrub.git`
4. Open a terminal and navigate into the local repo.
5. Install python3.

### Use the tool...
Using your key and secret from the registered app in your twitter developer account,
run the scrub.py script and follow it's prompts.
```
python3 scrub.py -h
usage: scrub.py [-h] [--noop] [--timeline] [--dms] --key KEY --secret SECRET

scrub a given twitter account's posts

optional arguments:
  -h, --help       show this help message and exit
  --noop           No operation flag (for dry runs).
  --timeline       Purge timeline
  --dms            Purge direct messages
  --key KEY        Consumer Key
  --secret SECRET  Consumer secret
```
