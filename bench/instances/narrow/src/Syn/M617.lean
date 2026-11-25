import Syn.M384
import Syn.M454
import Syn.M455
import Syn.M456
import Syn.M457
import Syn.M518
import Syn.M519
import Syn.M520
import Syn.M535
import Syn.M564
import Syn.M566
import Syn.M593
import Syn.M607

namespace Syn.M617
def val : Nat := Syn.M384.val % 7 + Syn.M454.val % 7 + Syn.M455.val % 7 + Syn.M456.val % 7 + Syn.M457.val % 7 + Syn.M518.val % 7 + Syn.M519.val % 7 + Syn.M520.val % 7 + Syn.M535.val % 7 + Syn.M564.val % 7 + Syn.M566.val % 7 + Syn.M593.val % 7 + Syn.M607.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M617
