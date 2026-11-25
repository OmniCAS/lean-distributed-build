import E1.Formalism.GradedWeylDivisibility.FinalC
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.BlockActTensor
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.NablaLBasis
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.NablaLDiag
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.NablaLKBasis
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.NablaLLe
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.NablaLTwMem
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.NablaLTwist
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.RowActDiagWeight
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.RowActMul
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.SSBasis
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.SSIdxFinite
import E1.Formalism.GradedWeylDivisibility.FockSpaceTableaux.TensorBasis

set_option Elab.async false

namespace E1N.M311
def val : Nat := E1N.M310.val % 7 + E1N.M314.val % 7 + E1N.M373.val % 7 + E1N.M374.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end E1N.M311
