module Canvas
( getCanvas
, getChar
, setChar
, setChars
) where

import Prelude hiding (getChar)
import Data.Array as A
import Data.List (intersect, intercalate, unfoldr)

------------------------------------------------------------------------------
-- Helper functions
------------------------------------------------------------------------------

-- | Adapted from:
-- http://stackoverflow.com/questions/12659562/insert-specific-element-y-after-every-n-elements-in-a-list
--
-- Inserts an item `y` into a list `xs` after every `n` elements.
insert :: Int -> a -> [a] -> [a]
insert n y xs = intercalate [y] . groups $ xs
    where groups = takeWhile (not . null) . unfoldr (Just . splitAt n)

------------------------------------------------------------------------------
-- Data types
------------------------------------------------------------------------------

type Coords = (Int,Int)

newtype Canvas = Canvas (A.Array Coords Char)

instance Show Canvas where
    show (Canvas a)   = insert width '\n' content
        where content = elems a
              width   = fst . snd $ A.bounds a

------------------------------------------------------------------------------
-- Canvas functions
------------------------------------------------------------------------------

-- | Gets a canvas with width `x` and height `y`.
getCanvas :: Coords -> Canvas
getCanvas (x,y) = Canvas $ A.listArray ((1,1),(x,y)) (repeat ' ')

-- | Gets the character at the specified coordinates.
getChar :: Coords -> Canvas -> Maybe Char
getChar (x,y) (Canvas a)
    | (x,y) `elem` is = Just $ a ! (x,y)
    | otherwise       = Nothing
    where is = A.indices a

-- | Sets the character at the specified coordinates.
setChar :: Coords -> Char -> Canvas -> Maybe Canvas
setChar (x,y) c (Canvas a)
    | (x,y) `elem` is = Just $ Canvas (a // [((x,y),c)])
    | otherwise       = Nothing
    where is = A.indices a

-- | Sets the characters at the specified coordinates.
setChars :: [(Coords,Char)] -> Canvas -> Maybe Canvas
setChars aList (Canvas a)
    | indicesAreValid = Just $ Canvas (a // aList)
    | otherwise       = Nothing
    where isOld           = A.indices a
          isNew           = map fst aList
          indicesAreValid = isNew `intersect` isOld == isNew
