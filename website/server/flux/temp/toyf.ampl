# variables
var V0>=0.0, <=100.0;
var V1>=0.0, <=100.0;
var V2>=-100.0, <=100.0;
var V3>=0.0, <=100.0;
var V4>=0.0, <=100.0;
var V5>=0.0, <=100.0;
var V6>=0.0, <=100.0;
var V7>=0.0, <=100.0;
var V8>=0.0, <=100.0;
var V9>=-100.0, <=100.0;
var V10>=0.0, <=100.0;
var V11>=0.0, <=100.0;
# Objective function 
maximize Obj: 
0  + 1 * V0 + 1 * V1 + 1 * V2 + 1 * V3 + 1 * V4 + 1 * V5 + 1 * V6 + 1 * V7 + 1 * V8 + 1 * V9 + 1 * V10 + 1 * V11;
# Constraints
subject to c_akg:
	- 1.0 * V0 + 1.0 * V1 + 1.078 * V8 = 0 ;
subject to c_accoa:
	+ 1.0 * V2 - 1.0 * V4 + 1.0 * V5 + 2.928 * V8 = 0 ;
subject to c_suc:
	- 1.0 * V1 + 1.0 * V10 = 0 ;
subject to c_oaa:
	+ 1.0 * V5 + 1.786 * V8 - 1.0 * V10 - 1.0 * V11 = 0 ;
subject to c_r5p:
	+ 1.0 * V3 - 1.0 * V6 = 0 ;
subject to c_pyr:
	- 1.0 * V3 + 1.0 * V4 - 2.0 * V7 + 2.833 * V8 + 1.0 * V11 = 0 ;
subject to c_g6p:
	+ 1.0 * V6 + 1.0 * V7 + 0.205 * V8 - 1.0 * V9 = 0 ;
subject to c_icit:
	+ 1.0 * V0 - 1.0 * V5 = 0 ;
option solver ipopt;
solve > /dev/null ;
printf " === Flux Results ===\n"; printf "Objective function value %6.6f\n", Obj;  
for {k in 1.._nvars} {printf "%s\t%6.6f\n", _varname[k], _var[k];}
