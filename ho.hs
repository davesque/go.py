import Data.List (intersperse, elemIndex)
import System.Cmd (rawSystem)
import System.Info (os)
import Control.Monad (void)
import Data.Function (on)

------------------------------------------------------------------------------
-- Data types
------------------------------------------------------------------------------

data Position = Empty
              | Hoshi
              | Black
              | White deriving (Show, Read, Eq)

posToChar :: Position -> Char
posToChar Empty = '+'
posToChar Hoshi = 'a'
posToChar Black = '@'
posToChar White = 'O'

newtype Line = Line { positions :: [Position] }

instance Show Line where
    show (Line ps) = intersperse '-' $ map posToChar ps

newtype Board = Board { lines :: [Line] }

instance Show Board where
    show (Board ls) = concatMap ((++"\n") . show) ls

------------------------------------------------------------------------------
-- Helpers
------------------------------------------------------------------------------

clear :: IO ()
clear = void $ rawSystem cmd []
    where cmd = if os `elem` ["win32", "mingw32"] then "cls" else "clear"

-- | Replaces an item at the specified index in a list.
replaceAt :: (Integral i) => i -> a -> [a] -> [a]
replaceAt _ _ [] = []
replaceAt i r a@(x:xs)
    | i < 0      = a
    | i == 0     = r:xs
    | otherwise  = x:replaceAt (i - 1) r xs

------------------------------------------------------------------------------
-- Functions
------------------------------------------------------------------------------

clearBoard :: Board
clearBoard = Board $
    replicate 3 clearLine ++
    [hoshiLine] ++
    replicate 5 clearLine ++
    [hoshiLine] ++
    replicate 5 clearLine ++
    [hoshiLine] ++
    replicate 3 clearLine
    where clearLine = Line $ replicate 19 Empty
          hoshiLine = Line $
            replicate 3 Empty ++
            [Hoshi] ++
            replicate 5 Empty ++
            [Hoshi] ++
            replicate 5 Empty ++
            [Hoshi] ++
            replicate 3 Empty

coord :: Char -> Maybe Int
coord = (`elemIndex` ['a'..'s'])

isInside :: Char -> Char -> Bool
isInside = (&&) `on` coordInRange
    where coordInRange c = case coord c of
                           (Just _) -> True
                           Nothing  -> False

isHoshi :: Int -> Int -> Bool
isHoshi x y = (x, y) `elem` [(p, q) | p <- [3, 9, 15], q <- [3, 9, 15]]

setPosition :: Char -> Char -> Position -> Board -> Maybe Board
setPosition x y p (Board b) = do
    iX <- coord x
    iY <- coord y
    let yLine       = b !! iY
        newPosition | p == Empty && isHoshi iX iY = Hoshi
                    | p == Hoshi                  = Empty
                    | otherwise                   = p
        newLine     = Line $ replaceAt iX newPosition (positions yLine)
        newBoard    = Board $ replaceAt iY newLine b
    return newBoard

------------------------------------------------------------------------------
-- Main
------------------------------------------------------------------------------

main :: IO ()
main = do
    clear
    print clearBoard
