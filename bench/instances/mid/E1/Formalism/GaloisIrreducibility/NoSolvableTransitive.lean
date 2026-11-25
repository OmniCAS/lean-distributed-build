import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.AltNotSolvable
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.BlockBoundOfOrbits
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.FewLargeParts
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.IrredOf
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.JordanPrime
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.LemmaAOf
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.NoSolvableOf
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.OneNonUnit
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.OrbitSubSum
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.PermSubSumInv
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.PowerPCycle
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.PrimitiveOfPCycle
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.ResiduesLe
import E1.Formalism.GaloisIrreducibility.GaloisIrreducibilityProofs.RestrictRoots

set_option Elab.async false

namespace E1N.M302
def val : Nat := E1N.M287.val % 7 + E1N.M288.val % 7 + E1N.M289.val % 7 + E1N.M290.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
end E1N.M302
