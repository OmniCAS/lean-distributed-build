import Syn.M2012
import Syn.M2014
import Syn.M2015
import Syn.M2016
import Syn.M2017
import Syn.M2018
import Syn.M2019
import Syn.M2027
import Syn.M2058
import Syn.M2059
import Syn.M2060
import Syn.M2061
import Syn.M2062
import Syn.M2063
import Syn.M2064
import Syn.M2065
import Syn.M2066
import Syn.M2067
import Syn.M2069
import Syn.M2070
import Syn.M2106
import Syn.M2107
import Syn.M2108
import Syn.M2607

namespace Syn.M2609
def val : Nat := Syn.M2012.val % 7 + Syn.M2014.val % 7 + Syn.M2015.val % 7 + Syn.M2016.val % 7 + Syn.M2017.val % 7 + Syn.M2018.val % 7 + Syn.M2019.val % 7 + Syn.M2027.val % 7 + Syn.M2058.val % 7 + Syn.M2059.val % 7 + Syn.M2060.val % 7 + Syn.M2061.val % 7 + Syn.M2062.val % 7 + Syn.M2063.val % 7 + Syn.M2064.val % 7 + Syn.M2065.val % 7 + Syn.M2066.val % 7 + Syn.M2067.val % 7 + Syn.M2069.val % 7 + Syn.M2070.val % 7 + Syn.M2106.val % 7 + Syn.M2107.val % 7 + Syn.M2108.val % 7 + Syn.M2607.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2609
