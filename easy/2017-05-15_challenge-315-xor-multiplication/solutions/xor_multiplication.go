package main

import (
    "fmt"
    "bufio"
    "os"
    "strings"
    "strconv"
)

func main() {
    s := bufio.NewScanner(os.Stdin)
    for s.Scan() {
        line := strings.TrimSpace(s.Text())
        asStrings := strings.Split(line, " ")
        firstFactor, _ := strconv.ParseUint(asStrings[0], 10, 32)
        secondFactor, _ := strconv.ParseUint(asStrings[1], 10, 32)
        product := xorMultiply(uint(firstFactor), uint(secondFactor))
        fmt.Printf("%d@%d=%d\n", firstFactor, secondFactor, product)
    }
}

func xorMultiply(a, b uint)(product uint) {
    for ; b != 0; a, b = a << 1, b >> 1 {
        product ^= (a * (b & 1))
    }
    return
}
