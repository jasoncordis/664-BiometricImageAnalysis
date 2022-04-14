from greyscale import *
from binary import *

def main():
    print("PROJECT 5 DEMO \nWelcome to the project demo.")
    while True:
        user_input = input('Enter g for greyscale or enter b for binary. Enter q to quit. \n')
        if(user_input == 'g'):
            example = input('Greyscale Demo \nEnter 1 for Example 1 or 2 for Example 2 \n')
            if(example == '1'):
                greyscale_heads('0001_greyscale.png')
            elif(example == '2'):
                    greyscale_heads('0146_greyscale.png')
            else:('Invalid example.')
                    
        elif(user_input == 'b'):
            example = input('Binary Demo \nEnter 1 for Example 1 or 2 for Example 2 \n')
            if(example == '1'):
                binaryFile('lonefishintersect2.png')
        elif(user_input == 'q'):
            break
        else:('Invalid command.')
        
if __name__ == "__main__":
    main()

