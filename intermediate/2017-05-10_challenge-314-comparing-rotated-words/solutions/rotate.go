package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    s := bufio.NewScanner(os.Stdin)
    for s.Scan() {
        line := s.Text()
        rotation, size := line, 0
        for i := 0; i < len(line); i++ {
          attempt := line[i:] + line[:i]
          if attempt < rotation {
            rotation, size = attempt, i
          }
        }
        fmt.Printf("%d %s\n", size, rotation)
    }
}
