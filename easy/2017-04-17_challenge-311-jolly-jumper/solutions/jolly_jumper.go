package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
    "strconv"
)

func main() {
    s := bufio.NewScanner(os.Stdin)
    for {
        s.Scan()
        line := s.Text()
        if line == "" {
            break
        }

        numbers := parseLine(line)

        fmt.Print(line)
        if isJolly(numbers) {
            fmt.Println(" JOLLY")
        } else {
            fmt.Println(" NOT JOLLY")
        }
    }
}

func parseLine(line string)(numbers []int) {
    tokens := strings.Split(line, " ")[1:]
    numbers = make([]int, len(tokens))

    for i, v := range tokens {
        numbers[i], _ = strconv.Atoi(v)
    }

    return
}

func isJolly(numbers []int)(jolly bool) {
    differences := make([]int, len(numbers) - 1)

    for i, v := range numbers[:len(numbers) - 1] {
        diff := v - numbers[i + 1]
        if diff < 0 {
            diff = diff * -1
        }
        differences[i] = diff
    }

    for i := 1; i < len(numbers); i++ {
        present := false
        for _, v := range differences {
            if i == v {
                present = true
                break
            }
        }
        if ! present {
            return false
        }
    }
    return true
}
