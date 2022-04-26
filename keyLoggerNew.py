from pynput.keyboard import Key, Listener
import time

phrase = "the five boxing wizards jump quickly"

typedPhrase = []
lineList = []
times = 1


def on_press(key):
    press = time.time()
    if key == Key.esc:
        return False
    typedPhrase.append(str(key))
    lineList.append("press,"+str(key) + ","+str(press))


def on_release(key):
    release = time.time()
    lineList.append("release,"+str(key) + ","+str(release))
    if key == Key.enter:
        log_handle()


def log_handle():
    global typedPhrase, lineList, times
    typedPhrase.pop()
    typed_str = ''.join(typedPhrase)
    typed_str = typed_str.replace("'", '')
    typed_str = typed_str.replace("Key.space", " ")

    if typed_str == phrase:
        line = ','.join(lineList)
        line = line.replace("'", '')
        new_list = line.split(",")
        time_list = []
        # ORGANIZE NEW_LIST INTO FINAL_LIST
        for x in range(len(phrase)+1):

            first_press = new_list.index('press')
            letter = new_list[first_press + 1]

            time_list.append(new_list[first_press+2])

            del new_list[first_press:first_press+3]
            its_release = new_list.index(letter)
            time_list.append(new_list[its_release + 1])
            del new_list[its_release-1:its_release + 2]

        time_list = [float(x) for x in time_list]
        log = []

        # CALCULATE HOLD, DD, UD AND PUT IT IN LOG
        for x in range(len(phrase)+1):
            value = time_list.pop(0)
            time_list = [x - value for x in time_list]
            hold = time_list[0]
            log.append(round(hold, 5))

            if len(time_list) > 1:
                dd = time_list[1]
                log.append(round(dd, 5))
                value = time_list.pop(0)
                time_list = [x - value for x in time_list]
                ud = time_list[0]
                log.append(round(ud, 5))

        log = [str(x) for x in log]
        final_line = ','.join(log)
        with open("logFinalDiffKeyboard.csv", "a") as f:
            f.write(subject+","+sessionIndex+","+str(times)+","+final_line)
            f.write('\n')
        print('You have witten the phrase {0} times'.format(times))
        times += 1
    else:
        print("You wrote: "+typed_str+" / Expected: "+phrase)

    typedPhrase = []
    lineList = []


subject = input("Enter your first name: ")
sessionIndex = input("Enter session number: ")

print("Wait 1 second! Remember to press enter after each phrase")
time.sleep(1)
print("Start typing: "+phrase)

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
