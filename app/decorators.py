from threading import Thread

# Creates background thread using decorator '@threader'
def threader(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper