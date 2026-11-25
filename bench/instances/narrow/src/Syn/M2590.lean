import Syn.M1535
import Syn.M1537
import Syn.M1575
import Syn.M1576
import Syn.M1577
import Syn.M1578
import Syn.M1579
import Syn.M1580
import Syn.M1611
import Syn.M1840
import Syn.M1890
import Syn.M1891
import Syn.M2227
import Syn.M2253
import Syn.M2254
import Syn.M2255
import Syn.M2256
import Syn.M2290
import Syn.M2291
import Syn.M2546
import Syn.M2547
import Syn.M2582

namespace Syn.M2590
def val : Nat := Syn.M1535.val % 7 + Syn.M1537.val % 7 + Syn.M1575.val % 7 + Syn.M1576.val % 7 + Syn.M1577.val % 7 + Syn.M1578.val % 7 + Syn.M1579.val % 7 + Syn.M1580.val % 7 + Syn.M1611.val % 7 + Syn.M1840.val % 7 + Syn.M1890.val % 7 + Syn.M1891.val % 7 + Syn.M2227.val % 7 + Syn.M2253.val % 7 + Syn.M2254.val % 7 + Syn.M2255.val % 7 + Syn.M2256.val % 7 + Syn.M2290.val % 7 + Syn.M2291.val % 7 + Syn.M2546.val % 7 + Syn.M2547.val % 7 + Syn.M2582.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M2590
