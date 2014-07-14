set size ratio -1
set xrange [-84:204] 
set yrange [-72:72] 
unset key
unset border
unset tics
plot "initialHemkerMesh" using 1:2 title 'mesh' with lines lc rgb "black"
set terminal postscript eps color lw 1 "Helvetica" 20
set out 'initialHemkerMesh.eps'
replot
set term pop
replot
set border
set xrange [-5:5] 
set yrange [-5:5] 
set terminal postscript eps color lw 1 "Helvetica" 20
set out 'initialHemkerMeshDetail.eps'
replot
set term pop
replot