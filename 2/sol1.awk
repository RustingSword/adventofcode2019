#!/bin/awk -f
{
  split($1, a, ",")
  a[2] = 12
  a[3] = 2
  l = length(a)
  i = 1
  while(i <= l) {
    if(a[i] == 99) {
      print a[1]
      break
    }
    if(a[i] == 1) {
      a[a[i+3] + 1] = a[a[i+1] + 1] + a[a[i+2] + 1]
    } else if (a[i] == 2) {
      a[a[i+3] + 1] = a[a[i+1] + 1] * a[a[i+2] + 1]
    }
    i += 4
  }
}
