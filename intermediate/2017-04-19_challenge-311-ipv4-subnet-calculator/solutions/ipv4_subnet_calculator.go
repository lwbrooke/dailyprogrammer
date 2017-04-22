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
    pretty string
}

type node struct {
    value address
    next *node
}

func main() {
    s := bufio.NewScanner(os.Stdin)
    s.Scan()
    count, _ := strconv.Atoi(s.Text())
    var addresses *node
    for i := 0; s.Scan() && i < count; i++ {
        addr := parseLine(s.Text())
        uncovered_address := true

        var prev *node
        for cur := addresses; cur != nil; prev, cur = cur, cur.next {
            if cur.value.cidr & addr.mask == addr.cidr { // covers existing address
                if prev == nil { // at head of list
                    addresses = cur.next
                    prev = cur.next
                } else {
                    prev.next = cur.next
                    cur = prev
                }
            } else if addr.cidr & cur.value.mask == cur.value.cidr { // covered by existing address
                uncovered_address = !uncovered_address
                break
            }
        }
        if uncovered_address {
            addresses = &node{addr, addresses}
        }
    }

    printAll(addresses)
}

func parseLine(line string)(addr address) {
    tokens := strings.Split(line, "/")

    var ipv4 uint
    for i, v := range strings.Split(tokens[0], ".") {
        octet, _ := strconv.ParseUint(v, 10, 32)
        ipv4 |= uint(octet << uint(24 - 8 * i))
    }

    bit_count, _ := strconv.Atoi(tokens[1])
    mask := uint(0xFFFFFFFF) << uint(32 - bit_count)
    addr = address{ipv4 & mask, mask, line}

    return
}

func printAll(n *node) {
    if n == nil {return}
    printAll(n.next)
    fmt.Printf("%s\n", n.value.pretty)
}
