# author: luojun
# date: 2019/12/6 21:06


import sentry_sdk

# test = sentry_sdk.init("https://50fd3b3e95f44277a64c8c65870c279d@sentry.io/1540553")
test = sentry_sdk.init("http://00ddf49506714a30b0e7ed70a5f05884@localhost:9000/2")

# http://00ddf49506714a30b0e7ed70a5f05884@localhost:9000/2
res = 1 / 0
