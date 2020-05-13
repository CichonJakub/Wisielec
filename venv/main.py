password = input('Podaj hasło\n')
#password = 'jak' # for manual tests
print(f'to jest twoje hasło: {password}\n')

tab = list(password) #lista z haslem
secret = list(password) #lista z zakrytym haslem -> do wyświetlania

#zamienienie liter na '_'
for letter in range (len(password)):
    secret[letter] = '_'

print(f"odkryta tablica znakow: {tab}\n")
print(f"zakryta tablica znakow: {secret}\n")

#try_count - ile mamy żyć :
lives = 5

#game loop
while lives > 0:
    print(f"You have got {lives} lives, dont give up!\n")
    print(' '.join(secret))

    guess = input("Plese give me your next guess :)\n")

    #success case:
    if guess in password:
        print(f'There is {guess} in the desired password ;) good job! \n')
        #changing '_' into guessed letter
        for letter in range(len(tab)):
            if password[letter] == guess:
                secret[letter] = guess

        #checking if we have guessed whole password
        if ''.join(map(str, secret)) == password:
            print(f"You have guessed the whole password! It was ' {''.join(secret)} ' MUCH WOW....\n")
            break
    #failure case:
    else:
        lives -= 1


