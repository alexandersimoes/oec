
export function abbreviate(num, fixed) {
  if (num === null) {
    return null;
  } // terminate early

  if (num === 0) {
    return "0";
  } // terminate early

  // number of decimal places to show
  fixed = !fixed || fixed < 0 ? 0 : fixed;

  // get power
  const b = (num).toPrecision(2).split("e"),
        k = b.length === 1 ? 0 : Math.floor(Math.min(b[1].slice(1), 14) / 3), // floor at decimals, ceiling at trillions
        c = k < 1 ? num.toFixed(0 + fixed) : (num / Math.pow(10, k * 3) ).toFixed(1 + fixed), // divide by power
        d = c < 0 ? c : Math.abs(c), // enforce -0 is 0
        e = d + ['', 'K', 'M', 'B', 'T'][k]; // append power

  return e;
}
