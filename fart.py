from pippi import dsp
from hcj import fx
from datetime import datetime
import subprocess
import tweepy
import os

slen = dsp.rand(5, dsp.rand(15, 400))

layers = []

for _ in range(dsp.randint(2, dsp.randint(6, 50))):
    freq = dsp.rand(0.1, 5) 
    length = dsp.stf(slen)
    pulsewidth = dsp.rand(0.5, 1)
    waveform = [0] + dsp.breakpoint([ dsp.rand(-1, 1) for _ in range(dsp.randint(6, dsp.randint(10, 30))) ], 512) + [0]
    window = dsp.wavetable('tri', 512)
    mod = dsp.wavetable('phasor', 100)
    mod = dsp.breakpoint(mod[-1:] + [ dsp.rand() for _ in range(50) ], 1024*2)
    modrange = dsp.rand(1, 10)
    modfreq = 1.0 / slen
    amp = dsp.rand(0.3, 0.75)

    layer = dsp.pulsar(freq, length, pulsewidth, waveform, window, mod, modrange, modfreq, amp)
    layer = fx.penv(layer)

    layers += [ layer ]

out = dsp.mix(layers)

now = datetime.now()
filename = 'fart-%s-%s-%s-%s' % (now.year, now.month, now.day, now.hour)

dsp.write(out, filename)
print 'rendered'

print subprocess.call('sox %s.wav -C 320 %s.mp3 norm' % (filename, filename), shell=True)
print subprocess.call('scp %s.mp3 hecanjog.com:hecanjog.com/farts/' % filename, shell=True)

# Authenticate w/ twitter as @fartsynthesis
consumer_key = os.environ['FART_CONSUMER_KEY']
consumer_secret = os.environ['FART_CONSUMER_SECRET']
access_token = os.environ['FART_ACCESS_KEY']
access_token_secret = os.environ['FART_ACCESS_SECRET']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Make the fart hashtag
letters = ['p','P','f','F','t','s','S','h','H']
fart_hash = '#' + ''.join([ dsp.randchoose(letters) for _ in range(dsp.randint(6, 12)) ])
tweet = '%s #fartsynthesis http://hecanjog.com/farts/%s.mp3' % (fart_hash, filename)

# Send the tweet
print 'Tweeting...'
api.update_status(tweet)

print tweet
