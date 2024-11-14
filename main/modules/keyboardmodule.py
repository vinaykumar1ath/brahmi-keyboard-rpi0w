import json
from time import perf_counter

from .sendreport import keypress
#from .sendreport import write_report,NULL_CHAR

from .preloadata import stdkeyname_to_scancode as KeyCodes
from .preloadata import key_to_shiftheld as shifted
from .preloadata import shiftheld_to_key as nonshifted
from .preloadata import keyboard_library_keymapping as stdkeyname
from .preloadata import keypadcodes as kpcode
from .preloadata import importantkeys as impkeys
from .preloadata import essentialmodkeys as modcode
#from .preloadata import modkey_to_scancode as modcode

# Used for debugging purposes
from .debug import debugconsolemessage as dbugmsg

# Global variable Initialisations 
global keybuflist,send_keypress
keybuflist=[]
send_keypress=True

global readsettings
readsettings=False
# readsettings boolean used to indicate if settings read successfully without any errors from set.txt file
# can be used to check if settings are read

global prevtime
prevtime=perf_counter()

# these variables may be used in directly printing text in rpi console
# global text
# text='' 

try:
    with open('/home/pi/keyboardattachment/main/set.txt') as settings:
        set=json.load(settings)
    #setting language
    with open('/home/pi/keyboardattachment/main/number_to_unicode/{0}.txt'.format(set['language'])) as language:
        num2uni=json.load(language)
    #opening keymapper
    with open('/home/pi/keyboardattachment/main/layouts/{0}/{1}.txt'.format(set['language'],set['layout'])) as keymap:
        keymapper=json.load(keymap)
    if keymapper and num2uni:
        readsettings=True
except FileNotFoundError:
    raise Exception("Check the Settings")


def sendkey_asitis(keybuflist):
    print("sendkey_asitis")
    print(keybuflist)
    try:
        if len(keybuflist)==1:
            if keybuflist[0] in impkeys: # using impkeys for faster execution of program and to eliminate potential key errors
                keypress(impkeys[keybuflist[0]])
            else:
                keypress(int(KeyCodes[stdkeyname[keybuflist[0]]],16)) # using int( ,16) for decoding hexadecimal numbers
        elif len(keybuflist)==2:
            if keybuflist[0] in modcode:
                keypress(int(KeyCodes[stdkeyname[keybuflist[1]]],16),modcode[keybuflist[0]])    
        elif len(keybuflist)>2:
            pass
    except KeyError:
        pass


# def press_unicode_directway(uc):
#     uc=str(uc)
#     write_report(NULL_CHAR*8)
#     write_report(chr(4)+NULL_CHAR*7)
#     for digit in uc:
#        #write_report(chr(4)+NULL_CHAR+KeyCodes["KEY_KP{0}".format(digit)])
#        write_report(chr(4)+NULL_CHAR+chr(kpcode[int(digit)])+NULL_CHAR*5)
#        write_report(chr(4)+NULL_CHAR*7)
#     write_report(NULL_CHAR*8)

def press_unicode(uc):
    uc=str(uc)
    dbugmsg("pressunicode")
    dbugmsg(uc,False)
    keypress(0)
    keypress(0,4,False)#only presses alt key
    for digit in uc:
        keypress(kpcode[int(digit)],4,False)
        keypress(0,4,False)
    keypress(0)

# Function whether to send unicode character keypress or direct keypress 
def keymodifier(keybuflist,key):
    global readsettings,pressedkeys
    pressedkeys='~'.join(keybuflist)
    dbugmsg("keymodifier")
    dbugmsg(pressedkeys,False)
    if readsettings and pressedkeys in keymapper.keys():
        press_unicode(num2uni[str(keymapper[pressedkeys])])
    else:
        sendkey_asitis(keybuflist)
        pass


def key_pressed(key):
    global keybuflist,send_keypress
    print("\n"+key+" pressed\n")

    # condition to not add keys in bufferlist that are already present
    if key not in keybuflist:
        keybuflist.append(key)
    
    # if multiple keys are pressed at same time only first two keys pressed are considered
    if send_keypress and len(keybuflist)>=2:
        maxkeys2=keybuflist[:2]
        keymodifier(maxkeys2,key)
        send_keypress=False


def key_released(key):
    print("\n"+key+" released\n")
    dbugmsg(key)
    dbugmsg("released",False)

    # send keypresses for a single keypress
    global keybuflist,send_keypress,prevtime
    if send_keypress and len(keybuflist)==1:
        keymodifier(keybuflist,key)
        send_keypress=False
    
    #to remove all possible occurances of the key
    while key in keybuflist:
        keybuflist.remove(key)
    if key in shifted.keys():
         while shifted[key] in keybuflist:
             keybuflist.remove(shifted[key])
    if key in nonshifted.keys():
        while nonshifted[key] in keybuflist:
            keybuflist.remove(nonshifted[key])
    #maintaining list of keys pressed even after key is released to ensure not sending key presses before releasing all

    # if due to some issues, keybuflist is not emptied properly, this can flush out the keybuflist
    if not keybuflist: 
        send_keypress=True
    elif perf_counter()-prevtime > 3:
        send_keypress=True
        keybuflist=[]
        prevtime=perf_counter()