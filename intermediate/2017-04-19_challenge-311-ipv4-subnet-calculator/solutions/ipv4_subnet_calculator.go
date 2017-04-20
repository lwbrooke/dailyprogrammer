package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
    "strconv"
)

type address struct {
    ipv4, mask uint
}

func main() {
    s := bufio.NewScanner(os.Stdin)
    s.Scan() // discard first line
    addresses := make(map[string]address)
    for {
        s.Scan()
        line := s.Text()
        if line == "" {
            break
        }

        key, addr := parseLine(line)
        cidr := addr.ipv4 & addr.mask
        add_key := true
        for k, a := range addresses {
            if a.ipv4 & addr.mask == cidr {
                delete(addresses, k)
            } else if addr.ipv4 & a.mask == a.ipv4 & a.mask {
                add_key = !add_key
                break
            }
        }
        if add_key {
            addresses[key] = addr
        }
    }

    for k := range addresses {
        fmt.Printf("%s\n", k)
    }
}

func parseLine(line string)(key string, addr address) {
    tokens := strings.Split(line, "/")
    key = line

    var ipv4 uint
    for i, v := range strings.Split(key, ".") {
        u64, _ := strconv.ParseUint(v, 10, 32)
        octet := uint(u64)
        octet = octet << uint(8 * (4 - i - 1))
        ipv4 |= octet
    }

    bitmask_bits, _ := strconv.Atoi(tokens[1])
    var mask uint = getMask(bitmask_bits)
    addr = address{ipv4, mask}

    return
}

func getMask(bits int)(mask uint) {
    mask = 2
    for i := 1; i < bits; i++ {
        mask = mask * 2
    }
    mask = mask - 1
    mask = mask << uint(32 - bits)
    return
}
