# import
import numpy as np

# diamond square algorithm
def diamond_square( width, height, sample_size=2, scale=1.0, scale_reduction=2.0 ):
    """Diamond Square Algorithm.

    <a href="https://en.wikipedia.org/wiki/Diamond-square_algorithm">Wikipedia</a>

    @type width: int
    @param width: Width of landscape.

    @type height: int
    @param height: Height of landscape.

    @type sample_size: int
    @param sample_size: Defines the size of initial grid.

    @type scale: float
    @param scale: Scale of random numbers.

    @type scale_reduction: float
    @param scale_reduction: Defines reduction rate of scale variable between iteration steps.

    @rtype: float
    @return: Landscape.
    """

    # parameter
    sample_size = int( 2 * sample_size )

    # determine 2^n
    width_b2    = __getNextBiggerBase2Potenz( width )
    height_b2   = __getNextBiggerBase2Potenz( height )
    if( width_b2 < sample_size ):
        width_b2 = sample_size
    if ( height_b2 < sample_size ):
        height_b2 = sample_size

    # data
    data = np.empty( [ width_b2 + 1, height_b2 + 1 ] )

    # initialize
    for y in range( 0, height_b2 + 1, sample_size ) :
        for x in range( 0, width_b2 + 1, sample_size ) :
            data[ x, y ] = __get_random( scale )

    # core algorithm
    while( sample_size > 1 ):
        # square step
        for y in range( 0, height_b2, sample_size ) :
            for x in range( 0, width_b2, sample_size ) :
                data = __square( x, y, sample_size, scale, data )

        # diamond step
        for y in range( 0, height_b2, sample_size ) :
            for x in range( 0, width_b2, sample_size ) :
                data = __diamond( x, y, sample_size, scale, data )

        # adjust parameter
        sample_size = int( sample_size / 2 )
        scale /= scale_reduction

    return data[ :width, :height ]

# square step
def __square( x, y, size, scale, values ):
    # A   B
    #   E
    # C   D

    A = values[ x, y ]
    B = values[ x + size, y ]
    C = values[ x, y + size ]
    D = values[ x + size, y + size ]

    E = ( ( A + B + C + D ) / 4.0 ) + __get_random( scale )
    values[ int( x + size / 2 ), int( y + size / 2 ) ] = E

    return values

# diamond step
def __diamond( x, y, size, scale, values ):
    # A G B
    # F E H
    # C I D

    A = values[ x, y ]
    B = values[ x + size, y ]
    C = values[ x, y + size ]
    D = values[ x + size, y + size ]
    E = values[ int( x + size / 2 ), int( y + size / 2 ) ]

    hs = int( size / 2 )

    if( 0 <= x - hs < values.shape[ 0 ] ):
        f = values[ x - hs, y + hs ]
    else:
        f = E

    if( 0 <= y - hs < values.shape[ 1 ] ):
        g = values[ x + hs, y - hs ]
    else:
        g = E

    if( 0 <= x + size + hs < values.shape[ 0 ] ):
        h = values[ x + size + hs, y + hs ]
    else:
        h = E

    if( 0 <= y + size + hs < values.shape[ 1 ] ):
        i = values[ x + hs, y + size + hs  ]
    else:
        i = E

    F = ( ( A + E + C + f ) / 4.0 ) + __get_random( scale )
    G = ( ( A + E + B + g ) / 4.0 ) + __get_random( scale )
    H = ( ( B + E + D + h ) / 4.0 ) + __get_random( scale )
    I = ( ( D + E + C + i ) / 4.0 ) + __get_random( scale )

    values[ x, y + hs ] = F
    values[ x + hs, y ] = G
    values[ x + size, y + hs ] = H
    values[ x + hs, y + size ] = I

    return values

# generate random number [ -1.0, 1.0 ]
def __get_random( scale ):
    return ( np.random.rand( 1, 1 ) * 2.0 - 1.0 ) * scale

# next bigger base 2
def __getNextBiggerBase2Potenz( x ):
    return 1 << ( x - 1 ).bit_length()