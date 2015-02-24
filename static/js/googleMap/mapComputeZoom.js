/**
 * Created by laurianemollier on 22/02/15.
 */


function radiusToZoom(r, map){
    var w = map.getDiv().offsetWidth;
    var d = r * 2;
    var zooms = [21282,16355,10064,5540,2909,1485,752,378,190,95,48,24,12,6,3,1.48,0.74,0.37,0.19];
    var z = 20, m;
    while( zooms[--z] ){
        m = zooms[z] * w;
        if( d < m ){
            break;
        }
    }
//    return z;
    return 10;
}