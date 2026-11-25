import Syn.M1199
import Syn.M1312
import Syn.M1346
import Syn.M1384
import Syn.M1428
import Syn.M1459
import Syn.M1594
import Syn.M1647
import Syn.M1664
import Syn.M1668
import Syn.M1698
import Syn.M1710
import Syn.M1734
import Syn.M1735
import Syn.M1736
import Syn.M1737
import Syn.M1738
import Syn.M1775
import Syn.M1826
import Syn.M1863
import Syn.M2577

namespace Syn.M2587
def val : Nat := Syn.M1199.val % 7 + Syn.M1312.val % 7 + Syn.M1346.val % 7 + Syn.M1384.val % 7 + Syn.M1428.val % 7 + Syn.M1459.val % 7 + Syn.M1594.val % 7 + Syn.M1647.val % 7 + Syn.M1664.val % 7 + Syn.M1668.val % 7 + Syn.M1698.val % 7 + Syn.M1710.val % 7 + Syn.M1734.val % 7 + Syn.M1735.val % 7 + Syn.M1736.val % 7 + Syn.M1737.val % 7 + Syn.M1738.val % 7 + Syn.M1775.val % 7 + Syn.M1826.val % 7 + Syn.M1863.val % 7 + Syn.M2577.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2587
