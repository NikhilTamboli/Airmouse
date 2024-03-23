function start(){
    if (window.DeviceMotionEvent == undefined) {
        //No accelerometer is present. Use buttons. 
        document.getElementById("status").innerHTML = "Accelerometer not detected";
    }
    else {
        document.getElementById("status").innerHTML = "Accelerometer detected";
        window.addEventListener("devicemotion", accelerometerUpdate, true);
    }
    
    function accelerometerUpdate(e) {
        var aX = e.accelerationIncludingGravity.x*1;
        var aY = e.accelerationIncludingGravity.y*1;
        var aZ = e.accelerationIncludingGravity.z*1;
        //The following two lines are just to calculate a
        // tilt. Not really needed. 
        xPosition = Math.atan2(aY, aZ);
        yPosition = Math.atan2(aX, aZ);
    
        document.getElementById("x").innerHTML = xPosition;
        document.getElementById("y").innerHTML = yPosition;
    
    }

    window.setInterval(start,1000);
}
