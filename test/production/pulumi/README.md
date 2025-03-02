# Current
Long story short Pulumi has become a pain in the ass so aws_cli will be used instead. Pulumi likely manages the complexity of highly complex use cases - i.e. long running machines, multiple cloud providers, etc. But for the foreseeable future, aws_cli seems to be the way forward. 

# Getting pulumi working

## Prepare __main__.py
* use correct ami - confirm main ami is same as twitch ec2 nstance. ami-0f3485fd713cb1ede
* scp the script (where the script is just a log - copy func to new file and log)
  * Script:...
* for now, we'll skip Spot

Okay...so we'll clone the repo:
git clone git@github.com:adam-zakaria/twitch_detection.git

## Testing
Okay. What works and what doesn't.

I've had clients connecting to flask servers running on ec2 so this isn't new. And right now we're able to connect to the flask server on localhost:
url = "http://localhost:1337/logs"

But this does not work:
    url = "http://54.167.31.12:1337/logs"
Failed to post log: HTTPSConnectionPool(host='54.167.31.12', port=443): Max retries exceeded with url: /logs (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1000)')))

I'm almost positive I didn't need to do any ssl business for other apps, but maybe I did...

We updated the log testing POST to use the public ip and verify=False
We've shutdown the instnace and just need to observer the log getting logged, then we'll move on to doing more: running the twitch_detections/main.py and observing the logs, then integrating it into main.py (Eventually we want main.py to spawn the gpu and run the process piece.)

What's a good workflow for 

pulumi up...have browser next to it.

How to output the p

what options do I have for doing this quickly? I want to be able to shutdown and restart quickly because I am testing running a script on startup. I am potentially fine with just starting a new stack...it's not ideal, but it's cool. 1. It's not expensive anyways, but also once the stopping is initiated you are not charged. I guess that's fine.

We're going to start from scratch with a simple script maybe straight from the pulumi docs, and a small instance.