# import
from diamond_square import diamond_square
import matplotlib.pyplot as plt

def main():
    # get landscape
    landscape = diamond_square( 400, 600, 32 )

    # plot landscape
    plt.imshow( landscape, cmap='gray' )
    plt.axis( 'off' )
    plt.show()

if __name__ == '__main__':
    main()
    print( 'Done.' )