#!/bin/bash
awk '{s+=int($1/3-2)}END{print s}' input
