
def stop_me(reason, exitcode=23):
    from sys import exit
    print('[FATAL] - %s' %(str(reason)))
    exit(exitcode)

def warn_me(reason):
    print('[WARNING] - %s' %(str(reason)))
