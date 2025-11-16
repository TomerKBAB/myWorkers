# background worker loop
import time

def main():
    while True:
        # TODO: fetch next pending job
        # TODO: mark as RUNNING
        # TODO: execute it
        # TODO: mark as DONE or FAILED
        time.sleep(1)

if __name__ == "__main__":
    main()