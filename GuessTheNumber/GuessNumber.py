secret = 42
guess = 0
tries = 0

def main():

    logfile = open("log.txt", "a")

    # for tries in range(2):      # the loop doesn't ever stop, why?
    while guess != secret:
        print "Attempt number %d " % (tries + 1)
        guess = raw_input("Type a number: ")
        if guess.isdigit():
            tries += 1
            if int(guess) == secret:
                print "Correct!"
                tries = 0
                print "Number of tries was reset to %d" % tries
                logfile.write(("Secret number guessed and number of tries was reset to %d" % tries) + '\n')
                break
            elif int(guess) < secret:
                again = raw_input("Incorrect, your number is too small. Try again (y/n)? ").lower()
                if again not in ['y', 'n']:
                    print "Type y or n"
                elif again == 'n':
                    break
            elif int(guess) > secret:
                again = raw_input("Incorrect, your number is too big. Try again (y/n)? ").lower()
                if again not in ['y', 'n']:
                    print "Type y or n"
                elif again == 'n':
                    break
        else:
            print "This is not a valid number, try again"

    logfile.close()


if __name__ == '__main__':
    main()
