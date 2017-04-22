package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
    "strconv"
)

type address struct {
    cidr, mask uint
}

func main() {
    s := bufio.NewScanner(os.Stdin)
    s.Scan() // discard first line
    addresses := make(map[string]address)
    for s.Scan() {
        line := s.Text()
        if line == "" {
            break
        }

        addr := parseLine(line)
        add_key := true
        for k, a := range addresses {
            if a.cidr & addr.mask == addr.cidr {
                delete(addresses, k)
            } else if addr.cidr & a.mask == a.cidr {
                add_key = !add_key
                break
            }
        }
        if add_key {
            addresses[line] = addr
        }
    }

    for k := range addresses {
        fmt.Printf("%s\n", k)
    }
}

func parseLine(line string)(addr address) {
    tokens := strings.Split(line, "/")

    var ipv4 uint
    for i, v := range strings.Split(tokens[0], ".") {
        octet, _ := strconv.ParseUint(v, 10, 32)
        octet = octet << uint(8 * (4 - i - 1))
        ipv4 |= uint(octet)
    }

    bit_count, _ := strconv.Atoi(tokens[1])
    mask := uint(0xFFFFFFFF) << uint(32 - bit_count)
    addr = address{ipv4 & mask, mask}

    return
}
