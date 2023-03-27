import pygame

# inititalizig pygame
def init():
    pygame.init()
    win = pygame.display.set_mode((400,400))


# acquiring the keystrokes with pygame for keyboard control
def getKey(keyName):
    ans = False
    
    for events in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()


    return ans

def main():
    if getKey("LEFT"):
        print("LEFT")
    if getKey("RIGHT"):
        print("RIGHT")


if __name__ == "__main__":
    init()
    while True:
        main()