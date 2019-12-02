#!/bin/awk -f

{
  input = $1
  found = 0
  # brute force
  for (noun = 0; noun <= 99 && !found; noun++) {
    for (verb = 0; verb <= 99 && !found; verb++) {
      split(input, a, ",")
      a[2] = noun
      a[3] = verb
      l = length(a)
      i = 1
      while (i <= l) {
        if (a[i] == 99) {
          if (a[1] == 19690720) {
            print noun * 100 + verb
            found = 1
          }
          break
        }
        if (a[i] == 1) {
          a[a[i+3] + 1] = a[a[i+1] + 1] + a[a[i+2] + 1]
        } else if (a[i] == 2) {
          a[a[i+3] + 1] = a[a[i+1] + 1] * a[a[i+2] + 1]
        }
        i += 4
      }  # while
    }  # for
  }  # for
}
