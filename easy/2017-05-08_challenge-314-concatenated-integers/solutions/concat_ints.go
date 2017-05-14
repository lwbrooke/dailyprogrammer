package main

import (
    "bufio"
    "fmt"
    "os"
    "sort"
    "strings"
    "strconv"
)

func main() {
    s := bufio.NewScanner(os.Stdin)
    for s.Scan() {
        integers := strings.Split(s.Text(), " ")
        sort.Slice(integers, func(i, j int) bool {
          iThenJ, _ := strconv.Atoi(strings.Join([]string{integers[i], integers[j]}, ""))
          jThenI, _ := strconv.Atoi(strings.Join([]string{integers[j], integers[i]}, ""))
          return iThenJ < jThenI
        })
        smallest := strings.Join(integers, "")
        sort.Slice(integers, func(i, j int) bool {
          iThenJ, _ := strconv.Atoi(strings.Join([]string{integers[i], integers[j]}, ""))
          jThenI, _ := strconv.Atoi(strings.Join([]string{integers[j], integers[i]}, ""))
          return iThenJ > jThenI
        })
        largest := strings.Join(integers, "")
        fmt.Printf("%s %s\n", smallest, largest)
    }
}
