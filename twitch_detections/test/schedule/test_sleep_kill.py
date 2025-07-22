"""
Okay, so the schedule...what does the test blocking say? Well...what's the goal? The goal is execute the schedule no matter what. But 

Some ideas:
Check if streamer is online before trying to kill?

The wait() call might mess things up? If the kill doesn't work then the wait() will block...(it's not in a thread). Could do poll()? But also maybe wait()ish is unnecessary. 

"""