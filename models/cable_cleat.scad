module hullplate() {
$fn=100;
   hull() {
	   cube([30,20,5]);
       translate([0,10,0]) cylinder(r=10,h=5);
       translate([30,10,0]) cylinder(r=10,h=5);
   }
}

module halfcleat() {
$fn=100;
   difference() {
   hullplate();
   translate([2,2,0])scale([0.8,0.8,2.0]) hullplate();
   translate([-10,0,0]) cube([30,30,10]);
   }
}

module cleat_arms() {
$fn=100;
union() {
    translate([-30,0,0]) scale ([1.0,0.6,1.0]) halfcleat();
    translate([65,12,0]) scale ([1.0,0.6,1.0]) rotate([0,0,180]) halfcleat();
    translate([-12,0,0]) cube([60,3,5]);
}
}

module cleat_bracket() {
$fn=100;
difference() {
translate([-30,0,0]) cube([60,6.5,5]);
translate([-20,5,0]) scale([0.75,1,1.0]) cylinder(r=3.5,h=10);
translate([20,5,0]) scale([0.75,1,1.0]) cylinder(r=3.5,h=10);

}
}

module cleat() {
     translate([-18,0,0])cleat_arms();
     translate([0,-10,0])cleat_bracket();
}

module cleat_assembly() {
$fn=100;
difference() {
      cleat();
      translate([-27,8,3]) rotate([90,0,0]) cylinder(r=1,h=30);
      translate([0,8,3]) rotate([90,0,0]) cylinder(r=1,h=30);
      translate([27,8,3]) rotate([90,0,0]) cylinder(r=1,h=30);
}
}
cleat_assembly();
