import Data.Array as A
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

newtype Board = Board (A.Array Coords Position) deriving (Show)

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
getBoard :: Coords -> Board
getBoard (x,y) = Board $ A.listArray ((1,1),(x,y)) (repeat Empty)

-- | Gets the position at the specified coordinates.
getPosition :: Coords -> Board -> Maybe Position
getPosition (x,y) (Board a)
    | (x,y) `elem` is = Just $ a ! (x,y)
    | otherwise       = Nothing
    where is = A.indices a

-- | Sets the position at the specified coordinates.
setPosition :: Coords -> Position -> Board -> Maybe Board
setPosition (x,y) p (Board a)
    | (x,y) `elem` is = Just $ Board (a // [((x,y),p)])
    | otherwise       = Nothing
    where is = A.indices a

------------------------------------------------------------------------------
-- Main
------------------------------------------------------------------------------

--  main :: IO ()
--  main = do
--      clear
