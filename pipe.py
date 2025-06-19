import threading
import queue
import atexit

# Worker queue to do IO async, should most likely be external like a GCP pub/sub
pipe = queue.Queue(1000) # 1000 events should be enough for everyone
listeners = []

# Exit cleanups
def exit_handler():
    pipe.join() # Process all events before exit, what could possibly go wrong? 😀
    pipe.shutdown()

atexit.register(exit_handler)

# RISK: queue is built up and consumer doesn't stand a chance to process all
def worker():
    global listeners
    while True:
        item = pipe.get()
        for f in listeners:
            f(item)
        pipe.task_done()
        print(f"Done processing event {item}")

threading.Thread(target=worker, daemon=True).start()
