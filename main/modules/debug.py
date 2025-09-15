
def debugconsolemessage(message,newmessage=True):
    message=str(message)
    if not newmessage:
        print(' ')
    else:
        print('\n')
    print(message)