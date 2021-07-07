var units = ['C', 'Pa', 'kPa', 'MPa'];

function bytesToFloat(bytes) {
    "use strict";
    var bits = bytes[3] << 24 | bytes[2] << 16 | bytes[1] << 8 | bytes[0];
    var sign = (bits >>> 31 === 0) ? 1.0 : -1.0;
    var e = bits >>> 23 & 0xff;
    var m = (e === 0) ? (bits & 0x7fffff) << 1 : (bits & 0x7fffff) | 0x800000;
    var f = sign * m * Math.pow(2, e - 150);
    return f;
}

function decodeUplink(input) {
    "use strict";
    switch (input.fPort) {
        case 99:
            return {
                data: {
                    longitude: readInt16LE(input.bytes.slice(7, 9)) * 0xffff / 1e7,
                    latitude: readInt16LE(input.bytes.slice(5, 7)) * 0xffff / 1e7,
                    altitude: readUInt16LE(input.bytes.slice(9, 11)) * 0xff / 1000,

                }
            };
        default:
            return {
                errors: ['Unknown FPort - see device manual!'],
            };
    }
}

/* ******************************************
* bytes to number
********************************************/
function readUInt16LE(bytes) {
    var value = (bytes[1] << 8) + bytes[0];
    return value & 0xffff;
}

function readInt16LE(bytes) {
    var ref = readUInt16LE(bytes);
    return ref > 0x7fff ? ref - 0x10000 : ref;
}