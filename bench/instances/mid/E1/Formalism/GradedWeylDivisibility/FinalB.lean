import E1.Formalism.GradedWeylDivisibility.DualWeylDominanceOf
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.ClosedEqNabla
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.FockQBilin
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.FockQPos
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.FockQRowDivAdj
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.HWInClosed
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.HWLine
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.HWLineTall
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.NablaTallZero
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.RowDivClosedGraded
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.WeylEqNablaQ
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.WeylRationalOf

set_option Elab.async false

namespace E1N.M309
def val : Nat := E1N.M308.val % 7 + E1N.M315.val % 7 + E1N.M334.val % 7 + E1N.M335.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end E1N.M309
