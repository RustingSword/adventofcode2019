#!/bin/bash
awk '{while($1>0){$1=int($1/3-2);if($1>0)s+=$1;}}END{print s}' input
