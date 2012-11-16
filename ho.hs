import Data.Array.IO as A
import Data.Array.MArray as M
import Data.List (elemIndex)
import System.Cmd (rawSystem)
import System.Info (os)
import Control.Monad (void)

------------------------------------------------------------------------------
-- Data types
------------------------------------------------------------------------------

data Position = Empty
              | Black
              | White deriving (Show, Read, Eq)

posToChar :: Position -> Char
posToChar Empty = '+'
posToChar Black = '@'
posToChar White = 'O'

type Coords = (Int,Int)

type Board = A.IOArray Coords Position

------------------------------------------------------------------------------
-- Helpers
------------------------------------------------------------------------------

clear :: IO ()
clear = void $ rawSystem cmd []
    where cmd | os `elem` ["win32", "mingw32"] = "cls"
              | otherwise                      = "clear"

-- | Replaces an item at the specified index in a list.
replaceAt :: (Integral a) => a -> b -> [b] -> [b]
replaceAt _ _ [] = []
replaceAt i r a@(x:xs)
    | i < 0      = a
    | i == 0     = r:xs
    | otherwise  = x:replaceAt (i - 1) r xs

-- | Safely gets the head of a list.
safeHead :: [a] -> Maybe a
safeHead xs = if not $ null xs
              then Just $ head xs
              else Nothing

-- | Safely gets an item in a list by index.
safeIndex :: (Integral b) => [a] -> b -> Maybe a
safeIndex [] _ = Nothing
safeIndex (x:xs) i
    | i < 0     = Nothing
    | i == 0    = Just x
    | otherwise = safeIndex xs (i - 1)

(!!!) :: (Integral b) => [a] -> b -> Maybe a
(!!!) = safeIndex

------------------------------------------------------------------------------
-- Functions
------------------------------------------------------------------------------

coord :: Char -> Maybe Int
coord = fmap (+1) . (`elemIndex` ['a'..'s'])

-- | Gets a board with width `x` and height `y`.
getBoard :: Coords -> IO Board
getBoard (x,y) = newArray ((1,1),(x,y)) Empty

-- | Gets the position at the specified coordinates.
getPosition :: Board -> Coords -> IO Position
getPosition = readArray

-- | Sets the position at the specified coordinates.
setPosition :: Board -> Coords -> Position -> IO ()
setPosition = writeArray

------------------------------------------------------------------------------
-- Main
------------------------------------------------------------------------------

main :: IO ()
main = do
    b <- getBoard (19,19)
    print b
    return ()
