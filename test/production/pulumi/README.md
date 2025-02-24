Okay so we're doing pulumi
spawn a gpu and run a script

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



